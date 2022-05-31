"""
Team Programming Assignment 3


"""

import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12013
MAX_CLIENTS = 2  # maximum clients supported
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT_NAMES = ["X", "Y"]  # Names for clients
ORDER = {1: "first", 2: "second"}  # ordering
END_CONVO_KEYWORD = "Bye"
connections = []  # holds active connections
received_msgs = []  # holds messages from clients
client_threads = []  # holds active threads
end_chat = False

def connection_handler():
    """
    Handles connection to clients and assigning order
    """
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")

    print("[SERVER] The server is waiting to receive two connections...")
    while len(connections) < MAX_CLIENTS:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        connections.append(conn)
        index = connections.index(conn)
        print(f"[SERVER] Accepted {ORDER[index + 1]} connection, calling it {CLIENT_NAMES[index]}")


def send_confirmation_msg(client_list):
    """
    Sends confirmation to connected clients in client_list
    :param client_list: list of active clients
    """
    for client in client_list:
        index = client_list.index(client)
        msg = "[SERVER] From Server: Client {} connected.".format(CLIENT_NAMES[index])
        client.send(msg.encode())
    pass



def exchange_messages(connection):
    """
    used to receive messages from clients, decode, and format
    :param connection:
    """
    global end_chat
    client_name = connections.index(connection)
    # infinite loop to accept and decode messages
    while not end_chat:
        msg = connection.recv(2048).decode()
        #  Listens for end_convo_keyword
        if msg:
            say(msg, CLIENT_NAMES[client_name])
            if msg == END_CONVO_KEYWORD:
                end_chat = True


def say(msg, name="[SERVER]"):
    mod_msg = "{0}: {1}".format(name, msg)
    print(mod_msg)
    for client in connections:
        client.send(mod_msg.encode())


def start_client_communications():
    """
    Starts threads for clients in connection array to receive messages from them.
    """
    for client in connections:
        thread = threading.Thread(target=exchange_messages, args=(client,))
        client_threads.append(thread)
        thread.start()


def client_feedback():
    """
    formats messages from both clients wile noting the order, content and names of senders
    then send received messages this message to all clients
    """
    # unpacking tuples
    first_client, first_msg = received_msgs[0]
    second_client, second_msg = received_msgs[1]
    msg = "[SERVER] {0}: {1} received before {2}: {3}".format(
        CLIENT_NAMES[first_client],
        first_msg,
        CLIENT_NAMES[second_client],
        second_msg
    )
    for client in connections:
        client.send(msg.encode())


def end_connections():
    """
    Joins threads and terminates connections
    """
    goodbye_msg = "[SERVER] Terminated your connection"
    for client in connections:
        client.send(goodbye_msg.encode())
        client.send(END_CONVO_KEYWORD.encode())
    for thread in client_threads:
        thread.join()
    for client in connections:
        client.close()


def launch_server():
    """
    launches the server
    """
    print("[STARTING] Server is starting...")
    try:
        server.bind((SERVER, PORT))
    except socket.error as e:
        print(str(e))
    # starts accepting client connections
    connection_handler()
    # sends confirmations to both clients with their names
    send_confirmation_msg(connections)

    print("[SERVER] Waiting to receive messages from client X and client Y...")

    start_client_communications()
    while not end_chat:
        pass
    # tells clients whose message was received first

    print("[SERVER] Waiting for clients to close connections...")
    # terminates
    end_connections()

    print("[SERVER] Connections successfully terminated.")


if __name__ == "__main__":
    launch_server()
