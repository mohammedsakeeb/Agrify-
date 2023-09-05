import serial
import pandas as pd

arduino_port = "COM3" 
baud = 9600
fileName="temperature.csv"
samples = 10
print_labels =  False


ser = serial.Serial(arduino_port,baud)
print("connection to arduino port:" + arduino_port)
file = open(fileName,"a")
print("created file")

line = 0

while line <= samples:
        if line==0:
            print("printing coloumn header")
        else:
            print("line" + str(line) + ":writing...")
            
        getData=str(ser.readline())
        data=getData[0:]
        print(data)
        
        file = open(fileName,"a")
        file.write(data + "\n")
        line = line+1

print("data collection completed")

file.close()
ser.close()

data = pd.read_csv('temperature.csv')


import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',  
                        password='sakeeb*12')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE sampleDB")
        print("isampleDB database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
    
    
try:
    conn = msql.connect(host='localhost', 
                           database='sampleDB', user='root', 
                           password='sakeeb*12')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS sa6;')
        print('Creating table....')
        cursor.execute("CREATE TABLE sa6 (temperature VARCHAR(100) NOT NULL)")
        print("iris table is created....")
        for i,row in data.iterrows():
            sql = "INSERT INTO sampleDB.sa6 VALUES (%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)





            