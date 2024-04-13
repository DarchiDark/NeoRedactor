import customtkinter as ctk
from PIL import Image, ImageTk
from mcrcon import MCRcon
import os
import paramiko
import threading
import time
import configparser
from os import path

#Vars
root = ctk.CTk()
config = configparser.RawConfigParser()
configreader = configparser.RawConfigParser()
configreader.read('config.ini')  # Read the config file

# Load background image for MainMenu
bg = Image.open('BackGround.png')
bg_resized = bg.resize((1280, 720))
bg_ctk = ImageTk.PhotoImage(bg_resized)

bg_console = Image.open('ConsoleBackGround.png')
bg_console_resized = bg_console.resize((1280, 720))
bg_console_ctk = ImageTk.PhotoImage(bg_console_resized)

bg_settings = Image.open('SettingsBackGround.png')
bg_settings = bg_settings.resize((1280, 720))
bg_settings = ImageTk.PhotoImage(bg_settings)

# Get host and port from the config
host = configreader.get('console', 'ipsftp')
port = configreader.getint('console', 'portmcrcon')
# Create Config if does not Exists
if(path.exists("config.ini") == False):
        config.add_section('console')
        config.set('console', 'linetxt', "Command Line /")
        config.set('console', 'ipsftp', "127.0.0.1")
        config.set('console', 'portsftp', "2222")
        config.set('console', 'usersftp', "DefaultUser")
        config.set('console', 'passwordsftp', "DefaultPassword")
        config.set('console', 'passwordmcrcon', "DefaultPassword")
        config.set('console', 'portmcrcon', "25566")
        with open('./config.ini', 'w') as f:
            config.write(f)

# Declare global variables
ConsoleInput = None

def send_rcon_command():
    mcr = MCRcon(host, configreader.get('console', 'passwordmcrcon'), port)
    mcr.connect()
    command = mcr.command(ConsoleInput.get())
    mcr.disconnect()

def sendRcon(event=None):
    t = threading.Thread(target=send_rcon_command)
    t.start()

def fetch_file_contents():
    file_path = '/logs/latest.log'
    file_name = os.path.basename(file_path)
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=configreader.get('console', 'ipsftp'), port=configreader.getint('console', 'portsftp'), username=configreader.get('console', 'usersftp'), password=configreader.get('console', 'passwordsftp'))
    
    sftp = ssh.open_sftp()
    sftp.get(file_path, file_name)
    
    with open(file_name, 'r', encoding='utf-8') as f:
        file_contents = f.read()
    
    if len(file_contents) > len(text_widget.get("1.0", "end")):
        lines = file_contents.split('\n')
        formatted_lines = []
        for line in lines:            
            formatted_lines.append(line)
        text_widget.delete('1.0', 'end')
        truncated_lines = [line in file_contents]
        truncated_lines = truncated_lines[:50]
        for line in formatted_lines[::-1]:
            text_widget.insert('end', line + '\n')
    
    sftp.close()
    ssh.close()

def consoleUpdater():
    while True:
        fetch_file_contents()
        time.sleep(0.1)  # Interval for updating, here it's set to 5 seconds

root.bind("<Return>", sendRcon)

def consoleElements():
    global ConsoleInput
    BackGround.place_forget()  
    ServerSetFrame.place_forget()  
    ConsoleButton.place_forget()
    FTPButton.place_forget()  
    SettingsButton.place_forget()  
    BackGroundC.place(x=0, y=0)
    ConsoleTxt = config.read('config.ini')
    ConsoleTxt = config.get('console', 'linetxt')
    ConsoleInput = ctk.CTkEntry(root, placeholder_text=ConsoleTxt, height=5, width=1180)
    ConsoleInput.place(x=5, y=690)
    ConsoleSendButton.place(x=1192, y=687)
    update_thread = threading.Thread(target=consoleUpdater)
    update_thread.daemon = True
    update_thread.start()
    text_widget.place(x=10, y=35)
    BackToMain.place(x=5, y=5)

def settingsElements():
    BackGround.place_forget()  
    ServerSetFrame.place_forget()  
    ConsoleButton.place_forget()
    FTPButton.place_forget()  
    SettingsButton.place_forget()  
    CommandLineTXT.place(x=30, y=30)
    CommandLineEntry.place(x=330, y=30)
    BackGroundS.place(x=0, y=0)
    SaveButton.place(x=1100, y=650)
    SFtpIpTXT.place(x=30, y=50)
    SFtpIpEntry.place(x=330, y=50)
    SFtpPortTXT.place(x=30, y=70)
    SFtpPortEntry.place(x=330, y=70)
    SFtpUserTXT.place(x=30, y=90)
    SFtpUserEntry.place(x=330, y=90)
    SFtpPasswordTXT.place(x=30, y=110)
    SFtpPasswordEntry.place(x=330, y=110)
    McRCONPortTXT.place(x=30, y=130)
    McRCONPortEntry.place(x=330, y=130)
    McRCONPasswordTXT.place(x=30, y=150)
    McRCONPasswordEntry.place(x=330, y=150)
root.iconbitmap('D:\ServerModifer\icon.ico')
root.resizable(0, 0)
root.title('Neo Redactor')
root.geometry("1280x720")

def saveAndBack():
    if path.exists('config.ini'):
        config.read('config.ini')
        config.set('console', 'linetxt', CommandLineEntry.get())
        config.set('console', 'ipsftp', SFtpIpEntry.get())
        config.set('console', 'portsftp', SFtpPortEntry.get())
        config.set('console', 'usersftp', SFtpUserEntry.get())
        config.set('console', 'passwordsftp', SFtpPasswordEntry.get())
        config.set('console', 'passwordmcrcon', McRCONPasswordEntry.get())
        config.set('console', 'portmcrcon', McRCONPortEntry.get())
        with open('./config.ini', 'w') as f:
            config.write(f)
    else:
        print("ERROR: NO CONFIG!")
    CommandLineTXT.place_forget()
    CommandLineEntry.place_forget()
    BackGroundS.place_forget()
    SaveButton.place_forget()
    SFtpIpTXT.place_forget()
    SFtpIpEntry.place_forget()
    SFtpPortTXT.place_forget()
    SFtpPortEntry.place_forget()
    SFtpUserTXT.place_forget()
    SFtpUserEntry.place_forget()
    SFtpPasswordTXT.place_forget()
    SFtpPasswordEntry.place_forget()
    McRCONPortTXT.place_forget()
    McRCONPortEntry.place_forget()
    McRCONPasswordTXT.place_forget()
    McRCONPasswordEntry.place_forget()
    BackGround.place(x=0, y=0)
    ServerSetFrame.place(x=0, y=670)
    ConsoleButton.place(x=400, y=678)
    SettingsButton.place(x=710, y=678)

def goToMain(): 
    global ConsoleInput
    BackGroundC.place_forget()
    ConsoleSendButton.place_forget()
    text_widget.place_forget()
    BackToMain.place_forget()
    if ConsoleInput:
        ConsoleInput.place_forget()
    BackGround.place(x=0, y=0)
    ServerSetFrame.place(x=0, y=670)
    ConsoleButton.place(x=400, y=678)
    SettingsButton.place(x=710, y=678)

#MainMenu
BackGround = ctk.CTkLabel(root, text='', image=bg_ctk, width=5, height=5)
BackGround.place(x=0, y=0)
ServerSetFrame = ctk.CTkFrame(root, width=1280, height=50, border_color='#9200ed',fg_color='#2e014a', border_width=5)
ServerSetFrame.place(x=0, y=670)
ConsoleButton = ctk.CTkButton(root, width=150, height=30, text="Console", text_color="#5e0099",font=("Pobeda", 25), fg_color="#9500f2", hover_color="#8100d1", command=consoleElements)
ConsoleButton.place(x=400, y=678)
FTPButton = ctk.CTkButton(root, width=150, height=30, text="FTP", text_color="#5e0099",font=("Pobeda", 25), fg_color="#9500f2", hover_color="#8100d1")
SettingsButton = ctk.CTkButton(root, width=150, height=30, text="Settings", text_color="#5e0099",font=("Pobeda", 25), fg_color="#9500f2", hover_color="#8100d1", command=settingsElements)
SettingsButton.place(x=710, y=678)

#ConsoleMenu
BackGroundC = ctk.CTkLabel(root, text='', image=bg_console_ctk, width=5, height=5)
ConsoleSendButton = ctk.CTkButton(root, width=10, height=5, text="Отправить", text_color="#5e0099",font=("Pobeda", 20), fg_color="#9500f2", hover_color="#8100d1", command=sendRcon)
text_widget = ctk.CTkTextbox(root, width=1260, height=640)
BackToMain = ctk.CTkButton(root, fg_color="#710de0", hover_color="#690ec9", text="Back", text_color="#3d067a",font=("Berlin Sans FB Demi", 20), command=goToMain)

#Settings
BackGroundS = ctk.CTkLabel(root, text='',image=bg_settings)
CommandLineTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Text On Command Line: ', text_color="black", font=("Berlin Sans FB Demi", 20))
CommandLineEntry = ctk.CTkEntry(root, placeholder_text="Command line /", bg_color="#7D10F7")
SFtpIpTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Ip to Connect to SFTP: ', text_color="black", font=("Berlin Sans FB Demi", 20))
SFtpIpEntry = ctk.CTkEntry(root, placeholder_text="127.0.0.1", bg_color="#7D10F7")
SFtpPortTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Port to Connect to SFTP: ', text_color="black", font=("Berlin Sans FB Demi", 20))
SFtpPortEntry = ctk.CTkEntry(root, placeholder_text="2222", bg_color="#7D10F7")
SFtpUserTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='User to Connect to SFTP: ', text_color="black", font=("Berlin Sans FB Demi", 20))
SFtpUserEntry = ctk.CTkEntry(root, placeholder_text="VasyaPupkin", bg_color="#7D10F7")
SFtpPasswordTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Password to Connect to SFTP: ', text_color="black", font=("Berlin Sans FB Demi", 20))
SFtpPasswordEntry = ctk.CTkEntry(root, placeholder_text="SuperSecretPassword", bg_color="#7D10F7")
McRCONPasswordTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Password to Connect to MCRcon: ', text_color="black", font=("Berlin Sans FB Demi", 20))
McRCONPasswordEntry = ctk.CTkEntry(root, placeholder_text="SuperSecretPassword", bg_color="#7D10F7")
McRCONPortTXT = ctk.CTkLabel(root, fg_color="#7D10F7", width=200, height=10, text='Port to Connect to MCRcon: ', text_color="black", font=("Berlin Sans FB Demi", 20))
McRCONPortEntry = ctk.CTkEntry(root, placeholder_text="25566", bg_color="#7D10F7")
SaveButton = ctk.CTkButton(root, fg_color="#710de0", hover_color="#690ec9", text="Save and Back", text_color="#3d067a",font=("Berlin Sans FB Demi", 20), command=saveAndBack)

root.mainloop()
