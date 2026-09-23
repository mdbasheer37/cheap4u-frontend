#!/usr/bin/env python3
"""
Verify that an Android package (.aab or .apk) is 16 KB page-size compatible.

Pure-stdlib: parses ELF program headers itself, so the result does not depend
on which readelf happens to be installed.

Checks (any failure => exit code 1):
  * package exists and is a valid zip
  * for .aab: it really is an App Bundle (BundleConfig.pb, base/manifest/AndroidManifest.xml)
  * every native library under lib/<abi>/ (apk) or <module>/lib/<abi>/ (aab):
      - is a parseable ELF
      - EVERY PT_LOAD segment has p_align >= 16384 and a multiple of 16384
      - p_offset % p_align == p_vaddr % p_align   (segment is really loadable at that alignment)
  * libraries hidden inside nested archives are checked too. python-for-android
    ships all Python C-extensions (kivy/*.so, pillow, ...) inside lib/<abi>/libpybundle.so
    (a tar) and/or assets/private.tar. Play's scanner cannot see those, but a 16 KB
    device still has to dlopen them, so they must be aligned as well.

Only 64-bit ABIs (arm64-v8a, x86_64) are required to be 16 KB aligned by Google Play;
32-bit ABIs are listed but not failed.
"""
import argparse
import io
import os
import struct
import sys
import tarfile
import zipfile

REQUIRED = 16384
STRICT_ABIS = ("arm64-v8a", "x86_64")
PT_LOAD = 1


def elf_load_segments(data):
    """Return (machine, bits, [(p_offset, p_vaddr, p_align)]) or raise ValueError."""
    if len(data) < 64 or data[:4] != b"\x7fELF":
        raise ValueError("not an ELF file")
    ei_class, ei_data = data[4], data[5]
    if ei_data != 1:
        raise ValueError("big-endian ELF not supported")
    if ei_class == 2:  # 64-bit
        e_machine = struct.unpack_from("<H", data, 18)[0]
        e_phoff = struct.unpack_from("<Q", data, 32)[0]
        e_phentsize, e_phnum = struct.unpack_from("<HH", data, 54)
        bits = 64
        segs = []
        for i in range(e_phnum):
            off = e_phoff + i * e_phentsize
            p_type = struct.unpack_from("<I", data, off)[0]
            if p_type == PT_LOAD:
                p_offset, p_vaddr = struct.unpack_from("<QQ", data, off + 8)
                p_align = struct.unpack_from("<Q", data, off + 48)[0]
                segs.append((p_offset, p_vaddr, p_align))
    elif ei_class == 1:  # 32-bit
        e_machine = struct.unpack_from("<H", data, 18)[0]
        e_phoff = struct.unpack_from("<I", data, 28)[0]
        e_phentsize, e_phnum = struct.unpack_from("<HH", data, 42)
        bits = 32
        segs = []
        for i in range(e_phnum):
            off = e_phoff + i * e_phentsize
            p_type = struct.unpack_from("<I", data, off)[0]
            if p_type == PT_LOAD:
                p_offset, p_vaddr = struct.unpack_from("<II", data, off + 4)
                p_align = struct.unpack_from("<I", data, off + 28)[0]
                segs.append((p_offset, p_vaddr, p_align))
    else:
        raise ValueError("unknown ELF class")
    if not segs:
        raise ValueError("ELF has no PT_LOAD segments")
    return e_machine, bits, segs


def check_elf(data):
    """Return (ok, min_align, problem)."""
    machine, bits, segs = elf_load_segments(data)
    min_align = min(a for _, _, a in segs)
    for off, vaddr, align in segs:
        if align < REQUIRED or align % REQUIRED != 0:
            return False, min_align, "PT_LOAD p_align=0x%x (need a multiple of 0x%x)" % (align, REQUIRED)
        if off % align != vaddr % align:
            return False, min_align, ("PT_LOAD offset 0x%x and vaddr 0x%x are not congruent modulo p_align 0x%x"
                                      % (off, vaddr, align))
    return True, min_align, ""


def abi_of(path):
    parts = path.split("/")
    if "lib" in parts:
        i = parts.index("lib")
        if i + 1 < len(parts) - 1:
            return parts[i + 1]
    return None


class Report:
    def __init__(self, blame_dir):
        self.failures = []
        self.checked = 0
        self.blame_dir = blame_dir

    def blame(self, name):
        if not self.blame_dir or not os.path.isdir(self.blame_dir):
            return []
        base = os.path.basename(name)
        hits = []
        for root, _, files in os.walk(self.blame_dir):
            if base in files:
                hits.append(os.path.join(root, base))
                if len(hits) >= 5:
                    break
        return hits

    def record(self, label, data, strict):
        try:
            ok, min_align, problem = check_elf(data)
        except ValueError as exc:
            if label.endswith(".so"):
                print("%s -> SKIP (%s)" % (label, exc))
            return
        self.checked += 1
        if ok:
            print("%s -> OK (min PT_LOAD align 0x%x)" % (label, min_align))
        elif not strict:
            print("%s -> NOT 16 KB aligned, but ABI is 32-bit (not required by Google Play)" % label)
        else:
            print("%s -> FAIL" % label)
            self.failures.append((label, problem, min_align))


def scan_tar(rep, label, blob, strict):
    try:
        tf = tarfile.open(fileobj=io.BytesIO(blob), mode="r:*")
    except tarfile.TarError:
        return False
    n = 0
    for m in tf:
        if m.isfile() and m.name.endswith(".so"):
            f = tf.extractfile(m)
            if f is None:
                continue
            n += 1
            rep.record("%s!/%s" % (label, m.name), f.read(), strict)
    print("  (%s: nested tar archive containing %d .so file(s))" % (label, n))
    return True


def scan_zip_members(rep, zf, prefix=""):
    for info in sorted(zf.infolist(), key=lambda i: i.filename):
        name = info.filename
        if info.is_dir():
            continue
        in_lib = "/lib/" in ("/" + name) and name.endswith(".so")
        is_private_tar = name.endswith("private.tar") or name.endswith("private.mp3")
        if not (in_lib or is_private_tar):
            continue
        abi = abi_of(name)
        strict = (abi in STRICT_ABIS) if abi else True
        blob = zf.read(name)
        if blob[:4] == b"\x7fELF":
            rep.record(prefix + name, blob, strict)
        elif not scan_tar(rep, prefix + name, blob, strict):
            if is_private_tar:
                # private.tar may be gz/plain tar; already tried. Anything else is not ours.
                print("%s -> SKIP (not an ELF, not a tar)" % (prefix + name))
            else:
                print("%s -> SKIP (not an ELF, not a tar; e.g. asset payload)" % (prefix + name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("package", help=".aab or .apk")
    ap.add_argument("--blame-dir", help="directory to search (e.g. .buildozer) to locate the recipe that produced a bad .so")
    args = ap.parse_args()

    pkg = args.package
    print("Checking native libraries for 16 KB compatibility...")
    print("Package: %s" % pkg)
    if not os.path.isfile(pkg):
        print("16 KB PAGE SIZE CHECK: FAIL\nProblem: package does not exist: %s" % pkg)
        return 1
    if not zipfile.is_zipfile(pkg):
        print("16 KB PAGE SIZE CHECK: FAIL\nProblem: %s is not a valid zip/AAB/APK" % pkg)
        return 1

    zf = zipfile.ZipFile(pkg)
    bad = zf.testzip()
    if bad:
        print("16 KB PAGE SIZE CHECK: FAIL\nProblem: corrupt zip entry %s" % bad)
        return 1
    names = set(zf.namelist())

    if pkg.endswith(".aab"):
        need = ("BundleConfig.pb", "base/manifest/AndroidManifest.xml")
        missing = [n for n in need if n not in names]
        if missing:
            print("16 KB PAGE SIZE CHECK: FAIL\nProblem: not a valid Android App Bundle, missing %s" % ", ".join(missing))
            return 1
        print("App Bundle structure: OK (BundleConfig.pb, base/manifest/AndroidManifest.xml present)")
    elif pkg.endswith(".apk"):
        if "AndroidManifest.xml" not in names:
            print("16 KB PAGE SIZE CHECK: FAIL\nProblem: not a valid APK (no AndroidManifest.xml)")
            return 1

    rep = Report(args.blame_dir)
    scan_zip_members(rep, zf)

    if rep.checked == 0:
        print("16 KB PAGE SIZE CHECK: FAIL\nProblem: no native ELF libraries were found in the package "
              "(a Kivy app must contain libSDL2.so, libmain.so, ...). Refusing to pass an empty check.")
        return 1

    print("")
    print("Libraries checked: %d" % rep.checked)
    if rep.failures:
        print("16 KB PAGE SIZE CHECK: FAIL")
        for label, problem, min_align in rep.failures:
            print("Library: %s" % label)
            print("Problem: %s" % problem)
            print("Detected alignment: 0x%x (%d bytes)" % (min_align, min_align))
            print("Required alignment: 0x%x (%d bytes)" % (REQUIRED, REQUIRED))
            hits = rep.blame(label.split("!/")[-1])
            if hits:
                print("Built by (matching files under %s):" % args.blame_dir)
                for h in hits:
                    print("    " + h)
        return 1
    print("16 KB PAGE SIZE CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
