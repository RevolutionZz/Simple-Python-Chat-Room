#---------------------------IMPORTS-----------------------
import threading
import socket

host = '127.0.0.1' #Host IP Of Server
port = 28379 #Host Port Of Server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates Socket For The Server
server.bind((host, port)) #Binds Socket To The Server IP And Server Port
server.listen() #Listening For Incoming Connections

clients = [] #List For Connected Clients
nicknames = [] #List For Nick names For Connected Clients

def broadcast(message): #Function For Sending Messages To The Client
    for client in clients: #For Loop To Iterate Over Each Client Connected To The Server
        client.send(message) #Sends Message To All The Connected Clients From The Server

def handle(client): #Function For Handling The Client Connection
    while True: #While Loop To Endlessly Executing
        try: #Try Statement To Execute Code But With Error Handling
            message = client.recv(1024) #Recieving 1024 Bytes Of Data From A Client
            broadcast(message) #Sends Message To All Clients Via broadcast Function
        except:
            index = client.index(client) #Gets Index Of Failed Client Within The clients List
            clients.remove(client) #Remove Client From The clients List
            client.close() #Terminates The Client's Connection
            nickname = nicknames[index] #Gets Index Of The Client's Nick Name Within The nicknames List
            broadcast(f"{nickname} has left the chat".encode('ascii')) #Sends Left Chat Message To All The Clients
            nicknames.remove(nickname) #Removes Nick Name From The nicknames List
            break #Breaks Out Of The Loop

def receive(): #Function For Recieving Client Connections
    while True: #While Loop To Endlessly Recieve Connections
        client, address = server.accept() #Accepts Client Connection
        print("Connected with {}".format(str(address))) #Output To Server Console Only
        client.send('NICK'.encode('ascii')) #Sends The Keyword NICK To Connected Client
        nickname = client.recv(1024).decode('ascii') #Recieves The Clients Nick Name
        nicknames.append(nickname) #Adds Client Nick Name To The nicknames List
        clients.append(client) #Adds The Client To The clients List

        print("Nickname is {}".format(nickname)) #Outputs Client's Nick Name To Server Console Only
        client.send('CONNECTED!'.encode('ascii'))  # Sends Message To Each Individual Client To Verify The Connection To The Server
        broadcast("{} joined the chat!".format(nickname).encode('ascii')) #Sends Message To All Of The Connected Clients

        #Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive() #Calls The receive Function