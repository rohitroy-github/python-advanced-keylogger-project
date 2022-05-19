# Program for generating an encryption key 

# importing cryptography library  
from cryptography.fernet import Fernet

# variable to generate key 
key = Fernet.generate_key()

# file where the encryption key can be pasted 
file = open("encryption_key.txt", 'wb')

file.write(key)
file.close()


# Important Step : 
# run this program once 
# copy the encryption key from "encryption_key.txt"
# paste it into "key" variable (declaration) in "keylogger.py" 
