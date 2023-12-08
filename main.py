# Import Flask Library
import random
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors
from datetime import datetime
from functools import wraps

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def staff_only(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('staff'):
            return route(*args, **kwargs)  # Direct to the actual function implementation
        else:
            return render_template('unauthorized.html')  # Redirect to unauthorized page or whatever of your choice

    return wrapper


def customer_only(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('customer'):
            return route(*args, **kwargs)  # Direct to the actual function implementation
        else:
            return render_template('unauthorized.html')  # Redirect to unauthorized page or whatever of your choice

    return wrapper


# Define route for home page
@app.route('/')
def home():
    cursor = conn.cursor()
    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
            'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'

    cursor.execute(query)
    posts = cursor.fetchall()
    cursor.close()
    return render_template('home.html', posts=posts)


@app.route('/search_flight_home', methods=['GET', 'POST'])
def search_flight_home():
    cursor = conn.cursor()
    beginDate = request.form['beginDate']
    endDate = request.form['endDate']
    sourceAirport = request.form['sourceAirport']
    destinationAirport = request.form['destinationAirport']

    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
            'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'

    cursor.execute(query)
    posts = cursor.fetchall()

    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Flight ' \
            'WHERE dept_date >= %s and dept_date <= %s and dept_airport = %s and arri_airport = %s'
    cursor.execute(query, (beginDate, endDate, sourceAirport, destinationAirport))
    data = cursor.fetchall()

    cursor.close()
    if (data):
        return render_template('home.html', data=data, posts=posts)
    else:
        # returns an error message to the html page
        error = 'Invalid Input'
        return render_template('home.html', error=error)


# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for customer register
@app.route('/registerCustomer')
def registerCustomer():
    return render_template('registerCustomer.html')


# Define route for staff register
@app.route('/registerStaff')
def registerStaff():
    return render_template('registerStaff.html')


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # md5 hash the password
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    password = md5.hexdigest()

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM Airline_Staff WHERE username = %s and air_password = %s'
    cursor.execute(query, (username, password))
    data1 = cursor.fetchone()
    query = 'SELECT * FROM customer WHERE email = %s and customer_password = %s'
    cursor.execute(query, (username, password))
    data2 = cursor.fetchone()

    # close the cursor once complete
    cursor.close()

    if (data1):
        # creates a session for the staff
        session['username'] = username
        # use redirect and url_for to redirect to path without rendering html
        session['staff'] = True
        session['customer'] = False
        return redirect(url_for('staffMainPage'))
    elif (data2):
        # creates a session for the customer
        session['username'] = username
        # use redirect and url_for to redirect to path without rendering html
        session['staff'] = False
        session['customer'] = True
        return redirect(url_for('cusMainPage'))
    else:
        # return an error message to the html page
        error = 'Invalid login or username'
        session['staff'] = False
        session['customer'] = False
        return render_template('login.html', error=error)


# Authorize Staff
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['first name']
    lastname = request.form['last name']
    dateOfBirth = request.form['date of birth']
    airline = request.form['airline name']
    emails = request.form.getlist('email')
    phones = request.form.getlist('phone')

    # md5 hash the password
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    password = md5.hexdigest()

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM Airline_Staff WHERE username = %s'
    cursor.execute(query, username)
    data = cursor.fetchone()

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('registerStaff.html', error=error)
    else:
        ins = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstname, lastname, dateOfBirth, airline))
        ins = 'INSERT INTO Working VALUES(%s, %s)'
        cursor.execute(ins, (airline, username))

        for email in emails:
            cursor.execute('INSERT INTO staff_email VALUES(%s, %s)', (username, email))
        for phone in phones:
            cursor.execute('INSERT INTO staff_phone_num VALUES(%s, %s)', (username, phone))
        query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
                'FROM Working Natural JOIN Flight ' \
                'WHERE Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
                'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'
        cursor.execute(query)
        data = cursor.fetchall()
        # commit changes for insert to go through
        conn.commit()
        cursor.close()
        return render_template('home.html', posts=data)


# Authorize Customer
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
    # grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['first name']
    lastname = request.form['last name']
    state = request.form['state']
    city = request.form['city']
    zipcode = request.form['zipcode']
    street = request.form['street']
    building = request.form['building number']
    apartment = request.form['apartment number']
    passport_num = request.form['passport number']
    passport_exp_date = request.form['passport expiration date']
    passport_country = request.form['passport country']
    date_of_birth = request.form['date of birth']
    phones = request.form.getlist('phone')

    # md5 hash the password
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    password = md5.hexdigest()

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, email)
    data = cursor.fetchone()

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        cursor.close()
        return render_template('registerCustomer.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            email, firstname, lastname, password, building, street, apartment, city, state, zipcode, passport_num,
            passport_exp_date, passport_country, date_of_birth))
        for phone in phones:
            cursor.execute('INSERT INTO customer_phone_number VALUES(%s, %s)', (email, phone))

        query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
                'FROM Working Natural JOIN Flight ' \
                'WHERE Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
                'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'

        cursor.execute(query)
        data = cursor.fetchall()
        # commit changes for insert to go through
        conn.commit()
        cursor.close()
        return render_template('home.html', posts=data)


# Define a route to hello function
@app.route('/')
@staff_only
def hello():
    return render_template('staffMainPage.html')


@app.route('/staffMainPage')
@staff_only
def staffMainPage():
    username = session['username']
    return render_template('staffMainPage.html', username=username)


@app.route('/viewFlight')
@staff_only
def viewFlight():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Working.username =  %s ' \
            'and Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
            'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewFlight.html', posts=data)


@app.route('/search_flight_staff', methods=['GET', 'POST'])
@staff_only
def searchFlight():
    username = session['username']
    cursor = conn.cursor()
    beginDate = request.form['beginDate']
    endDate = request.form['endDate']
    sourceAirport = request.form['sourceAirport']
    destinationAirport = request.form['destinationAirport']

    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Working.username = %s and Flight.dept_date >= %s and Flight.dept_date <= %s and dept_airport = %s and arri_airport = %s'
    cursor.execute(query, (username, beginDate, endDate, sourceAirport, destinationAirport))
    data1 = cursor.fetchall()

    cursor.close()
    if (data1):
        return render_template('viewFlight.html', username=username, posts=data1)
    else:
        # returns an error message to the html page
        error = 'Invalid Input'
        return render_template('viewFlight.html', error=error)


@app.route('/searchCustomer', methods=['GET', 'POST'])
@staff_only
def searchCustomer():
    username = session['username']
    cursor = conn.cursor();
    flight_num = request.form['Flight_Number']
    Departure_Date = request.form['Departure_Date']
    Departure_Time = request.form['Departure_Time']

    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Working.username =  %s ' \
            'and Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
            'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'

    cursor.execute(query, (username))
    data = cursor.fetchall()

    query = 'Select of.flight_num,customer.email, customer.first_name, customer.last_name ' \
            'From customer natural join purchase ' \
            'join of on of.id_num_ticket = purchase.id_num ' \
            'join Working on Working.name = of.name ' \
            'where Working.username = %s and of.flight_num = %s and of.dept_date = %s and of.dept_time = %s'

    cursor.execute(query, (username, flight_num, Departure_Date, Departure_Time))
    data1 = cursor.fetchall()

    cursor.close()
    if (data1):
        return render_template('viewFlight.html', posts2=data1, posts=data)
    else:
        # returns an error message to the html page
        error = 'Invalid Input'
        return render_template('viewFlight.html', error=error)


@app.route('/createFlight')
@staff_only
def createFlight():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT DISTINCT dept_date,dept_time,flight_num,dept_airport,arri_date,arri_time,base_price,flight_status,arri_airport ' \
            'FROM Working Natural JOIN Flight ' \
            'WHERE Working.username =  %s ' \
            'and Flight.dept_date >= (select CURDATE()) or ( Flight.dept_date = (select CURDATE()) and Flight.dept_time > (select CURTIME())) ' \
            'and Flight.dept_date <= (SELECT DATE_ADD(CURDATE(), INTERVAL 30 DAY))'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('createFlight.html', posts=data)


@app.route('/newFlight', methods=['GET', 'POST'])
@staff_only
def newFlight():
    username = session['username']
    cursor = conn.cursor()
    id_num = request.form['id_num']
    dept_date = request.form['dept_date']
    dept_time = request.form['dept_time']
    flight_num = request.form['flight_num']
    dept_airport = request.form['dept_airport']
    arri_date = request.form['arri_date']
    arri_time = request.form['arri_time']
    base_price = request.form['base_price']
    flight_status = request.form['flight_status']
    arri_airport = request.form['arri_airport']

    query0 = 'SELECT * ' \
             'FROM maintainance natural join Working ' \
             'WHERE username = %s and id_num = %s ' \
             'AND (((start_date < %s) OR (start_date = %s AND start_time <= %s)) ' \
             'AND ((end_date > %s) OR (end_date = %s AND end_time >= %s)) ' \
             'OR ((start_date < %s) OR (start_date = %s AND start_time <= %s)) ' \
             'AND ((end_date > %s) OR (end_date = %s AND end_time >= %s))) '
    cursor.execute(query0, (
        username, id_num, dept_date, dept_date, dept_time, arri_date, arri_date, arri_time, arri_date, arri_date,
        arri_time, dept_date, dept_date, dept_time))
    data0 = cursor.fetchall()
    if (not data0):
        try:
            query = 'INSERT INTO Flight (name, id_num, dept_date, dept_time, flight_num, dept_airport, arri_date, arri_time, base_price, flight_status, arri_airport) ' \
                    'VALUES((SELECT name FROM Working WHERE username = %s), %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(query, (
                username, id_num, dept_date, dept_time, flight_num, dept_airport, arri_date, arri_time, base_price,
                flight_status, arri_airport))

        except:
            cursor.close()
            error = 'Invalid Input'
            return render_template('createFlight.html', error=error)
        conn.commit()
        cursor.close()
        return redirect(url_for('createFlight'))
    else:
        cursor.close()
        error = 'Plane Under Maintenance Within the Time'
        return render_template('createFlight.html', error=error)


@app.route('/changeFlightStatus')
@staff_only
def changeFlightStatus():
    return render_template('changeFlightStatus.html')


@app.route('/changeStatus', methods=['GET', 'POST'])
@staff_only
def changeStatus():
    username = session['username']
    cursor = conn.cursor()
    flight_num = request.form['Flight_Number']
    Departure_Date = request.form['Departure_Date']
    Departure_Time = request.form['Departure_Time']
    status = request.form['Status']
    query = 'UPDATE Flight ' \
            'SET flight_status = %s ' \
            'WHERE flight_num = %s and dept_date = %s and dept_time = %s and name = (select name from Working where username = %s) '

    cursor.execute(query, (status, flight_num, Departure_Date, Departure_Time, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('changeFlightStatus'))


@app.route('/addAirplane')
@staff_only
def addAirplane():
    return render_template('addAirplane.html')


@app.route('/newAirplane', methods=['GET', 'POST'])
@staff_only
def newAirplane():
    username = session['username']
    cursor = conn.cursor()
    id_num = request.form['id_num']
    num_of_seats = request.form['num_of_seats']
    manu_company = request.form['manu_company']
    model_num = request.form['model_num']
    manu = request.form['manu_date']
    manu_date = datetime.strptime(manu, '%Y-%m-%d')
    current_date = datetime.now()
    age = current_date.year - manu_date.year - (
            (current_date.month, current_date.day) < (manu_date.month, manu_date.day))
    try:
        query = 'INSERT INTO AirPlane (name, id_num, num_of_seats, manu_company, model_num, manu_date, age) ' \
                'VALUES((SELECT name FROM Working WHERE username = %s), %s,%s,%s,%s,%s,%s)'
        cursor.execute(query, (username, id_num, num_of_seats, manu_company, model_num, manu_date, age))
    except:
        cursor.close()
        error = 'Invalid Input'
        return render_template('addAirplane.html', error=error)
    conn.commit()
    cursor.close()
    return redirect(url_for('viewAirplane'))


@app.route('/viewAirplane')
@staff_only
def viewAirplane():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT DISTINCT name,id_num,num_of_seats,manu_company,model_num,manu_date,age ' \
            'FROM Working Natural JOIN AirPlane WHERE Working.username = %s'

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewAirplane.html', posts=data)


@app.route('/addAirport')
@staff_only
def addAirport():
    return render_template('addAirport.html')


@app.route('/newAirport', methods=['GET', 'POST'])
@staff_only
def newAirport():
    username = session['username']
    cursor = conn.cursor()
    name = request.form['name']
    city = request.form['city']
    country = request.form['country']
    number_of_terminal = request.form['number_of_terminal']
    type = request.form['type']
    air_code = request.form['air_code']

    try:
        query = 'INSERT INTO Airport (air_code, name, city, country, num_of_terminal, type) ' \
                'VALUES(%s,%s,%s,%s,%s,%s)'
        cursor.execute(query, (air_code, name, city, country, number_of_terminal, type))
        query = 'INSERT INTO INSIDE (air_code, name) VALUES (%s, (SELECT name FROM Working WHERE username = %s))'
        cursor.execute(query, (air_code, username))
    except:
        cursor.close()
        error = 'Invalid Input'
        render_template('addAirport.html', error=error)
    conn.commit()
    cursor.close()
    return redirect(url_for('addAirport'))


@app.route('/viewFlightRatings')
@staff_only
def viewFlightRatings():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT of.flight_num, AVG(cus_comment.rate) as average_rating ' \
            'FROM of JOIN cus_comment ON of.id_num_ticket = cus_comment.id_num_ticket ' \
            'JOIN Working ON of.name = Working.name WHERE Working.username = %s ' \
            'GROUP BY of.flight_num'

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewFlightRatings.html', posts=data)


@app.route('/searchFlightRate', methods=['GET', 'POST'])
@staff_only
def searchFlightRate():
    username = session['username']
    cursor = conn.cursor()
    flight_num = request.form['Flight_Number']
    Departure_Date = request.form['Departure_Date']
    Departure_Time = request.form['Departure_Time']

    query = 'SELECT of.flight_num, of.dept_date, of.dept_time, cus_comment.comments, cus_comment.rate ' \
            'FROM cus_comment natural join of ' \
            'JOIN Working ON of.name = Working.name ' \
            'WHERE of.flight_num = %s and of.dept_date = %s and of.dept_time =%s and Working.username = %s'

    cursor.execute(query, (flight_num, Departure_Date, Departure_Time, username))
    data1 = cursor.fetchall()

    cursor.close()
    if (data1):
        return render_template('viewFlightRatings.html', posts2=data1)
    else:
        # returns an error message to the html page
        error = 'Invalid Input'
        return render_template('viewFlightRatings.html', error=error)


@app.route('/scheduleMaintenance')
@staff_only
def scheduleMaintenance():
    return render_template('scheduleMaintenance.html')


@app.route('/newMaintenance', methods=['GET', 'POST'])
@staff_only
def newMaintenance():
    username = session['username']
    cursor = conn.cursor()
    id_num = request.form['id_num']
    start_date = request.form['start_date']
    start_time = request.form['start_time']
    end_date = request.form['end_date']
    end_time = request.form['end_time']

    query = 'INSERT INTO maintainance (name, id_num, start_date, start_time, end_date, end_time) ' \
            'VALUES((SELECT name FROM Working WHERE username = %s), %s,%s,%s,%s,%s)'
    cursor.execute(query, (username, id_num, start_date, start_time, end_date, end_time))
    conn.commit()
    cursor.close()
    return redirect(url_for('scheduleMaintenance'))


@app.route('/viewFrequentCustomers')
@staff_only
def viewFrequentCustomers():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT email, COUNT(*) as flight_count ' \
            'FROM of natural JOIN Working ' \
            'JOIN purchase on purchase.id_num = of.id_num_ticket ' \
            'WHERE Working.username = %s and of.dept_date >= CURDATE() - INTERVAL 1 YEAR ' \
            'GROUP BY purchase.email ' \
            'ORDER BY flight_count DESC ' \
            'LIMIT 1 '

    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('viewFrequentCustomers.html', posts=data)


@app.route('/searchCustomerFlight', methods=['GET', 'POST'])
@staff_only
def searchCustomerFlight():
    username = session['username']
    cursor = conn.cursor()
    email = request.form['email']

    query = 'SELECT of.flight_num, of.dept_date, of.dept_time ' \
            'FROM of natural JOIN Working ' \
            'JOIN purchase ON of.id_num_ticket = purchase.id_num ' \
            'WHERE email = %s AND Working.username = %s '

    cursor.execute(query, (email, username))
    data1 = cursor.fetchall()

    cursor.close()
    if (data1):
        return render_template('viewFrequentCustomers.html', posts2=data1)
    else:
        # returns an error message to the html page
        error = 'Invalid Input'
        return render_template('viewFrequentCustomers.html', error=error)


@app.route('/viewEarnedRevenue')
@staff_only
def viewEarnedRevenue():
    username = session['username']
    cursor = conn.cursor()

    query_last_month = 'SELECT SUM(ticket_price) as last_month_revenue ' \
                       'FROM of natural join Working ' \
                       'join ticket on of.id_num_ticket = ticket.id_num ' \
                       'WHERE Working.username = %s and dept_date BETWEEN CURDATE() - INTERVAL 1 MONTH AND CURDATE()'
    cursor.execute(query_last_month, (username))
    last_month_revenue = cursor.fetchone()

    query_last_year = 'SELECT SUM(ticket_price) as last_year_revenue ' \
                      'FROM of natural join Working ' \
                      'join ticket on of.id_num_ticket = ticket.id_num ' \
                      'WHERE Working.username = %s and dept_date BETWEEN CURDATE() - INTERVAL 1 YEAR AND CURDATE()'
    cursor.execute(query_last_year, (username))
    last_year_revenue = cursor.fetchone()

    cursor.close()
    return render_template('viewEarnedRevenue.html', last_month_revenue=last_month_revenue,
                           last_year_revenue=last_year_revenue)


@app.route('/logoutStaff')
@staff_only
def logoutStaff():
    session.pop('username')
    return redirect('/')


@app.route('/cusMainPage')
@customer_only
def cusMainPage():
    username = session['username']
    return render_template('cusMainPage.html', username=username)


# Track Spending
@app.route('/track_spending', methods=['GET', 'POST'])
@customer_only
def track_spending():
    customer_email = session['username']

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        cursor = conn.cursor()

        if start_date and end_date:
            query = """
                SELECT MONTHNAME(p.date_purchase) AS month, SUM(t.ticket_price) AS total_spent
                FROM purchase as p, ticket as t
                WHERE p.email = %s AND p.date_purchase BETWEEN %s AND %s AND p.id_num = t.id_num
                GROUP BY MONTH(p.date_purchase)
                ORDER BY MONTH(p.date_purchase)
            """
            cursor.execute(query, (customer_email, start_date, end_date))
        else:
            query = """
                SELECT MONTHNAME(p.date_purchase) AS month, SUM(t.ticket_price) AS total_spent
                FROM purchase as p, ticket as t
                WHERE p.email = %s AND p.id_num = t.id_num AND p.date_purchase BETWEEN CURDATE() - INTERVAL 1 YEAR AND CURDATE()
                GROUP BY MONTH(p.date_purchase)
                ORDER BY MONTH(p.date_purchase)
            """
            cursor.execute(query, (customer_email,))

        spending_data = cursor.fetchall()
        cursor.close()

        if spending_data:
            return render_template('track_spending.html', spending_data=spending_data)
        else:
            return render_template('track_spending.html', message="No spending data found.")

    return render_template('track_spending.html')


# View My Flights
@app.route('/view_flights', methods=['GET', 'POST'])
@customer_only
def view_flights():
    customer_email = session['username']

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')

        cursor = conn.cursor()

        # Check which form was submitted and build the corresponding query
        if start_date is not None and end_date is not None:
            query = """
                SELECT DISTINCT flight.id_num, flight.name, flight.dept_date, flight.dept_time, flight.arri_date, flight.arri_time, flight.dept_airport
                , flight.arri_airport, flight.flight_status 
                FROM Flight join of on of.flight_num = flight.flight_num
	                        join purchase on of.id_num_ticket = purchase.id_num
                WHERE email = %s AND flight.dept_date BETWEEN %s AND %s
                ORDER BY flight.dept_date, flight.dept_time
            """
            cursor.execute(query, (customer_email, start_date, end_date))
        elif departure_airport is not None:
            query = """
                SELECT DISTINCT flight.id_num, flight.name, flight.dept_date, flight.dept_time, flight.arri_date, flight.arri_time, flight.dept_airport
                , flight.arri_airport, flight.flight_status 
                FROM Flight join of on of.flight_num = flight.flight_num
	                        join purchase on of.id_num_ticket = purchase.id_num
                WHERE email = %s AND flight.dept_airport LIKE %s
                ORDER BY flight.dept_date, flight.dept_time
            """
            cursor.execute(query, (customer_email, f"%{departure_airport}%"))
        elif arrival_airport is not None:
            query = """
                SELECT DISTINCT flight.id_num, flight.name, flight.dept_date, flight.dept_time, flight.arri_date, flight.arri_time, flight.dept_airport
                , flight.arri_airport, flight.flight_status 
                FROM Flight join of on of.flight_num = flight.flight_num
	                        join purchase on of.id_num_ticket = purchase.id_num
                WHERE email = %s AND flight.arri_airport LIKE %s
                ORDER BY flight.dept_date, flight.dept_time
            """
            cursor.execute(query, (customer_email, f"%{arrival_airport}%"))
        else:
            cursor.close()
            return render_template('view_flights.html', flights=None)

        flights = cursor.fetchall()
        cursor.close()

        return render_template('view_flights.html', flights=flights)

    return render_template('view_flights.html', flights=None)


# ---------------------
# Rate Comment
@app.route('/rate_comment', methods=['GET', 'POST'])
def rate_comment():
    def get_past_comments(customer_email):
        cursor = conn.cursor()
        cursor.execute("SELECT c.comments, c.rate FROM cus_comment c WHERE c.email = %s",
                       (customer_email,))
        past_comments = cursor.fetchall()
        cursor.close()
        return past_comments

    customer_email = session['username']

    if request.method == 'POST':
        flight_id = request.form['flight']
        rate_comment = request.form['cus_comment']
        rate = request.form['cus_comment_rating']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cus_comment (id_num_ticket, email, comments, rate) VALUES (%s, %s, %s, %s)",
                       (flight_id, customer_email, rate_comment, rate))
        conn.commit()
        cursor.close()

        return redirect(url_for('cusMainPage'))

    cursor = conn.cursor()
    cursor.execute("""
            SELECT distinct p.id_num, f.name 
            FROM Flight f
            JOIN of o ON f.id_num = o.id_num_ap and o.dept_date = f.dept_date
            JOIN ticket t ON o.id_num_ticket = t.id_num
            JOIN purchase p ON t.id_num = p.id_num
            LEFT JOIN cus_comment c ON o.id_num_ticket = c.id_num_ticket and c.email = %s
            WHERE f.arri_date < CURDATE() 
                AND (c.id_num_ticket IS NULL OR c.email <> %s)
                AND p.id_num NOT IN (SELECT id_num_ticket FROM cus_comment WHERE email = %s)
        """, (customer_email, customer_email, customer_email))
    flights = cursor.fetchall()
    cursor.close()

    past_comments = get_past_comments(customer_email)

    return render_template('rate_comment.html', flights=flights, past_comments=past_comments)


@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
    customer_email = session['username']
    cursor = conn.cursor()
    ticket_id = None

    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        try:
            cancel_trip_query = """
                DELETE FROM purchase
                WHERE email = %s AND id_num = %s
            """
            cursor.execute(cancel_trip_query, (customer_email, ticket_id))

            cancel_trip_query2 = """
                DELETE FROM of
                WHERE id_num_ticket = %s
            """
            cursor.execute(cancel_trip_query2, (ticket_id))

            # Delete from ticket
            cancel_trip_query3 = """
                DELETE FROM ticket
                WHERE id_num = %s
            """
            cursor.execute(cancel_trip_query3, (ticket_id))

            conn.commit()

            cursor.execute("""
            SELECT t.id_num
            FROM purchase t, of m
            WHERE m.id_num_ticket = t.id_num 
            AND m.dept_date - 1 > CURDATE() 
            AND t.email = %s
            """, (customer_email))
            flights = cursor.fetchall()
            cursor.close()

            return render_template('cancel_trip.html', flights=flights)

        except Exception as e:
            print(f"Error during cancellation: {str(e)}")
            conn.rollback()
            return "An error occurred during cancellation."

        finally:
            cursor.close()

    cursor.execute("""
            SELECT t.id_num
            FROM purchase t, of m
            WHERE m.id_num_ticket = t.id_num 
            AND m.dept_date - 1 > CURDATE()
            AND t.email = %s
        """, (customer_email))
    flights = cursor.fetchall()
    cursor.close()

    return render_template('cancel_trip.html', flights=flights)


@app.route('/search_flights', methods=['GET', 'POST'])
@customer_only
def search_flights():
    def find_actual_price(flight_id):
        cursor = conn.cursor()

        # Calculate taken seats
        taken_seats_query = """
            SELECT (Airplane.num_of_seats - COUNT(of.id_num_ap)) AS available_seat
            FROM of
            JOIN Airplane ON of.id_num_ap = Airplane.id_num
            WHERE of.id_num_ap = %s AND Airplane.id_num = %s
        """
        cursor.execute(taken_seats_query, (flight_id, flight_id))
        taken_seats_result = cursor.fetchone()

        if taken_seats_result is not None:
            taken_seats = taken_seats_result['available_seat']

            # Calculate actual price
            query = """
                SELECT flight_num, base_price * CASE
                    WHEN (%s / Airplane.num_of_seats) >= 0.8 THEN 1.25
                    ELSE 1
                END AS actual_price
                FROM Flight
                JOIN Airplane ON Flight.id_num = Airplane.id_num
                WHERE flight_num = %s;
            """
            cursor.execute(query, (taken_seats, flight_id))
            result = cursor.fetchone()

            if result is not None:
                actual_price = result['actual_price']
                return actual_price

        return None

    if request.method == 'POST':
        departure_airport = request.form.get('departure_airport')
        arrival_airport = request.form.get('arrival_airport')
        departure_date = request.form.get('departure_date')
        cursor = conn.cursor()

        query = """
            SELECT Flight.*, 
                   AirPlane.num_of_seats, 
                   (AirPlane.num_of_seats - COUNT(of.id_num_ticket)) AS available_seats
            FROM Flight
            LEFT JOIN AirPlane ON Flight.id_num = AirPlane.id_num
            LEFT JOIN of ON Flight.id_num = of.id_num_ap
            WHERE Flight.dept_airport = %s 
            AND Flight.arri_airport = %s 
            AND Flight.dept_date = %s
            GROUP BY Flight.id_num
            HAVING available_seats > 0
        """
        cursor.execute(query, (departure_airport, arrival_airport, departure_date))
        flights = cursor.fetchall()
        cursor.close()

        for flight in flights:
            actual_price = find_actual_price(flight['flight_num'])
            if actual_price is not None:
                flight['actual_price'] = actual_price
            else:
                flight['actual_price'] = 'N/A'

        if flights:
            return render_template('search_flights.html', flights=flights)
        else:
            return render_template('search_flights.html', message="No flights found.")

    return render_template('search_flights.html')


# Purchase Tickets
@app.route('/purchase_tickets', methods=['GET', 'POST'])
def purchase_ticket():
    def generate_unique_id(flight_id):
        return random.randint(1000, 9999)

    def is_unique_id(flight_id, id_num):
        cursor = conn.cursor()
        check_query = """
            SELECT id_num 
            FROM ticket
            WHERE id_num = %s
            UNION
            SELECT id_num_ticket
            FROM of
            WHERE id_num_ap = %s AND id_num_ticket = %s
        """
        cursor.execute(check_query, (id_num, flight_id, id_num))
        result = cursor.fetchone()
        cursor.close()
        return result is None

    def find_actual_price(flight_id):
        cursor = conn.cursor()

        # Calculate taken seats
        taken_seats_query = """
            SELECT (Airplane.num_of_seats - COUNT(of.id_num_ap)) AS available_seat
            FROM of
            JOIN Airplane ON of.id_num_ap = Airplane.id_num
            WHERE of.id_num_ap = %s AND Airplane.id_num = %s
        """
        cursor.execute(taken_seats_query, (flight_id, flight_id))
        taken_seats_result = cursor.fetchone()

        if taken_seats_result is not None:
            taken_seats = taken_seats_result['available_seat']

            # Calculate actual price
            query = """
                SELECT flight_num, base_price * CASE
                    WHEN (%s / Airplane.num_of_seats) >= 0.8 THEN 1.25
                    ELSE 1
                END AS actual_price
                FROM Flight
                JOIN Airplane ON Flight.id_num = Airplane.id_num
                WHERE flight_num = %s;
            """
            cursor.execute(query, (taken_seats, flight_id))
            result = cursor.fetchone()

            if result is not None:
                actual_price = result['actual_price']
                return actual_price

        return None

    if request.method == 'POST':
        flight_id = request.form.get('flight_id')
        passenger_name = request.form.get('passenger_name')
        customer_email = session['username']
        card_type = request.form.get('payment_type')
        card_num = request.form.get('payment_num')
        name_on_card = request.form.get('name_on_card')
        exp_date = request.form.get('expiration_date')
        date_purchase = datetime.now().date()
        time_purchase = datetime.now().time()
        id_num = generate_unique_id(flight_id)

        cursor = conn.cursor()

        while not is_unique_id(flight_id, id_num):
            id_num = generate_unique_id(flight_id)

        ticket_actual_price = find_actual_price(flight_id)

        insert_ticket_query = """
                            INSERT INTO ticket (id_num, ticket_price)
                            VALUES (%s, %s)
                        """
        cursor.execute(insert_ticket_query, (id_num, int(ticket_actual_price)))

        insert_of_query = """
            INSERT INTO of (name, id_num_ap, dept_date, dept_time, flight_num, id_num_ticket)
            SELECT name, id_num, dept_date, dept_time, flight_num, %s
            FROM Flight
            WHERE flight_num = %s
        """
        cursor.execute(insert_of_query, (id_num, flight_id))

        insert_query = """
                    INSERT INTO purchase (id_num, email, date_purchase, time_purchase, card_type, card_num, name_on_card, exp_date, passenger_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_query, (
            id_num, customer_email, date_purchase, time_purchase,
            card_type, card_num, name_on_card, exp_date, passenger_name
        ))

        conn.commit()
        cursor.close()

    return render_template('purchase_tickets.html')


@app.route('/logout')
@customer_only
def logout():
    session.pop('username')
    # this part needs to be edited to homepage
    return redirect('/')


@app.route('/unauthorized')
def unauthorized():
    if (session['staff']):
        return redirect('/staffMainPage')
    elif (session['customer']):
        return redirect('/cusMainPage')


app.secret_key = 'I do not know what key to use'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
