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

from Cheap4u import DashboardApp

if __name__ == "__main__":
    DashboardApp().run()
