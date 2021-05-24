# PyPirate
A simple proof-of-concept ransomware written with Python

PyPirate utilizes the AES encryption algorithm with 128 bit keys in CBC mode. Implementation of the AES is handled by the Fernet module of the cryptography package. The keys are generated and stored on a remote server and sent to the PyPirate client. PyPirate then crawls every file in every directory on as many drive partitions as it can find, reading and encrypting files as it crawls. When PyPirate client has finished crawling and encrypting, it waits for decryption instructions from the remote server.
