# Made by Aedan!
import socket #we are importing the socket library 

try:
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creating var (object correct name)  for mySocket to read Ipv4 and TCP 
    remote_host = "www.google.com"
    remote_port = 80
    remote_ip = socket.gethostbyname(remote_host) 

    mySocket.connect((remote_ip,remote_port)) #connecting based on the variables we put in 
    print(f"connected to {remote_host} on port {remote_port} ")   

    request = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n".encode() #computer cannot read text format, .encode used to translate to binary 
    mySocket.send(request) #sends var "request"

    response = mySocket.recv(2000).decode() #Listening for (2000) bytes and then decoding from binary to string ("") to readable version
    print('Press enter to continue...')
    input()
    print(f"received: {response} ")

except socket.error as e:       
    print("There is a error: " + str(e) )  #Converting "e" into a string add that string with "there is a error" and printing that to the screen 

finally: 
    mySocket.close() #ending connection with socet to receive data from google server