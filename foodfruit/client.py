import socket
import time
import os
import sys
import pickle
import sqlite3
from datetime import datetime

print('\n\n','*'*10 + '  CLIENT  ' + '*'*10,'\n\n')
TCP_IP = "127.0.0.1"
TCP_PORT = 6789
BUFFER_SIZE = 1024

NoPhone = "" #รอรับค่าเลขมือถือจากผู้ใช้
password = "" #รอรับรหัสผ่านจากผู้ใช้

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))

flag_login = 0

def Clear():
    os.system('cls')

def Main():
    print('1 ล็อกอิน' + '\n'
      '2 สมัครสมาชิก \n\n')
    while True:
        Input = int(input('โปรดเลือกเมนู (หมายเลข): '))
        Clear()
        if Input == 1:
            Login()
            break
        elif Input == 2:
            Register()
            time.sleep(2)
            Login()
            break
        else:
            print('โปรดกรอกหมายเลขให้ถูกต้อง!')
    global flag_login
    if flag_login == 1:
        menu()

    s.close()
    print('*'*10 + '  EXIT  ' + '*'*10)

def Login():
    while True:
        print("\n :ระบบล็อกอิน:")     
        s.send(bytes("--LOGIN--","utf-8"))
        global NoPhone
        global password
        NoPhone = input("โปรดกรอกเบอร์มือถือ 10 หลัก: ")
        s.send(bytes(NoPhone,"utf-8"))
        password = input("โปรดกรอกรหัสผ่าน: ")
        Clear()
        s.send(bytes(password,"utf-8"))
        time.sleep(1)
        s.send("break".encode("utf-8"))

        while 1:
            data = s.recv(BUFFER_SIZE).decode("utf-8")
            if not data: break
            elif data == "yes":
                #login สำเร็จ
                print("เข้าสู่ระบบสำเร็จแล้ว\n")
                print("สวัสดีคุณ, ",NoPhone)
                global flag_login
                flag_login = 1
                break
            elif data == "no":
                #login ไม่สำเร็จ
                print("คุณเข้าสู่ระบบไม่สำเร็จ")
                print("กรุณาลองใหม่อีกครั้ง\n")
                break
        if flag_login == 1:
            break

def Register():
    print("\n :ระบบสมัครสมาชิก:")   
    global NoPhone
    global password
    while True:
        NoPhone = input("โปรดกรอกเบอร์มือถือ 10 หลัก: ")
        password = input("โปรดกรอกรหัสผ่าน: ")
        password_con = input("โปรดกรอกรหัสผ่านอีกครั้ง เพื่อยืนยัน: ")
        if password == password_con:
            s.send(bytes("--REG--","utf-8"))
            time.sleep(0.5)
            s.send(bytes(NoPhone,"utf-8"))
            time.sleep(0.1)
            s.send(bytes(password,"utf-8"))
            time.sleep(0.1)
            s.send("break".encode("utf-8"))
            print("ได้ทำการส่งคำขอไปที่เซิร์ฟเวอร์")
            break
        else:
            print("โปรดตรวจสอบรหัสผ่านและรหัสผ่านยืนยันให้ตรงกัน")
    #ทำการส่งข้อมูลไปสมัคร
    while 1:
        data = s.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        elif data == "yes":
            #login สำเร็จ
            print("ทำการสมัครสมาชิกสำเร็จ\n")
            time.sleep(1)
            Clear()
            break

def Confirm(value,amount,Datetime):
    Clear()
    print("โปรดรอสักครู่...")

    s.send(bytes("--CONFIRM--","utf-8"))
    time.sleep(0.5)

    value_tosend = pickle.dumps(value)
    s.send(bytes(value_tosend))
    time.sleep(0.5)
    s.send(bytes("more for break","utf-8"))
    time.sleep(0.5)

    amount_tosend = pickle.dumps(amount)
    s.send(bytes(amount_tosend))
    time.sleep(0.5)
    s.send(bytes("more for break","utf-8"))
    time.sleep(0.5)

    s.send(bytes(NoPhone,"utf-8"))
    time.sleep(0.5)

    s.send(bytes(Datetime,"utf-8"))
    time.sleep(0.5)

    #รับคำขอแล้ว กำลังจัดทำ กำลังจัดสั่ง ดำเนินการเสร็จแล้ว
    print("\n--- สถานะการจัดส่ง ---\n")
    while 1:
        data = s.recv(BUFFER_SIZE).decode("utf-8")
        if not data: break
        elif data == "yes":
            print("25%|##        | รับคำขอแล้ว!.")
        elif data == "make":
            print("50%|#####     | กำลังจัดทำ!.")
        elif data == "send":
            print("75%|########  | กำลังจัดส่ง!.")
        elif data == "exit":
            print("100%|##########| ดำเนินการเสร็จแล้ว!.")
            break

def menu():
    #print("\n :เมนูหลัก:\n")
    #print("1 สั่งผลไม้")
    #print("2 ดูประวัติการสั่ง")
    if NoPhone == "admin":
        admin()
    else:
        while True:
            print("\n :เมนูหลัก:\n")
            print("1 สั่งผลไม้")
            print("2 ดูประวัติการสั่ง")
            print("3 EXIT")
            Input = int(input('โปรดเลือกเมนู (หมายเลข): '))
            Clear()
            if Input == 1:
                Order()
            if Input == 2:
                History()
            if Input == 3:
                Exit()
        
def Order():
    f = open('fruit.txt',encoding='utf-8')
    
    list_fruit=[]
    for line in f:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list_fruit.append(line_list)

    #ปริ้นรายการ   

    value=[]
    amount=[]
    cost=0
    Datetime=""
    while True:
        print("\n : เมนูผลไม้ :\n")
        for i in range(0,len(list_fruit)):
            print(list_fruit[i][0] ,list_fruit[i][1], list_fruit[i][2],"บาท")
        print("\nC=ยืนยันคำสั่งซื้อ, D=ลบข้อมูลสินค้าที่เลือกไว้, E=Exit, (กรอกหมายเลขสินค้า)")
        Input_value = input("โปรดกรอกสินค้าที่ต้องการ :")

        if Input_value == 'C':
            if len(value) == 0:
                print("\n #### ไม่มีสินค้าในตะกร้า ไม่สามารถทำรายการได้!! ")
            else:
                Confirm(value,amount,Datetime)
                Clear()
                print("ทำการสั่งซื้อเรียบร้อยแล้ว")
            break
        elif Input_value == 'D':
            Clear()
            print("ทำการลบสินค้าที่เลือกไว้แล้ว")
            value=[]
            amount=[]
            cost=0
        elif Input_value == 'E':
            Clear()
            print("ทำการยกเลิกการสั่งซื้อ")
            break
        else:
            cost=0
            Input_value = int(Input_value)
            if Input_value > 0 and Input_value < (len(list_fruit)+1):
                value.append(list_fruit[Input_value - 1])
                Input_amount = int(input("โปรดกรอกจำนวนที่ต้องการ (ตัวเลข) :"))
                print("\n")
                Clear()
                amount.append(Input_amount)
            else:
                Clear()
                print("#### โปรดกรอกเลขสินค้าให้ถูกต้อง!!!!!")
        print("\n\n******************:รายการสินค้าตอนนี้:******************")
        Datetime = str(datetime.now())
        for i in range(0,len(value)):
            #debug #print("cost:",cost,"ราคา",value[i][2],"x","จำนวน",amount[i])
            cost+=(int(value[i][2])*amount[i])
        for i in range(0,len(value)):
            print(value[i][1],"จำนวน x"+str(amount[i]),"ราคาหน่วยละ",value[i][2],"บาท")
        if(len(value) == 0):
            print("ไม่มีสินค้าในตะกร้าของคุณ")
        print("รวมยอดทั้งหมดคือ : ",cost,"บาท")
        print("วันเวลา",Datetime)
        print("***************************************************\n")
    #f.close()

def History():
    #pull information to list
    places = []
    with open('order.txt', 'r',encoding='utf-8') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            places.append(currentPlace)
        #print(places)

    #Debug
    '''
    i=0
    for x in places:
        print(i,x)
        i=i+1
    '''
    
    #ปริ้น ORDER
    k=0
    #print(len(places))
    while k < len(places):
        if(places[k] == NoPhone):
            print("ORDER เลขที่", int(k/6))
            print("มีอาหารดังนี้", places[k+1])
            #print(len(list(places[k+1])))
            #print(list(places[k+1][3]))
            print("จำนวน", places[k+2])
            print("ราคารวม", places[k+3])
            print("วันที่/เวลา ที่สั่งซื้อ", places[k+4],"\n")
            
        k=k+6
    
def Exit():
    s.send("--QUIT--".encode("utf-8"))
    print("ขอบคุณที่ใช้บริการ Fruit Delivery ^_^")
    sys.exit()

def ADMIN_Order():
    #pull information to list
    places = []
    with open('order.txt', 'r',encoding='utf-8') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            places.append(currentPlace)
        #print(places)

    #ปริ้น ORDER
    k=0
    #print(len(places))
    while k < len(places):
        print("ORDER เลขที่", int(k/6))
        print("ผู้รับบริการ", places[k])
        print("มีอาหารดังนี้", places[k+1])
        print("จำนวน", places[k+2])
        print("ราคารวม", places[k+3])
        print("วันที่/เวลา ที่สั่งซื้อ", places[k+4],"\n")
        k=k+6

def ADMIN_User():
    conn_db = sqlite3.connect('customer.db')
    c=conn_db.cursor()
    print("ได้ทำการเชื่อมต่อฐานข้อมูลแล้ว")
    c.execute("SELECT * FROM customer")
    for no in c.fetchall():
        print("No.Phone & Password",no)
    conn_db.commit()
    conn_db.close()
    print("ตัดการเชื่อมต่อฐานข้อมูลแล้ว")

def admin():
    print("\n :เมนูหลัก (ADMIN):\n")
    print("1 ดูประวัติการสั่งทั้งหมด")
    print("2 ดูรายชื่อผู้รับบริการทั้งหมด")
    print("3 EXIT")
    Input = int(input('โปรดเลือกเมนู (หมายเลข): '))
    Clear()
    if Input == 1:
        ADMIN_Order()
    if Input == 2:
        ADMIN_User()
    if Input == 3:
        Exit()

Main() #รันโปรแกรม
