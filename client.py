#!/usr/bin/python3

import socket
from save_data_stream import *

def data_process(input_string):
    """
    This is where all the processing happens.
    Let's just read the string backwards
    """
    target = input_string
    target.find('b')
    print("Processing input!")
    # return input_string[::-1] # test
    return input_string


def rec_data(conn, MAX_BUFFER_SIZE):
    """
    This increases the read capacity of a data packet from Server
    Return All data in one string - Ready to filter
    """
    import re
    all_data = ''

    while True:
        input_from_server_bytes = conn.recv(MAX_BUFFER_SIZE)
        # input_from_server_decode = input_from_server_bytes.decode('cp1252').rstrip()
        input_from_server_decode = input_from_server_bytes.decode('latin-1') #.rstrip()
        all_data += input_from_server_decode

        # Parameter to output loop
        if all_data:
            all_data.encode('utf-8')
            return all_data

def client_program():
    """
    Connection Settings - Start Client - Persistent Connection
    """

    host = '0.0.0.0' ### for port Test
    port = 000  # socket server port number

    conn = socket.socket()  # instantiate
    conn.connect((host, port))  # connect to the server
    MAX_BUFFER_SIZE = 4096

    message = input("to Send -> ")  # take input
    while message.lower().strip() != '':
        conn.sendall(message.encode())  # send message
        input_from_server = rec_data(conn, MAX_BUFFER_SIZE)
        input_string = data_process(input_from_server)
        print('Received -> {}'.format(input_string))  # show in terminal
        message = input("to Send -> ")
    conn.close()

client_program()

