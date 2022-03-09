
import socket
import threading
import sys


PORT = 7500
BUFSIZE = 4096
SERVERIP = '127.0.0.1' 


def server_handler(client):
    while True:
        try:
            data = client.recv(BUFSIZE) #server จะส่ง data มาให้เรา ว่าใครส่งข้อความมาบ้าง
        except:
            print('ERROR')
            break
        if(not data) or (data.decode('utf-8')=='q'):
            print('OUT!')
            break
        
        print('USER: ',data.decode('utf-8'))
    
    client.close()


client = socket.socket(socket.AF_INET ,socket.SOCK_STREAM) #สร้าง socket
client.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR,1) 


try:
    client.connect((SERVERIP,PORT)) #conect go to server
except:
    print("ERROR!")
    sys.exit() #not conect go to out server


task = threading.Thread(target=server_handler,args=(client,)) #สั่งรัน
task.start()

while True:
    msg = input('Message: ')
    client.sendall(msg.encode('utf-8'))
    if msg == 'q':
        break
client.close()











