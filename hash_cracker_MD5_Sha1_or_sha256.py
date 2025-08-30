# This script is created for educational purposes only.
# Unauthorized use or misuse of this code for malicious activities is strictly prohibited.

import hashlib
import pyfiglet

ascii_banner = pyfiglet.figlet_format("Anna's \nPython 4 Pentesters \nHASH CRACKER")
print(ascii_banner)

# Set the location of the wordlist file
wordlist_location = 'wordlist.txt'

# Ask for the hash and its type
hash_input = input('Enter hash to be cracked: ').strip()
hash_type = input('Enter hash type (md5 / sha1 / sha256): ').strip().lower()

# Function that selects the appropriate hashing function
def get_hash_function(htype):
    if htype == 'md5':
        return hashlib.md5
    elif htype == 'sha1':
        return hashlib.sha1
    elif htype == 'sha256':
        return hashlib.sha256
    else:
        print('Unsupported hash type. Use: md5, sha1, or sha256.')
        exit(1)

hash_function = get_hash_function(hash_type)

# Search through the wordlist
try:
    with open(wordlist_location, 'r') as file:
        for line in file:
            word = line.strip()
            hashed = hash_function(word.encode()).hexdigest()
            if hashed == hash_input:
                print(f'Found cleartext password! {word}')
                break
        else:
            print('Password not found in wordlist.')
except FileNotFoundError:
    print(f'Wordlist file "{wordlist_location}" not found.')
