import socket

serverip = '127.0.0.1' #ใส่ip เครื่อง server ในส่วนของ client
port = 7500

while True:
    data = input('Enter Message: ')
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR,1)
    
    server.connect((serverip,port)) #เชื่อมต่อไป server ไหน port ไหน
    server.send(data.encode('utf-8')) #ส่งข้อมูลไปหาserver
    
    data_server = server.recv(1024).decode('utf-8') #decode ทำการถอดรหัสก่อน
    print('Data from Server: ', data_server)
    server.close()

