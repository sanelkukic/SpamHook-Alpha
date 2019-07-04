import time
from time import sleep
import json
import os, sys, shutil
import urllib
from urllib import request

global totalSent
interactive_mode = not len(sys.argv) > 1

def wait_for_response():
    input("Press ENTER to continue...")

def check_py():
    verMgr = sys.version_info
    mjrVr = str(verMgr.major)
    minVr = str(verMgr.minor)
    micVr = str(verMgr.micro)
    verOut = "You are using Python version: " + mjrVr + "." + minVr + "." + micVr + "."
    correctVer = "You are using a compatible Python version. " + verOut
    incorrectVer = "You are not using a compatible Python version. " + verOut
    try:
        assert sys.version_info >= (3, 5)
    except AssertionError:
        print(incorrectVer)
    else:
        print(correctVer)
    if interactive_mode:
        wait_for_response()
        main_menu()
    else:
        leave_spamhook()

def make_empty():
    try:
        data = {}
        print("Failed to find existing spamhook.json file - creating new empty file...")
        with open("spamhook.json", "w") as f:
            json.dump(data, f)
            time.sleep(10) # give it time to save the data
    except Exception as tempFileException:
        raise RuntimeError("Failed to create empty spamhook.json:"+tempFileException)
    else:
        pass

def check_file():
    try:
        checkFile = os.access("./spamhook.json", os.F_OK)
    except Exception as missingFileException:
        print("Error checking for spamhook.json file, attempting to make new one...")
        make_empty()
    else:
        if checkFile == True:
            print("Loaded spamhook.json file!")
        elif checkFile == False:
            make_empty()
        else:
            print("Error checking for spamhook.json file")
            make_empty()

def spamhook_settings_file():
    try:
        checkSettings = os.access("./app-settings.json", os.F_OK)
    except Exception as settingsError:
        raise Exception("Error: " + str(settingsError))
    else:
        if checkSettings == True:
            print("Loaded app-settings.json file!")
        elif checkSettings == False:
            print("Failed to find app-settings.json file, creating empty one...")
            try:
                data = {}
                with open("app-settings.json", "w") as f:
                    json.dump(data, f)
                    time.sleep(10)
            except Exception as otherSettingsError:
                raise Exception("Error: " + otherSettingsError)
            else:
                print("Done!")

check_file()
spamhook_settings_file()

def install_reqs():
    wipe_screen()
    print("Installing missing modules...")
    try:
        import pip
    except ImportError:
        raise ImportError("While trying to auto-install missing modules, an error was encountered: You do not have pip on your Python installation.")
    except Exception as loadingPipException:
        raise Exception(loadingPipException)
    else:
        try:
            os.system("pip3 install -r requirements.txt")
        except Exception as installationException:
            raise Exception(installationException)
        else:
            print("Installed missing modules!")

def spamhook_settings():
    with open("app-settings.json") as g:
        return json.load(g)

spam_set = spamhook_settings()

def discord_warning():
    print("WARNING: Usage of this tool can get you reported by someone to Discord Staff, which could lead to your Discord account getting deleted.")
    print("If you are OK with this, enter \"yes\" in the field below, otherwise enter \"no\" in the field below.\n")
    proceed = input(">>> ")
    if proceed == "yes":
        accepted = "yes"
    elif proceed == "no":
        accepted = "no"
    else:
        print("Invalid option.")

    theData = {
        "accepted_agreement": accepted
    }
    try:
        with open("app-settings.json", "w") as h:
            json.dump(theData, h)
            time.sleep(10)
    except Exception as dbSaveError:
        raise Exception("Error: " + dbSaveError)
    else:
        print("Saved!")

def db_checker():
    try:
        if spam_set["accepted_agreement"] == "yes":
            return True
        else:
            return False
    except Exception:
        return False
    else:
        return False

check_agreed = db_checker()

def final_checker():
    if check_agreed == True:
        pass
    else:
        discord_warning()

def spam_hook():
    with open("spamhook.json") as f:
        return json.load(f)

spam_db = spam_hook()

try:
    import requests
except ImportError:
    install_reqs()
import webbrowser

import argparse
from argparse import ArgumentParser

def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="SpamHook - A trolling tool that spams a Discord webhook with a customizable message.")
    parser.add_argument("--spam", "-s", action="store_true", help="Go directly to the Spamming screen.")
    parser.add_argument("--make-file", "-make", action="store_true", help="Create the spamhook.json file used to store information about the webhook you're spamming.")
    parser.add_argument("--wipe-file", "-wipe", action="store_true", help="Wipe all contents of your spamhook.json file - does NOT delete it. This is irreversable.")
    parser.add_argument("--delete-file", "-del", action="store_true", help="DELETE your spamhook.json file. This is irreversable.")
    parser.add_argument("--github", "-gh", action="store_true", help="Opens the SpamHook GitHub repository.")
    parser.add_argument("--legacy", "-l", action="store_true", help="Launch the legacy (v1) version of SpamHook.")
    parser.add_argument("--make-empty", "-empty", action="store_true", help="Make an empty spamhook.json file")
    parser.add_argument("--view-file", "-view", action="store_true", help="View your current SpamHook settings.")
    parser.add_argument("--join-discord", "-discord", action="store_true", help="Join xDrixxyz's Discord server")
    parser.add_argument("--app-info", "-inf", action="store_true", help="Shows information about SpamHook.")
    parser.add_argument("--delete-settings", "-delset", action="store_true", help="Delete your app-settings.json file.")
    parser.add_argument("--cleanup", "-cl", action="store_true", help="Wipe and delete your app-settings.json and spamhook.json files.")
    parser.add_argument("--py-check", "-py", action="store_true", help="Check if your Python version is compatible with SpamHook.")

    return parser.parse_args()

def wipe_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

try:
    input = raw_input
except:
    pass

theVersion = "2.0-r1"
intro = ("SpamHook v"+theVersion+" Alpha\n"
         "Made by xDrixxyz\n"
         "---------------------------------------")

def spam_this_webhook():
    wipe_screen()
    print(intro)
    print("Tip: Press CTRL+C to exit spam mode.\n")
    whUrl = spam_db["url"]
    msg = spam_db["message"]
    use_tts = spam_db["use_tts"]
    custom_username = spam_db["username"]
    custom_avatar = spam_db["avy_url"]
    times_to_spam = spam_db["times_to_spam"]
    spamThis = True
    payload = {
        "content": msg,
        "tts": use_tts,
        "username": custom_username,
        "avatar_url": custom_avatar
    }
    if custom_username == "null":
        del(payload["username"])
        if custom_avatar == "null":
            del(payload["avatar_url"])
        else:
            pass
    elif custom_avatar == "null":
        del(payload["avatar_url"])
        if custom_username == "null":
            del(payload["username"])
        else:
            pass
    else:
        pass
    spamCounter = 0
    if times_to_spam == "none":
        spamThis = True
    else:
        pass

    if times_to_spam == "none":
        pass
    else:
        numToSpam = int(times_to_spam)

    totalSent = 0

    if times_to_spam == "none":
        while spamThis is True:
            r = requests.post(whUrl, data=payload)
            time.sleep(1) # to prevent rate limiting
            spamCounter += 1
            totalSent += 1
            resultsCode = str(r.status_code)
            resultsReason = str(r.reason)
            currentNumber = str(spamCounter)
            print("Executed, results: " + resultsCode + " | " + resultsReason + " - this is post number "+currentNumber+" out of infinity")
        print("Stopping webhook spam, successfully sent a total of "+str(totalSent)+" spam messages")
    else:
        while spamCounter < numToSpam:
            r = requests.post(whUrl, data=payload)
            time.sleep(1)
            spamCounter += 1
            totalSent += 1
            resultsCode = str(r.status_code)
            resultsReason = str(r.reason)
            currentNumber = str(spamCounter)
            print("Executed, results: " + resultsCode + " | " + resultsReason + " - this is post number "+currentNumber+" out of "+times_to_spam)
        print("Stopping webhook spam, successfully sent a total of "+str(totalSent)+" spam messages")
    if interactive_mode:
        wait_for_response()
        main_menu()
    else:
        leave_spamhook()

def make_spamhook_file():
    wipe_screen()
    print(intro)
    print("Please enter the URL of the webhook to spam")
    whUrl = input(">>> ")
    print("Please enter message to spam")
    msg = input(">>> ")
    print("Do you want to use TTS (text-to-speech) to read spammed messages out loud? (yes/no)")
    use_tts = input(">>> ")
    if use_tts == "yes":
        ttsChoice = "true"
    elif use_tts == "no":
        ttsChoice = "false"
    else:
        ttsChoice = "false"
    print("Do you want to set a custom username for your webhook (yes/no)")
    use_username = input(">>> ")
    if use_username == "yes":
        customUsername = input("Enter a custom username: >>> ")
        pass
    elif use_username == "no":
        customUsername = "null"
    else:
        customUsername = "null"
    print("Do you want to use a custom avatar URL for your webhook? (yes/no)")
    use_avatar = input(">>> ")
    if use_avatar == "yes":
        avy = input("Enter URL to avatar to use: >>> ")
        pass
    elif use_avatar == "no":
        avy = "null"
    else:
        avy = "null"
    print("Enter the amount of times to spam the webhook. Enter \"none\" for infinity.")
    timesToSpam = input(">>> ")
    data = {
        "url": whUrl,
        "message": msg,
        "use_tts": ttsChoice,
        "username": customUsername,
        "avy_url": avy,
        "times_to_spam": timesToSpam
    }
    with open("spamhook.json", "w") as f:
        json.dump(data, f)
        time.sleep(10) # lots of time given to save this json file
        print("Done.") # let the user know when its done and return to the main menu
        print("WARNING: You might need to restart SpamHook for the changes to propagate!")
        time.sleep(3) # give people time to read the warning
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def wipe_spamhook_file():
    wipe_screen()
    print(intro)
    print("Wiping spamhook.json file...")
    data = {}
    with open("spamhook.json", "w") as f:
        json.dump(data, f)
        time.sleep(10) # same as above
        print("Done.")
        print("WARNING: You might need to restart SpamHook for the changes to propagate!")
        time.sleep(3) # give people time to read the warning
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def leave_spamhook():
    print("Exiting...")
    sys.exit(0)

def open_gh():
    wipe_screen()
    print("Opening GitHub repository...")
    webbrowser.open("https://github.com/xDrixxyz/SpamHook-Alpha")
    if interactive_mode:
        wait_for_response()
        misc_menu()
    else:
        leave_spamhook()

def cleanup_spamhook():
    wipe_screen()
    print(intro)
    print("Deleting app-settings.json file...")
    try:
        os.remove("./app-settings.json")
    except Exception as cleanupError:
        raise Exception("Error: " + cleanupError)
    else:
        print("Done!")
    print("Deleting spamhook.json file...")
    try:
        os.remove("./spamhook.json")
    except Exception as cleanupException:
        raise Exception("Error: " + cleanupException)
    else:
        print("Done!")
        print("WARNING: You might need to restart SpamHook for the changes to take effect.")
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def settings_remover():
    wipe_screen()
    print(intro)
    print("Deleting app-settings.json file...")
    try:
        os.remove("./app-settings.json")
    except Exception as settingsDeletionError:
        raise Exception("Error: " + settingsDeletionError)
    else:
        print("Done!")
        print("WARNING: You might need to restart SpamHook for the changes to take effect!")
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def spamhook_old():
    wipe_screen()
    print(intro)
    whUrl = input("Webhook URL to spam: ")
    msg = input("Message to spam: ")
    payload = {
        "content": msg,
        "tts": "true"
    }
    legacyHook = True
    while legacyHook is True:
        try:
            r = requests.post(whUrl, data=payload)
        except Exception as legacyException:
            print("Error executing webhook: " + legacyException)
            wait_for_response()
            main_menu()
        else:
            print("Executed webhook!")
    print("Stopping webhook spam...")
    if interactive_mode:
        wait_for_response()
        main_menu()
    else:
        leave_spamhook()

def delete_spamhook_file():
    wipe_screen()
    print("Deleting spamhook.json file...")
    try:
        os.remove("spamhook.json")
        time.sleep(10) # let the program realize what just happened
    except Exception as removalException:
        raise Exception("Error deleting spamhook.json file: " + removalException)
    else:
        print("Deleted!")
        print("WARNING: You might need to restart SpamHook for the changes to propagate!")
        time.sleep(3) # give people time to read the warning
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def view_settings():
    wipe_screen()
    print("Reading spamhook.json file...")
    try:
        theUrl = spam_db["url"]
        theMsg = spam_db["message"]
        theAvy = spam_db["avy_url"]
        theUn = spam_db["username"]
        theTts = spam_db["use_tts"]
        acceptedAgreement = spam_set["accepted_agreement"]
    except KeyError:
        print("Your spamhook.json file is empty/missing a field.")
        wait_for_response()
        sys.exit(1)
    except Exception as printFileException:
        print("Error: " + printFileException)
    else:
        pass
    print("Current Settings in spamhook.json file: \n")
    print("Webhook URL: " + theUrl + "\n")
    print("Message to spam: " + theMsg + "\n")
    print("Custom Avatar URL: " + theAvy + "\n")
    print("Custom Username: " + theUn + "\n")
    print("Use TTS? " + theTts + "\n")
    print("Accepted agreement? " + acceptedAgreement + "\n")
    if interactive_mode:
        wait_for_response()
        main_menu()
    else:
        leave_spamhook()

def join_hexcord():
    wipe_screen()
    print("Loading...")
    try:
        webbrowser.open("https://xdrixxyz.eu.org/gw?dest=discord")
    except Exception as hexcordException:
        print("Error: " + hexcordException)
    else:
        print("Done!")
        if interactive_mode:
            wait_for_response()
            misc_menu()
        else:
            leave_spamhook()

def spamhook_info():
    wipe_screen()
    print(intro)
    print("SpamHook Information")
    print("--------------------")
    print("Version: " + theVersion + "\n")
    print("Developer: xDrixxyz\n")
    print("GitHub: https://github.com/xDrixxyz/SpamHook-Alpha\n")
    print("""
Credits:

- xDrixxyz: Program Development
- xDrixxyz: Program Icon
- StackOverflow: every dev's go to place for coding questions
- Discord\n
""")
    print("WARNING: Usage of this tool can get you reported by someone to Discord Staff, which could lead to your Discord account getting deleted. Use this with caution.\n")

    if interactive_mode:
        wait_for_response()
        misc_menu()
    else:
        leave_spamhook()

def wipe_settings():
    wipePayload = {}
    try:
        with open("app-settings.json", "w") as k:
            json.dump(wipePayload, k)
            time.sleep(10)
    except Exception as settingsDeleterError:
        raise Exception("Error: " + settingsDeleterError)
    else:
        print("Done!")
    if interactive_mode:
        wait_for_response()
        leave_spamhook()
    else:
        leave_spamhook()

def file_manager_menu():
    wipe_screen()
    print(intro)
    print("File Manager")
    print("------------")
    print("<1> Create spamhook.json file")
    print("<2> Create EMPTY spamhook.json file")
    print("<3> Wipe contents of spamhook.json file")
    print("<4> Delete spamhook.json file")
    print("<5> Delete app-settings.json file")
    print("<6> Wipe app-settings.json file")
    print("<7> Cleanup (deletes both spamhook.json and app-settings.json files)\m")
    print("\n<0> Back to main menu\n")
    choice = input(">>> ")
    if choice == "1":
        make_spamhook_file()
    elif choice == "2":
        make_empty()
    elif choice == "3":
        wipe_spamhook_file()
    elif choice == "4":
        delete_spamhook_file()
    elif choice == "5":
        settings_remover()
    elif choice == "6":
        wipe_settings()
    elif choice == "7":
        cleanup_spamhook()
    elif choice == "0":
        main_menu()
    else:
        print("Invalid choice.")

def misc_menu():
    wipe_screen()
    print(intro)
    print("Miscellaneous Menu")
    print("------------------")
    print("<1> View SpamHook statistics")
    print("<2> Run Python version check")
    print("<3> View SpamHook GitHub repository")
    print("<4> Join xDrixxyz's Discord server")
    print("\n<0> Back to main menu\n")
    option = input(">>> ")
    if option == "1":
        spamhook_info()
    elif option == "2":
        check_py()
    elif option == "3":
        open_gh()
    elif option == "4":
        join_hexcord()
    elif option == "0":
        main_menu()
    else:
        print("Invalid choice.")

def main_menu():
    wipe_screen()
    print(intro)
    print("WARNING: Usage of this tool can get you reported by someone to Discord Staff, which could lead to your Discord account getting deleted.\n")
    print("\nMain Menu")
    print("---------")
    print("""
<1> Spam a webhook (requires a non-empty spamhook.json file, which you can generate using option 2)

<2> View your SpamHook settings

<3> File management (delete spamhook.json, wipe spamhook.json, cleanup SpamHook, etc)
<4> Miscellaneous (view GitHub repository, join xDrixxyz's Discord, etc)

<5> Use legacy SpamHook (SpamHook v1.0)

<0> Exit
""")
    menu_choice = input(">>> ")
    if menu_choice == "1":
        spam_this_webhook()
    elif menu_choice == "2":
        view_settings()
    elif menu_choice == "3":
        file_manager_menu()
    elif menu_choice == "4":
        misc_menu()
    elif menu_choice == "5":
        spamhook_old()
    elif menu_choice == "0":
        leave_spamhook()
    else:
        print("Invalid menu option.")

args = parse_cli_arguments()

def boot_hook():
    final_checker()
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)
    wipe_screen()
    verManager = sys.version_info
    strMajor = str(verManager.major)
    strMinor = str(verManager.minor)
    strMicro = str(verManager.micro)
    finalOutput = "Your Python version is: " + strMajor + "." + strMinor + "." + strMicro + "."
    print("Loading SpamHook...")
    print("Checking Python version...")
    try:
        assert sys.version_info >= (3, 5)
    except AssertionError:
        raise AssertionError("Ew, you're not on Python 3.5 or newer. Get Python 3.5 or newer and then try to run this script. " + finalOutput)
    else:
        print("Python version check PASS! " + finalOutput)
        print("Loading...")
        print("Checking command line arguments...")
        if interactive_mode:
            main_menu()
        else:
            if args.spam:
                spam_this_webhook()
            elif args.make_file:
                make_spamhook_file()
            elif args.wipe_file:
                wipe_spamhook_file()
            elif args.delete_file:
                delete_spamhook_file()
            elif args.github:
                open_gh()
            elif args.legacy:
                spamhook_old()
            elif args.view_file:
                view_settings()
            elif args.make_empty:
                make_empty_spamhook_file()
            elif args.join_discord:
                join_hexcord()
            elif args.make_empty:
                make_empty()
            elif args.app_info:
                spamhook_info()
            elif args.cleanup:
                cleanup_spamhook()
            elif args.delete_settings:
                settings_remover()
            elif args.py_check:
                check_py()

if __name__ == '__main__':
    check_file()
    spamhook_settings_file()
    boot_hook()
