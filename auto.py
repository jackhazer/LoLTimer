import subprocess
import time

def modify_clipboard_file(new_content):
    with open('LoLTimer.ahk', 'r+') as file:
        lines = file.readlines()
        lines[5] = 'send {enter}'+ new_content + '{enter}\n'  # Modify the content at the 3rd row
        file.seek(0)
        file.writelines(lines)
        file.truncate()

def run_ahk_script():
    ahk_script = "LoLTimer.ahk"
    ahk_exe = "C:/Program Files/AutoHotkey/v1.1.37.01/AutoHotkeyU64.exe"

    # Run the AHK script using AutoHotkey.exe
    subprocess.Popen([ahk_exe, ahk_script], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
