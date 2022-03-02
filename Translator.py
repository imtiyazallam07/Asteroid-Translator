import googletrans
from googletrans import Translator
from gtts import gTTS
import playsound 
import os
import platform
import time
import pyperclip
import colorama
import socket
from progress.bar import Bar
from progress.spinner import Spinner

def translate(frm="auto", to="english", text=None):
    translator = Translator()
    is_avi = True
    if not (lang_exists(frm) or frm == "auto"):
        print("Traceback (most recent call last):")
        print("\t<UnavailableLanguage> Language not found: " + to)
        is_avi = False
    if not (lang_exists(to)):
        print("Traceback (most recent call last):")
        print("\t<UnavailableLanguage> Language not found: " + frm)
        is_avi = False
    if(not is_avi):
        return "", ""
    if(text == None):
        text = input("Enter a text to translate: " + colorama.Fore.CYAN)
        print(colorama.Fore.RESET, end="")
    if(frm == 'auto'):
        translation = translator.translate(text, dest=googletrans.LANGCODES.get(to))
    else:
        translation = translator.translate(text, googletrans.LANGCODES.get(to), googletrans.LANGCODES.get(frm))
    return translation.text, translation.dest

def lang_exists(lang):
    return (googletrans.LANGCODES.get(lang) != None)

def main():
    if(platform.system() == 'Windows'):
        os.system('cls')
    else:
        os.system('clear')
    recent_lang = ""
    res = ""
    while True:
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT + "Asteroid-Translator",end="")
        print(colorama.Fore.MAGENTA + colorama.Style.BRIGHT + " in ", end="")
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + os.getlogin() + "@" + socket.gethostname(),end="")
        print(colorama.Fore.RESET + colorama.Style.BRIGHT + ":", end="")
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT + "~", end="")
        print(colorama.Fore.RESET + "$ ", end="")
        print(colorama.Fore.CYAN + colorama.Style.NORMAL, end="")
        command = input("")
        command = command.lower()
        print(colorama.Fore.RESET, end="")
        try:
            while command.index("  ") != -1:
                command.replace("  ", " ")
        except ValueError:
            pass
        keys = command.split(" ")
        if(keys[0] == "translate"):
            if(len(keys) == 2):
                res, recent_lang = translate(frm='english', to=keys[1])
            elif(len(keys) == 3):
                res, recent_lang = translate(frm=keys[1], to=keys[2])
            else:
                res, recent_lang = translate(frm='english', to='english')
            print(colorama.Fore.YELLOW + res + colorama.Fore.RESET)
        elif(keys[0] == 'exit'):
            if(len(keys) == 1):
                print(colorama.Fore.RED + "Clearing cache and exiting...")
                if(os.path.exists(".cache-translated.mp3")):
                    print(colorama.Fore.RESET + "Removing .cache-translated.mp3" )
                    progress_bar()
                    free()
                    print("\nRemoved .cache-translated.mp3")
                else:
                    print("No Cache found")
                print("Exiting...")
                time.sleep(1)
                print("goodbye")
                break
            else:
                print("\'exit\' command takes no arguments")
        elif (keys[0] == 'speak'):
            if(len(keys) == 1):
                save_file(True, res, recent_lang)
                playsound.playsound(".cache-translated.mp3")
            else:
                print("\'speak\' command takes no arguments")
        elif (keys[0] == 'copy'):
            if(len(keys) == 1):
                pyperclip.copy(res)
            else:
                print("\'copy\' command takes no arguments")
        elif (keys[0] == 'clear'):
            if(len(keys) == 1):
                if(platform.system() == 'Windows'):
                    os.system('cls')
                else:
                    os.system('clear')
            else:
                print("\'clear\' command takes no arguments")
        elif (keys[0] == 'save'):
            if(len(keys) == 1):
                save_file(False, res, recent_lang)
            else:
                print("\'save\' command takes no arguments")
        elif (keys[0] == 'clipboardtranslate'):
            txt = pyperclip.paste()
            if(len(keys) == 1):
                res, recent_lang = translate(frm='auto', to='english', text=txt)
                print(res)
            else:
                print("\'save\' command takes no arguments")
        elif (keys[0] == 'clean'):
            if(len(keys) == 1):
                free()
                res = ""
                recent_lang = ""
            else:
                print("\'clean\' command takes no arguments")
        elif (keys[0] == 'help' and len(keys) == 1):
            print(colorama.Fore.GREEN + "Asteroid-Translator Help")
            print("\tTranslate:")
            print("\t\tTranslates text from one language to another")
            print("\t\tUsage: translate [from language] [to language]")
            print("\t\tExample: translate english french")
            print("\t\t         translate [from]  [to]")
            print("\t\tExample: translate french")
            print("\t\t         translate [to]")
            print("\t\t         auto detects the language and translates to the given langauge")
            print("\t\tExample: translate")
            print("\t\t         auto detects the language and translates to english")
            print("\tExit:")
            print("\t\tExits the program")
            print("\t\tUsage: exit")
            print("\t\tExample: exit")
            print("\tSpeak:")
            print("\t\tSaves the translated text to a cached mp3 file and automatically plays it")
            print("\t\tUsage: speak")
            print("\t\tExample: speak")
            print("\tCopy:")
            print("\t\tCopies the translated text to the clipboard")
            print("\t\tUsage: copy")
            print("\t\tExample: copy")
            print("\tClear:")
            print("\t\tClears the terminal")
            print("\t\tUsage: clear")
            print("\t\tExample: clear")
            print("\tSave:")
            print("\t\tsaves the translated voice of last translation to a mp3 file")
            print("\t\tUsage: save")
            print("\t\tExample: save")
            print("\tClipboard Translate:")
            print("\t\tTranslates the text in the clipboard")
            print("\t\tUsage: clipboardtranslate")
            print("\t\tExample: clipboardtranslate")
            print("\tClean:")
            print("\t\tRemoves all files from the cache and resets the program")
            print("\t\tUsage: clean")
            print("\t\tExample: clean")
        else:
            print("Traceback (most recent call last):")
            print("\t<UnavailableCommand> Command not found:", keys[0])

def free():
    if(os.path.exists(".cache-translated.mp3")):
        os.remove(".cache-translated.mp3")

def progress_bar():
    bar = Bar('Deleting', max=100, suffix='%(percent)d%%', fill='#', empty='.')
    spinner = Spinner('Loading ')
    for i in range(0, 100):
        time.sleep(0.05)
        bar.next()

def save_file(a, res, recent_lang):
    t1 = gTTS(text=res, lang=recent_lang)
    if os.path.exists(".cache-translated.mp3"):
        os.remove(".cache-translated.mp3")
    if a:
        t1.save(".cache-translated.mp3")
    else:
        fl = str(time.time())+"-translated.mp3"
        t1.save(fl)
        print("Saved to:", os.getcwd() + "\\" + fl)

if __name__ == "__main__":
    main()