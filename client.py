#-----------------------------IMPORTS--------------------------
import threading
import socket

nickname = input("Enter a nickname: ") #Input For Client Nick Name

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates The Socket
client.connect(('127.0.0.1', 28379)) #Connects To The Specified IP And Port

def receive(): #Function For Recieving Server Data
    while True: #While Loop To Endlessly Listen And Recieve Data From The Server
        try: #try Statement To Keep Trying A Block Of Code With Error Handling
            message = client.recv(1024).decode('ascii') #Recieves 1024 Bytes Of Data From Server
            if message == 'NICK': #If The Data Was The Keyword 'NICK'
                client.send(nickname.encode('ascii')) #Client Will Send The It's Nick Name To The Server
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close() #Terminates Connection
            break

def write(): #Function For Writing And Sending Messages
    while True: #While Loop To Endlessly Waiting For Inputs
        message = '{}: {}'.format(nickname, input('')) #Client's Message
        client.send(message.encode('ascii')) #Sends Message To The Server

recieve_thread = threading.Thread(target=receive) #Creates New Thread For When Client Is Recieving Data
recieve_thread.start() #Starts Thread

write_thread = threading.Thread(target=write) #Creates New Thread For When Client Is Writing A Message
write_thread.start() #Starts Thread
