import mysql.connector as sql
import argon2
from cryptography.fernet import Fernet
import base64

pd = str(input("pd: ")).encode()
salt = str(input("salt: ")).encode()
key = base64.urlsafe_b64encode(argon2.hash_password(password=pd, salt=salt)[:32])
f = Fernet(key)

message = "It is a big secret"
encrypted = f.encrypt(message.encode())

print("\n------------------------------------------\n")
print("pd (remember this): " + str(pd.decode()))
print("salt (remember this): " + str(salt.decode()))
print("encrypted (copy this to lockle.py line 45 'encrypted = '): " + str(encrypted))
print("\n------------------------------------------\n")
print("Come back after installing mysql and create a database named 'accounts'.")

host = str(input("host: "))
user = str(input("user: "))
passwd = str(input("passwd: "))

db = sql.connect(host=host, user=user, passwd=passwd, database='accounts')
mycursor = db.cursor()
mycursor.execute("CREATE TABLE ac (target NOT NULL VARCHAR(50), email VARCHAR(255), username VARCHAR(255), password VARCHAR(255))")

print("Table created. Please check the table with sql and put host string and user string into lockle line 32.")
