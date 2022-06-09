#Features of my advanced keylogger : 

1 > Capturing keystrokes & creating a text file. 

2 > Recording microphone data for a specific period of time.

3 > Acquring clipboard information & creating a text file. 

4 > Acquring system information & text file. 

5 > Capturing live screenshots during execution.

6 > Sending all these files over ot attacker's email address. 

7 > Encrypting keystrokes text file, clipboard information text file, system infomartion text file using Fernet encryption algorithm. 

8 > Decrypting the above whenever needed using the same decryption algorithm. 


#Steps to follow for successful execution of my keylogger. 

1 > execute the GenerateKey.py file and it will generate an encryption key 

2 > copy that key from the file and paste it into keyLogger.py and DecryptFiles.py at a specified location (mentioned in comments)

3 > set the sender email id and password and the receievr email id in the KeyLogger.py file (in specified locations, mentioned in comments)

5 > create a new folder "Saved Logs" and copy the folder path and paste it into the keylogger.py and DecryptFiles.py at specified location(in specified location as mentioned in comments)

6 > save all the files before final execution

5 > execute the KeyLogger.py program now 

6 > the preview of every keystroke will be visible at the output window of the execution and the message "email sent" will be provided once the email to get sent

7 > a copy of the encrypted files will be added to the "Saved Logs" folder in order to decrypt them, we have to run the DecryptFiles.py 

8 > a decrypted version of all the encrypted files will be saved in the same folder "Saved Logs" 


Reference video file is https://youtu.be/25um032xgrw
