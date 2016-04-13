#!/usr/bin/env python
# coding: utf8

import socket
import random
import os

def include(filename):
    if os.path.exists(filename): 
        execfile(filename)

# TODO: externalize fuzzing functions
#include('fuzz_functions.py')

def create_response():
    response = ""
    num_tags = random.randint(1,10)
    for x in range (1,num_tags):
        tag = get_tag()
        if (tag == "u"):
            value = get_fuzzy_url()
        elif (tag == "n"):
            if (random.randint(1,3) != 3):
                value = str(get_fuzzy_num())
            else:
                value = get_fuzzy_str()
        else:
            value = get_fuzzy_str()
        response += tag + get_delimiter() + value
        if (x < num_tags-1):
            response += "\n"
    return response

def get_fuzzy_int():
    exp = random.randint(1,32)
    return random.randint(0,2**exp)+1
    
def get_fuzzy_float():
    a = str(get_fuzzy_int())
    b = str(get_fuzzy_int());
    return float(a + "." + b)

def get_fuzzy_double():
    x = random.randint(1,3)
    if (x == 1):
        y = -1
    else:
        y = 1
    return get_fuzzy_float() * y

def get_fuzzy_num():
    x = random.randint(1,3)
    if (x == 1):
        n = get_fuzzy_int()
    elif (x == 2):
        n = get_fuzzy_float()
    else:
        n = get_fuzzy_double()
    return n

def get_fuzzy_str_ascii():
    len = random.randint(1,30)
    str = ''
    for x in range (1,len):
        str += chr (random.randint(31,126))
    return str

def get_fuzzy_str_unicode():
    len = random.randint(1,30)
    str = ''
    for x in range (1,len):
        str += unichr (random.randint(0,65535))
    return str


def get_fuzzy_str():
    x = random.randint(1,2)
    if (x == 1):
        str = get_fuzzy_str_ascii()
    else:
        str = get_fuzzy_str_unicode()
    #return str
    return get_fuzzy_str_ascii()


def get_fuzzy_url():
    # tokens and ports
    # is_legit = .com
    host = ''
    port = ''
    num_tokens = random.randint(1,4)
    for i in range (0,num_tokens):
        host += get_fuzzy_str() + "."
    if (random.randint(1,2) == 1):
        host += get_fuzzy_str()
    else:
        host += "com"
    if (random.randint(1,2) == 1):
        port = ":" + str(get_fuzzy_int())
    return host + port

def get_tag():
    tags = ['n','i','u', 'a', 's', 'd', 'ad', 'sd']
    tags.append (get_fuzzy_str())
    # unicode???
    i = random.randint(1,len(tags)) - 1
    return tags[i]

def get_delimiter():
    return ":"


def run():
    r'''Main loop'''

    # Create TCP socket listening on 13000 port for all connections, 
    # with connection queue of length 1
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, \
                                socket.IPPROTO_TCP)
    server_sock.bind(('127.0.0.1', 13000))
    server_sock.listen(1)

    while True:
        # accept connection
        client_sock, client_addr = server_sock.accept()
        response_body_raw = create_response()
        print "\nSHAVAR RESPONSE:\n"
        print response_body_raw + "\n"

        response_headers = {
            'Content-Type': 'text/plain; charset=us-ascii',
            'Content-Length': len(response_body_raw),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.iteritems())

        # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK' # this could be randomized


        # sending all this stuff
        client_sock.send('%s %s %s' % (response_proto, response_status, response_status_text))
        client_sock.send('\n') # to separate headers from body

        client_sock.send(response_headers_raw)
        client_sock.send('\n') # to separate headers from body
        temp = response_body_raw.decode ("utf-8", "ignore")

        client_sock.send(temp)
        client_sock.close()

run()