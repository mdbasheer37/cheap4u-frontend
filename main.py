"""
Entry point required by python-for-android / Buildozer.

The Android (SDL2) bootstrap that python-for-android builds always looks
for and executes a file literally named `main.py` at the root of
`source.dir`. The app's real code lives in Cheap4u.py (DashboardApp),
so this file just imports and runs it.

Do not rename or remove this file - without it the build either fails
or produces an APK that crashes immediately on launch because p4a
cannot find an entry script.
"""

# ── Wake the (free-tier) server while the app is still loading ───────────────
# Render's free plan puts the backend to sleep after ~15 idle minutes, and the
# first request afterwards can take 30-60 s. That is what made History and the
# first screens feel slow. Pinging /health from a background thread right now
# lets the server boot WHILE Python/Kivy are still importing and building the
# UI, instead of only after the splash screen. Failures are ignored.
import threading as _threading


def _early_backend_wakeup():
    try:
        import requests as _requests
        _requests.get("https://cheap4u-backend.onrender.com/health", timeout=70)
    except Exception:
        pass


_threading.Thread(target=_early_backend_wakeup, daemon=True).start()

from Cheap4u import DashboardApp

if __name__ == "__main__":
    DashboardApp().run()
