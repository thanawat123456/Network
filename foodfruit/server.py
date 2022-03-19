import socket
import time
import traceback
import sqlite3
from threading import Thread
import pickle

print('\n\n','*'*10 + '  SERVER  ' + '*'*10,'\n\n')
TCP_IP = "127.0.0.1"
TCP_PORT = 6789
BUFFER_SIZE = 1024

def Login(connection ,ip):
    member_profile = []
    print(connection,"ได้ทำการเชื่อมต่อเข้ามาเพื่อขอล็อกอิน")
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        if len(member_profile) > 2 or len(member_profile) == 2:
            break
        print("รับข้อความมาว่า : ",data)
        member_profile.append(data)
    print("No.Phone&Password: ",member_profile)

    #check id
    conn_db = sqlite3.connect('customer.db')
    c=conn_db.cursor()
    print("ได้ทำการเชื่อมต่อฐานข้อมูลแล้ว")
    c.execute("SELECT * FROM customer")
    flag = 1
    for no in c.fetchall():
        if no == tuple(member_profile):
            print("ข้อมูลถูกต้อง!!! ")
            flag = 0
            break
    if flag == 0:
        connection.send("yes".encode("utf-8"))
    else:
        connection.send("no".encode("utf-8"))
    conn_db.commit()
    conn_db.close()
    print("ตัดการเชื่อมต่อฐานข้อมูลแล้ว")
    print("ล็อกอินสำเร็จแล้ว")

def Register(connection ,ip):
    member_profile = []
    print(connection,"ได้ทำการเชื่อมต่อเข้ามาเพื่อขอสมัครสมาชิก")
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        elif len(member_profile) > 2 or len(member_profile) == 2:
            break
        print("rev: ",data)
        member_profile.append(data)
        print(member_profile)
        print(len(member_profile))
    print("No.Phone&Password: ",member_profile)

   #check id
    conn_db = sqlite3.connect('customer.db')
    c=conn_db.cursor()
    print("ได้ทำการเชื่อมต่อฐานข้อมูลแล้ว")
    sqlite_insert_with_param = """INSERT INTO customer
                          (NoPhone, Password) 
                          VALUES (?, ?);"""
    data_tuple = (member_profile[0],member_profile[1])
    c.execute(sqlite_insert_with_param, data_tuple)
    print("ทำการนำข้อมูลเข้าสู่ฐานข้อมูลแล้ว")
    time.sleep(0.1)

    conn_db.commit()
    conn_db.close()
    print("ตัดการเชื่อมต่อฐานข้อมูลแล้ว")
    connection.send("yes".encode("utf-8"))
    print("สมัครสมาชิกสำเร็จแล้ว")

def Confirm_Order(connection ,ip, port):
    #รับคำขอแล้ว กำลังจัดทำ กำลังจัดสั่ง ดำเนินการเสร็จแล้ว
    #รับ 
    # รับ value
    print("order loading...")
    value = []
    while True:
        data = connection.recv(BUFFER_SIZE)
        if not data: break
        elif len(value)>1:
            break
        #print("rev: ",data)
        value = data
    value = pickle.loads(value)
    #print("value: ",value)
    time.sleep(0.2)

    #รับ amount
    amount = []
    while True:
        data = connection.recv(BUFFER_SIZE)
        if not data: break
        elif len(amount)>1:
            break
        #print("rev: ",data)
        amount = data
    amount = pickle.loads(amount)
    #print("amount: ",amount)
    #print("รอรับแล้วโว้ยยย")

    #รับเบอร์ผู้รับบริการ
    NoPhone="0"
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        NoPhone = data
        if NoPhone != '0':
            break
    #print("ลูกค้าเบอร์ ",NoPhone)
    
    #รับวันเวลา
    Datetime="0"
    while True:
        data = connection.recv(BUFFER_SIZE).decode("utf-8")
        Datetime = data
        if Datetime != '0':
            break
    #print("วันเวลา ",Datetime)

    #คำนวณยอดรวม
    cost = 0
    for i in range(0,len(value)):
        print("cost:",cost,"ราคา",value[i][2],"x","จำนวน",amount[i])
        cost+=(int(value[i][2])*amount[i])

    print("\n\n******************:รายการสินค้าของคุณ ",ip+":"+port,":******************")
    for i in range(0,len(value)):
        print(value[i][1],"จำนวน x"+str(amount[i]),"ราคาหน่วยละ",value[i][2],"บาท")
    if(len(value) == 0):
        print("ไม่มีสินค้าในตะกร้าของคุณ")
    print("รวมยอดทั้งหมดคือ : ",cost,"บาท")
    print("วันเวลา",Datetime)
    print("************************************************\n")

    
    #text = "["+"id="+NoPhone+"\n"+str(value)+"\n"+str(amount)+"\n"+str(cost)+"\n"+str(Datetime)+"]"+"\n\n"
    #NoPhone = "'" + NoPhone + "'"
    #Datetime = "'" + Datetime + "'"
    #text = NoPhone+","+str(value)+","+str(amount)+","+str(cost)+","+str(Datetime)+"\n"
    text = [NoPhone,value,amount,cost,Datetime]
    #places = ['Berlin', 'Cape Town', 'Sydney', 'Moscow']
    with open('order.txt', 'a',encoding='utf-8') as filehandle:
        for listitem in text:
            filehandle.write('%s\n' % listitem)
        filehandle.write('\n')

    #ส่ง
    time.sleep(1)
    while True:
        print("\n\nทำการส่งข้อมูลไปถึงคุณลูกค้า ",ip+":"+port)
        print("พิมพ์ Y เพื่อรับคำขอ,M เพื่อจัดทำ,S เพื่อจัดส่ง,E เพื่อเสร็จสิ้นการจัดส่ง:")
        confirm1=input("ป้อนคำสั่ง : ")
        if confirm1 == 'Y':
            connection.send("yes".encode("utf-8"))
        elif confirm1 == 'M':
            connection.send("make".encode("utf-8"))
        elif confirm1 == 'S':
            connection.send("send".encode("utf-8"))
        elif confirm1 == 'E':
            connection.send("exit".encode("utf-8"))
            break

def process_input(input_str):
    print("Processing the input received from client")

    return str(input_str).upper()

def receive_input(connection):
    client_input = connection.recv(BUFFER_SIZE)
    
    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result

def client_thread(connection, ip, port):
    is_active = True

    while is_active:
        client_input = receive_input(connection)

        if "--LOGIN--" in client_input:
            print("สมาชิกกำลังล็อกอินเข้าสู่ระบบ...")
            Login(connection, ip)
        elif "--REG--" in client_input:
            print("สมาชิกขอสมัครสมาชิกเข้าสู่ระบบ")
            Register(connection, ip)
        elif "--CONFIRM--" in client_input:
            print("สมาชิกขอสมัครสมาชิกเข้าสู่ระบบ")
            Confirm_Order(connection, ip, port)
        elif "--QUIT--" in client_input:
            print("Client ได้ทำการร้องขอออกจากระบบ")
            connection.close()
            print("Connection " + ip + ":" + port + " ได้ทำการออกจากระบบ")
            is_active = False
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP,TCP_PORT)) #เชื่อมต่อ
    s.listen(5)
    print("ได้ทำการรันเซิร์ฟเวอร์แล้ว")

    #flag_server = 0
    while True:
        conn,addr = s.accept()
        ip,port = str(addr[0]), str(addr[1])
        print("มีการเชื่อมต่อเข้ามา...")
        try:
            Thread(target=client_thread,args=(conn,ip,port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    s.close()
    
Main()