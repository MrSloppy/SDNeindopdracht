# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import psycopg2

# create the application object
app = Flask(__name__)
def credentialChecker():
    #maak connectie met de database
    with open("wachtwoord.txt", "r") as passwordFile:
        passwordDatabase = passwordFile.readlines()
        print(passwordDatabase[0])

    conString=("dbname='sdn' user='sdn' password='{}' host='84.24.206.147' port='5432'").format(passwordDatabase[0])

    try:
        conn = psycopg2.connect(conString)
        print("CONNECTION TO THE DB ESTABLISHED.")
    except:
        print("I am unable to connect to the database.")
    cur = conn.cursor()
    cur.execute("select (case when password = 'Welkom01' AND username = 'Timo' THEN 0 else 1 end) from customerinfo where username = 'Timo'")

#def


# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Dit zijn de variabelen zoals ze uit de form komen
        print("bedrijfsnaam = "+request.form['companyName'])
        print("username = "+request.form['username'])
        print("password = "+request.form['password'])
        print("outletID = "+request.form['outletID'])

        bedrijfsNaam = request.form['companyName']
        username = request.form['username']
        password = request.form['password']
        outletID = request.form['outletID']

        if credentialChecker() is True:
            print("Succesfully logged in")
            # Hier moet de functie komen om de flows te maken
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
