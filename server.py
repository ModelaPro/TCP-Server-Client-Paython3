#!/usr/bin/python3

"""
Python 3 TCP Server
"""

def data_process(input_string):
    """
    This is where all the processing happens.
    Let's just read the string backwards
    """

    output = input_string
    return output

    # Test
    # return input_string

def rec_data(conn, MAX_BUFFER_SIZE):
    """
    This increases the read capacity of a data packet
    """
    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

    import sys
    siz = sys.getsizeof(input_from_client_bytes)
    if siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))

    input_from_client = input_from_client_bytes.decode().rstrip()
    print('From client -> ' + input_from_client)
    return input_from_client

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    """
    Client Data incoming
    """
    # start_client(port)

    still_listen = True
    while still_listen:
        input_from_client = rec_data(conn, MAX_BUFFER_SIZE)
        # if you receive this or end the connection
        if input_from_client == '':
            print('--ENDOFDATA--')
            conn.close()
            print('Connection ' + ip + ':' + port + " ended")
            still_listen = False

        else:
            res = data_process(input_from_client)
            print('Response -> ' + res)
            vysl = res.encode()  # encode the result string
            conn.sendall(vysl)  # send it to client

            # tell client that we can accept another data processing
            # conn.sendall("-".encode("utf8"))

def start_server():
    """
    Start Server - Configuration
    """
    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("0.0.0.0", 0000)) # IP/PORT Settings
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terrible error!")
            import traceback
            traceback.print_exc()
    soc.close()

start_server()
