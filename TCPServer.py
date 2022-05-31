import socket
import threading
"""
Team Programming Assignment # 3
Team 5 -  Layla, Saul, and Yavik
Date: May 31, 2022
The objective of this program is to create a server which can send and receive messages from two clients.
The server assigns clients names X and Y based on connection order.
Once clients send messages the server will broadcast a message to both clients announcing whose msg arrive first

In order for this to work in mininet, please run the server on H3 or edit the ip SERVER field to the hosts IP
"""

SERVER = "10.0.0.3"
PORT = 12013
MAX_CLIENTS = 2  # maximum clients supported
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT_NAMES = ["X", "Y"]  # Names for clients
ORDER = {1: "first", 2: "second"}  # ordering
connections = []  # holds active connections
received_msgs = []  # holds messages from clients
client_threads = []  # holds active threads


def connection_handler():
    """
    Handles connection to clients and assigning order
    """
    server.listen(2)
    print("[LISTENING] Server is listening on {}".format(SERVER))

    print("[SERVER] The server is waiting to receive two connections...")
    while len(connections) < MAX_CLIENTS:
        conn, addr = server.accept()
        print("[NEW CONNECTION] {} connected.".format(addr))
        connections.append(conn)
        index = connections.index(conn)
        print("[SERVER] Accepted {0} connection, calling it {1}".format(
            ORDER[index + 1],
            CLIENT_NAMES[index]))


def send_confirmation_msg(client_list):
    """
    Sends confirmation to connected clients in client_list
    :param client_list: list of active clients
    """
    for client in client_list:
        index = client_list.index(client)
        msg = "[SERVER] From Server: Client {} connected.".format(CLIENT_NAMES[index])
        client.send(msg.encode())


def receive_messages(connection):
    """
    used to receive messages from clients, decode, and format
    :param connection:
    """
    client_name_pos = connections.index(connection)
    # infinite loop to accept and decode messages
    while True:
        msg = connection.recv(2048).decode()
        # exit loop if empty string received due to closed connection
        if not msg:
            break
        # store and print confirmation of client message
        else:
            # received messages are store in array as tuple pairs of client name and message
            received_msgs.append((client_name_pos, msg))
            index = received_msgs.index((client_name_pos, msg))
            print("[Client {0}] sent message {1}: {2}".format(CLIENT_NAMES[client_name_pos],
                                                              index + 1,
                                                              msg))


def start_client_communications():
    """
    Starts threads for clients in connection array to receive messages from them.
    """
    for client in connections:
        thread = threading.Thread(target=receive_messages, args=(client,))
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
    for client in connections:
        client_threads[connections.index(client)].join()
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
    while len(received_msgs) < 2:
        pass
    # tells clients whose message was received first
    client_feedback()
    print("[SERVER] Waiting for clients to close connections...")
    # terminates
    end_connections()

    print("[SERVER] Connections successfully terminated.")


if __name__ == "__main__":
    launch_server()
