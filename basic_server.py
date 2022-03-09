from http import client
import socket

serverip = '127.0.0.1' #ใส่ ip เครื่องของเรา
port = 7500

while True:
    server = socket.socket() # ประกาศตัวแปร server
    server.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEADDR,1) #เพื่อที่จะสามารถใช้ port เดิมได้ ถ้าไม่ใส่จุดนี้มันอาจจะรันได้สัก 2-3 ครั้ง ครั้งต่อไปจะerrorเพระเหมือนมันใช้ port ซ้ำ

    server.bind((serverip,port)) #ก็คือสั่งรันได้แล้ว รอ client เข้ามาติดต่อ
    server.listen(5) #conect เข้ามาใช้งานพร้อมกัน 5 q เช่น 0.00001 วินาที จะรับได้ 5 q
    print('Wating for clinet...')

    client, addr = server.accept()
    print('Connect from: ' , str(addr))
    data = client.recv(1024).decode('utf-8') #จำนวนที่จะรับได้เป็นหน่วนไบทร์
    print('Message from client: ', data)
    client.send('We received your Message!'.encode('utf-8')) #ก่อนจะส่งไปหาคนอื่นได้เราจะต้อง encode('utf-8')) ก่อน
    client.close() 



