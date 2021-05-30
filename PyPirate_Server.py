from cryptography.fernet import Fernet
import socket
import string
import time


# functionality to send the stored key back to the client for decryption needs to be implemented

def listen(sock):

    message = None
    duplicate = False

    while 1:

        message = sock.recvfrom(4096)

        if message != None:

            print('Key request received from %s' % message[1][0])

            file = open('hosts.txt', 'r+') # ensure that you have already created the hosts.txt file
            hosts = file.readlines()

            for s in hosts:

                if message[0].decode() in s:
              
                    duplicate = True
                    print('Error: %s has already requested a key' % message[1][0])
                    break

            if duplicate == False:
            
                key = Fernet.generate_key()

                file.write(message[0].decode() + ' : ' + str(key) + '\n')

                sock.sendto(key, (message[1][0], message[1][1]))

            file.close()
   
        message = None
        duplicate = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
sock.bind((ip_address, 30000)) # change port as desired, though the client will need to be updated as well

listen(sock)
