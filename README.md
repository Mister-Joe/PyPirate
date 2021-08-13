# PyPirate
A simple proof-of-concept ransomware written with Python.

**Caution:** PyPirate is tested and functioning on Python 3.7 and Windows 10. Please do not accidentally encrypt your files!

PyPirate utilizes AES with 128 bit keys in CBC mode. Implementation of AES is handled by the Fernet module of the cryptography package.

The keys are generated and stored on a remote server and sent to the client. The client then crawls every file in every directory on as many drive partitions as it can find, reading and encrypting files as it crawls. When the client has finished crawling and encrypting, it waits for decryption instructions from the remote server. 

**Note:** Not all of the functionality of the remote server has been completed as of yet.
