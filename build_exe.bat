@echo off
@title SpamHook - EXE builder
goto build

:build
echo Building SpamHook exe using PyInstaller...
pyinstaller --clean --log-level DEBUG --onefile --name SpamHook -i more_spam.ico --uac-admin --osx-bundle-identifier com.hexexpeck.spamhook.v SpamHook-v2.py