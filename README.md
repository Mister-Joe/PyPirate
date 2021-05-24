# PyPirate
A simple proof-of-concept ransomware written with Python

Note: PyPirate is not intended to be used on any device that you do not have permission to use.
Caution: PyPirate is tested and functioning on Python 3.7 and Windows 10. Please do not accidentally encrypt your files! 

PyPirate utilizes the AES encryption algorithm with 128 bit keys in CBC mode. Implementation of the AES is handled by the Fernet module of the cryptography package.

The keys are generated and stored on a remote server and sent to the client. The client then crawls every file in every directory on as many drive partitions as it can find, reading and encrypting files as it crawls. When the client has finished crawling and encrypting, it waits for decryption instructions from the remote server.
