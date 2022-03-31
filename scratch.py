import sqlite3
import json
from flask import request

import main

"""------DBInit-------"""
# url2 = r'C:\Users\Hatul\Desktop\lala\finalProject.db'
# conn = sqlite3.connect(url2)
# cursor = conn.cursor()


def Dbinit():
    url2 = r'C:\Users\Hatul\Desktop\lala\finalProject.db'
    conn = sqlite3.connect(url2)
    cursor = conn.cursor()
    return conn, cursor


"""------Suppoting Functions for Flight table------"""
def readFlights(cursor): # connect to import_flights in main (GET)
    SqlStatment = f"SELECT * FROM Flights"
    cursor.execute(SqlStatment)
    return cursor
    # for row in cursor:
    #     print(row)


def getIdflight(x,cursor): # connect to cheack_flight in main(GET\ID)
    SqlStatment = f"SELECT * from Flights where flight_Id = {x}"
    cursor.execute(SqlStatment)
    return cursor


def insertValues(timestamp,remaininmg_seats,origion_country_id,dest_country_id,cursor): # post
    SqlStatment = f"INSERT INTO Flights (timestamp, remaininmg_seats, origion_country_id, dest_country_id) " \
                  f"VALUES('{timestamp}',{remaininmg_seats}, {origion_country_id}, {dest_country_id})"

    cursor.execute(SqlStatment)
    return cursor


def UpdateSeats(x, cursor): #subtraction remaining seats by the user in the Flight table

    SqlStatment = f"select remaininmg_seats FROM Flights WHERE flight_id= {x};"
    cursor.execute(SqlStatment)

    y = ""
    for row in cursor:
        y = row[0]
    y = int(y)
    y=y-1
    y =str(y)

    SqlStatment = f"UPDATE Flights SET remaininmg_seats = {y} WHERE flight_id = {x};"

    cursor.execute(SqlStatment)
    return cursor


def UpdateFlight(x, cursor): #put
    SqlStatment = f"SELECT * from Flights where flight_Id = {x}"
    cursor.execute(SqlStatment)

    for row in cursor:
        oldflight = main.Flights(row[0], row[1], row[2], row[3], row[4])

    newflight = request.json
    newflight = json.dumps(newflight)
    newflight = json.loads(newflight)

    # flight_Id, timestamp, remaininmg_seats, origion_country_id, dest_country_id
    if oldflight.remaininmg_seats != newflight["remaininmg_seats"]:
        oldflight.remaininmg_seats = newflight["remaininmg_seats"]
        cursor.execute(f"UPDATE flights SET remaininmg_seats = {oldflight.remaininmg_seats} WHERE flight_id = {x}")

    if oldflight.origion_country_id != newflight["origion_country_id"]:
        oldflight.origion_country_id = newflight["origion_country_id"]
        cursor.execute(f"UPDATE flights SET origion_country_id = {oldflight.origion_country_id} WHERE flight_id = {x}")

    if oldflight.dest_country_id != newflight["dest_country_id"]:
        oldflight.dest_country_id = newflight["dest_country_id"]
        cursor.execute(f"UPDATE flights SET dest_country_id = {oldflight.dest_country_id} WHERE flight_id = {x}")

    if oldflight.timestamp != newflight["timestamp"]:
        cursor.execute(f"UPDATE flights SET timestamp = datetime() WHERE flight_id = {x}")

    return cursor
    #exsample : {"flight_Id": 1,"timestamp": "15-01-2022", "remaininmg_seats": "123","origion_country_id": "3","dest_country_id":"1"}


def DeleteValues(x, cursor): #DELETE
    SqlStatment = f"DELETE FROM Flights WHERE flight_Id = {x}"
    cursor.execute(SqlStatment)
    return cursor

"""------ Supporting Functions for User table------"""
def readUsers(cursor): #get User
    SqlStatment = f"SELECT * FROM Users"
    cursor.execute(SqlStatment)
    return cursor


def getIdUser(x,cursor): #get id user
    SqlStatment = f"SELECT * from Users where id_al = {x}"
    cursor.execute(SqlStatment)
    return cursor


def insertValuesUser(full_name,password,real_id,cursor): #post
    SqlStatment = f"INSERT INTO Users (full_name, password, real_id) " \
                  f"VALUES('{full_name}',{password}, {real_id})"
    cursor.execute(SqlStatment)
    return cursor


def updateUser(x, cursor): #put
    SqlStatment = f"SELECT * from Users where flight_Id = {x}"
    cursor.execute(SqlStatment)

    for row in cursor:
        oldUser = main.User(row[0], row[1], row[2], row[3])

    newUser = request.json
    newUser = json.dumps(newUser)
    newUser = json.loads(newUser)

    # id_al, full_name, password, real_id
    if oldUser.full_name != newUser["full_name"]:
        oldUser.full_name = newUser["full_name"]
        cursor.execute(f"UPDATE Users SET full_name = {oldUser.full_name} WHERE id_al = {x}")

    if oldUser.password != newUser["password"]:
        oldUser.password = newUser["password"]
        cursor.execute(f"UPDATE Users SET password = {oldUser.password} WHERE id_al = {x}")

    if oldUser.real_id != newUser["real_id"]:
        oldUser.real_id = newUser["real_id"]
        cursor.execute(f"UPDATE Users SET real_id = {oldUser.real_id} WHERE id_al = {x}")

    return cursor


def DeleteUserValues(x, cursor): #DELETE
    SqlStatment = f"DELETE FROM Users WHERE flight_Id = {x}"
    cursor.execute(SqlStatment)
    return cursor


"""------ Supporting Functions for Tickets table------"""
def readTickets(cursor): #get Tickets
    SqlStatment = f"SELECT * FROM Tickets"
    cursor.execute(SqlStatment)
    return cursor

def getIdTickets(x,cursor): #get id Tickets
    SqlStatment = f"SELECT * from Tickets where ticket_id = {x}"
    cursor.execute(SqlStatment)
    return cursor


def insertValuesTickets(user_id, flight_id, cursor): # post
    SqlStatment = f"INSERT INTO Tickets (user_id, flight_id) " \
                  f"VALUES('{user_id}',{flight_id})"
    cursor.execute(SqlStatment)
    return cursor


def DeleteTicketsValues(x, cursor): #DELETE
    SqlStatment = f"DELETE FROM Tickets WHERE ticket_id = {x}"
    cursor.execute(SqlStatment)
    return cursor


"""------ Supporting Functions for Countries table------"""
def readCountries(cursor): #get Tickets
    SqlStatment = f"SELECT * FROM Countries"
    cursor.execute(SqlStatment)
    return cursor


def getIdCountries(x,cursor): #get id Tickets
    SqlStatment = f"SELECT * from Countries where code_Al = {x}"
    cursor.execute(SqlStatment)
    return cursor


def insertValuesCountries(name, cursor): # post
    SqlStatment = f"INSERT INTO Countries (name) " \
                  f"VALUES('{name}')"
    cursor.execute(SqlStatment)
    return cursor


def updateCountries(x, cursor): #put
    SqlStatment = f"SELECT * from Countries where code_Al = {x}"
    cursor.execute(SqlStatment)

    for row in cursor:
        oldCountries = main.Countries(row[0], row[1])

    newCountries=request.json
    newCountries=json.dumps(newCountries)
    newCountries=json.loads(newCountries)

    # code_Al name
    if oldCountries.full_name != newCountries["code_Al"]:
        oldCountries.full_name = newCountries["code_Al"]
        cursor.execute(f"UPDATE Tickets SET user_id = {oldCountries.name} WHERE code_Al = {x}")

    return cursor


def DeleteCountriesValues(x, cursor): #DELETE
    SqlStatment = f"DELETE FROM Countries WHERE code_Al = {x}"
    cursor.execute(SqlStatment)
    return cursor


"""------ Supporting Functions for Client side------"""
def CheckUser(cursor):
    SqlStatment = f'select password from Users WHERE full_name = "{main.User["name"]}" '
    cursor.execute(SqlStatment)
    return cursor






def closeConn(cursor,conn):
    conn.commit()
    cursor.close()
    conn.close()

"""------Main------"""
# insertValues(cursor)
# UpdateValues(cursor)
# DeleteValues(cursor)
# readFlights(cursor)