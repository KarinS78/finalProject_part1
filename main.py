import logging

from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
import scratch
import json

app = Flask(__name__)
app.secret_key = "PythonIsFun"
app.permanent_session_lifetime = timedelta(minutes=5)


class User:
    def __init__(self, id_al, full_name, password, real_id):
        self.id_al = id_al
        self.full_name = full_name
        self.password = password
        self.real_id = real_id
        logging.info(f"a new user created the name is :{self.full_name}")

    def __str__(self):
        return f'User [id:{self.id_al},full name:{self.full_name},password:{self.password},real id:{self.real_id}]'


class Flights:
    def __init__(self, flight_Id, timestamp, remaininmg_seats, origion_country_id, dest_country_id):
        self.flight_Id = flight_Id
        self.timestamp = timestamp
        self.remaininmg_seats = remaininmg_seats
        self.origion_country_id = origion_country_id
        self.dest_country_id = dest_country_id
        logging.info(f"a new flight created :{self.flight_Id}")

    def __str__(self):
        return f'Flights [flight id:{self.flight_Id}, time stamp:{self.timestamp}, remaining seats:{self.remaininmg_seats}, origin country id:{self.origion_country_id}, destination country id:{self.dest_country_id}]'


class Tickets:
    def __init__(self, ticket_id, user_id, flight_id):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.flight_id = flight_id
        logging.info(f"a new ticked created: {self.ticket_id}")

    def __str__(self):
        return f'Tickets [ticket id:{self.ticket_id},user id:{self.user_id},flight id:{self.flight_id}]'


class Countries:
    def __init__(self, code_Al, name):
        self.code_Al = code_Al
        self.name = name
        logging.info(f"a new country was created: {self.name}")

    def __str__(self):
        return f'Countries [code:{self.code_Al},name{self.name}]'


"""-----------------------Flight Resource-----------------------"""


@app.route("/flight", methods=["GET"])
def import_flights():
    # import all the flights - task 1 (get)
    variable = ""
    conn, cursor = scratch.Dbinit()
    cursor = scratch.readFlights(cursor)

    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"flight list: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/flight/<int:x>', methods=["GET"])
def cheack_flight(x):
    # import id flight - task 2 (get/id)
    variable = ""
    conn, cursor = scratch.Dbinit()
    cursor = scratch.getIdflight(x, cursor)

    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"flight id: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/form/flight', methods=['GET'])
def form():
    # function for the form -flight post
    logging.debug(f"open form successfully")
    return render_template('flights.html')


@app.route('/flight/post', methods=["POST"])
def add_flights():
    # add a new flight - task 3 (post)
    conn, cursor = scratch.Dbinit()
    # connect to the form
    timestamp = request.form['timeStamp']
    remaininmg_seats = request.form['remaininmgSeats']
    origion_country_id = request.form['origionCountryId']
    dest_country_id = request.form['destCountryId']

    cursor = scratch.insertValues(timestamp, int(remaininmg_seats),
                                  int(origion_country_id), int(dest_country_id), cursor)
    scratch.closeConn(cursor, conn)


    variable = ""
    conn, cursor = scratch.Dbinit()
    cursor = scratch.readFlights(cursor)

    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"flight information: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/flight/put/<int:x>', methods=["GET"])
def remainingSeatsUpdate(x):
    # subtraction remaining seats by the user in the Flight table
    conn, cursor = scratch.Dbinit()
    cursor = scratch.UpdateSeats(x, cursor)
    logging.debug("subtraction remaining seats successfully")
    scratch.closeConn(cursor, conn)


@app.route('/flight/put/<int:x>', methods=["PUT"])
def updateFlight(x):
    # update an existent flight - task 4 (put\id)
    conn, cursor = scratch.Dbinit()
    scratch.UpdateFlight(x, cursor)
    logging.debug("update an existent flight")
    scratch.closeConn(cursor, conn)
    return r"flight updated"


@app.route('/flight/delete/<int:x>', methods=["DELETE"])
def deleteFlight(x):
    # delete an existent flight - task 5 (delete\id)
    conn, cursor = scratch.Dbinit()
    scratch.DeleteValues(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug("flight deleted")

    scratch.closeConn(cursor, conn)
    return f"flight deleted"


"""-----------------------Users Resource-----------------------"""


@app.route('/users', methods=["GET"])
def importUsers():
    # import all the users - task 1 (get)
    conn, cursor = scratch.Dbinit()
    cursor = scratch.readUsers(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"users list: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/users/<int:x>', methods=["GET"])
def checkUser(x):
    # import id users - task 2 (get/id)
    conn, cursor = scratch.Dbinit()
    cursor = scratch.getIdUser(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"users id list:{variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/form/user', methods=['GET'])
def formUsers():
    # function for the form -User post
    logging.debug(f"open form successfully")
    return render_template('Users.html')


@app.route('/user/post', methods=["POST"])
def add_Users():
    # add a new user - task 3 (post)
    conn, cursor = scratch.Dbinit()

    # connect to the form
    fullName = request.form['fullName']
    password = request.form['password']
    realId = request.form['realId']

    cursor = scratch.insertValuesUser(fullName, password, realId, cursor)
    scratch.closeConn(cursor, conn)

    conn, cursor = scratch.Dbinit()
    cursor = scratch.readUsers(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"users information: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/user/put/<int:x>', methods=["PUT"])
def updateUser(x):
    # update an existent user - task 4 (put\id)
    conn, cursor = scratch.Dbinit()
    scratch.updateUser(x, cursor)
    logging.debug(f"update an existent user")
    scratch.closeConn(cursor, conn)
    return r"user updated"


@app.route('/user/delete/<int:x>', methods=["DELETE"])
def deleteUser(x):
    # delete an existent user - task 5 (delete\id)
    conn, cursor = scratch.Dbinit()
    scratch.DeleteUserValues(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"deleted a user")
    scratch.closeConn(cursor, conn)
    return f"user deleted"


"""-----------------------Tickets Resource-----------------------"""


@app.route('/ticket', methods=["GET"])
def importTickets():
    # import all the ticket - task 1 (get)
    conn, cursor = scratch.Dbinit()
    cursor = scratch.readTickets(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"list of all tickets: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/ticket/<int:x>', methods=["GET"])
def checkTickets(x):
    # import id ticket - task 2 (get/id)

    conn, cursor = scratch.Dbinit()
    cursor = scratch.getIdTickets(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"list of ticket Id: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/form/tickets', methods=['GET'])
def formTickets():
    # function for the form -ticket post
    logging.debug(f"open form successfully")
    return render_template('Tickets.html')


@app.route('/tickets/post', methods=["POST"])
def add_Tickets():
    # add a new ticket - task 3 (post)
    conn, cursor = scratch.Dbinit()

    # connect to the form
    user_id = request.form['user_id']
    flight_id = request.form['flight_id']

    cursor = scratch.insertValuesTickets(user_id, flight_id, cursor)
    scratch.closeConn(cursor, conn)

    conn, cursor = scratch.Dbinit()
    cursor = scratch.readTickets(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"a new ticked was added")

    scratch.closeConn(cursor, conn)
    return f"ticket updated"


@app.route('/ticket/delete/<int:x>', methods=["DELETE"])
def deleteTickets(x):
    # delete an existent ticket - task 5 (delete\id)
    conn, cursor = scratch.Dbinit()
    scratch.DeleteTicketsValues(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"deleted ticket")

    scratch.closeConn(cursor, conn)
    return f"ticket deleted"


"""-----------------------Countries Resource-----------------------"""


@app.route('/countries', methods=["GET"])
def importCountries():
    # import all the countries - task 1 (get)
    conn, cursor = scratch.Dbinit()
    cursor = scratch.readCountries(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"list of countries: {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/countries/<int:x>', methods=["GET"])
def checkCountries(x):
    # import id countries - task 2 (get/id)
    conn, cursor = scratch.Dbinit()
    cursor = scratch.getIdCountries(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"ist of Id countires : {variable}")

    scratch.closeConn(cursor, conn)
    return json.loads(variable)


@app.route('/form/countries', methods=['GET'])
def formCountries():
    # function for the form -countries post
    logging.debug(f"open form successfully")
    return render_template('Countries.html')


@app.route('/Countries/post', methods=["POST"])
def add_Countries():
    # add a new countries - task 3 (post)
    conn, cursor = scratch.Dbinit()

    # connect to the form

    name = request.form['name']

    cursor = scratch.insertValuesCountries(name, cursor)
    scratch.closeConn(cursor, conn)

    conn, cursor = scratch.Dbinit()
    cursor = scratch.readTickets(cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a
    logging.debug(f"a new country added ")

    scratch.closeConn(cursor, conn)
    return variable


@app.route('/countries/put/<int:x>', methods=["PUT"])
def updateCountries(x):
    # update an existent flight - task 4 (put\id)

    conn, cursor = scratch.Dbinit()
    scratch.updateCountries(x, cursor)
    logging.debug(f" updated a country ")
    scratch.closeConn(cursor, conn)
    return r"Country updated"


@app.route('/countries/delete/<int:x>', methods=["DELETE"])
def deleteCountries(x):
    # delete an existent flight - task 5 (delete\id)
    conn, cursor = scratch.Dbinit()
    scratch.DeleteCountriesValues(x, cursor)

    variable = ""
    for row in cursor:
        a = str(row)
        variable = variable + a

    scratch.closeConn(cursor, conn)
    return f"Country deleted"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("HomePage.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn, cursor = scratch.Dbinit()
        cursor = scratch.CheckUser(cursor)
        userlist = list(scratch.readUsers(cursor))

        for user in userlist:
            if username == user["name"]:
                # command = conn.execute(f'select password from users WHERE full_name = "{user["name"]}" ')
                for user in cursor:
                    thispassword = user[0]
                if password == thispassword:
                    # functions.thisuser(username, password)
                    User(username, password)
                    flash("Login Successful!")
                    return f"hello {username}"
                else:
                    return "wrong password"
    else:
        return "wrong username"


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("you have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/form/customers', methods=['GET'])
def formCoustomers():
    # function for the form -User post
    return render_template('customers.html')


@app.route("/user/info")
def userInformation():
    # if -existent ticket (methods - get)
    if request.method == 'GET':
        return checkTickets()
    # elif - buy a ticket (methods - get, get/id,post)
    elif request.method == 'POST':
        return render_template('Tickets.html')
    # elif - delete an exsistent ticket (method - delete)
    elif request.method == 'DELETE':
        return deleteTickets()


if __name__ == '__main__':
    app.run()
