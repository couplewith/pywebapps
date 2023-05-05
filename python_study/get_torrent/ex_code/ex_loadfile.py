
#import re
#import urllib.request
#import http.client
#import requests
#import sys

import os  # for checking file existence
import sys  # for handling errors

def read_file_into_list(filename):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' does not exist")
        return None

    try:

        with open(filename, 'r', encoding='utf-8') as file:
            #lines = file.readlines()
            lines = [line.strip() for line in file.readlines()]
            print (lines)

    except UnicodeDecodeError:
        print(f"Error: could not read file '{filename}' as UTF-8")
        return None

    return lines

file_name = '../torrent_sites.txt'
read_file_into_list(file_name)
