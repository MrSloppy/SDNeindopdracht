# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import requests
import psycopg2
import json
from jinja2 import Template

# create the application object
app = Flask(__name__)


def connectDatabaseChecker():
    #maak connectie met de database
    with open("wachtwoord.txt", "r") as passwordFile:
        passwordDatabase = passwordFile.readlines()
        print(passwordDatabase[0])
    #used to connect to databsae.
    conString=("dbname='sdn' user='sdn' password='{}' host='84.24.206.147' port='5432'").format(passwordDatabase[0])

    try:
        conn = psycopg2.connect(conString)
        print("CONNECTION TO THE DB ESTABLISHED.")
        return conn
    except:
        print("I am unable to connect to the database.")

def credentialChecker(password, username, conn):

    cur = conn.cursor()
    print(password, username)
    credString=("select (case when password = '{0}' AND username = '{1}' THEN 0 else 1 end) from customerinfo where username = '{1}'").format(password, username)
    print(credString)
    cur.execute(credString)
    feedback = cur.fetchall()
    print(feedback)
    if(feedback[0][0] == 0):
        return True

def CustomerInfoChecker(username, conn):
    cur = conn.cursor()
    CustomerInfoString=("select companyname, username, fsaccess, prntacces, leminutes, fsport from customerinfo where username = '{}'").format(username)
    cur.execute(CustomerInfoString)
    feedback = cur.fetchall()
    #print(feedback)
    #bedrijfsNaam = feedback[0][0]
    fsaccess = feedback[0][2]
    prntaccess = feedback[0][3]
    leminutes = feedback[0][4]
    userValues = {'bedrijfsNaam': feedback[0][0], 'fsaccess': feedback[0][2], 'prntaccess': feedback[0][3],'leminutes': feedback[0][4], 'fsport': feedback[0][5]}
    return userValues


def DevicePortmapper(outletnumber, conn):
    cur = conn.cursor()
    DevicePortMapperQueryString=("select * from devicemap where 11 IN (port1,port2,port3,port4)").format(outletnumber)
    cur.execute(DevicePortMapperQueryString)
    colnames =[desc[0] for desc in cur.description]
    values = cur.fetchall()
    #we need to map this to a dict/keyval store, because we fail at doing SQL properly...
    #also, totally unscalable thanks to not using loops. Should be fixed in the "newer" version!
    DevicekeyValue = {colnames[0] : values[0][0], colnames[1] : values[0][1], colnames[2] : values[0][2], colnames[3] : values[0][3],colnames[4] : values[0][4]}

    for key, value in DevicekeyValue.items():
        print(key)
        print(value)
        print(outletnumber)
        if value == outletnumber:
            output=[DevicekeyValue['deviceid'],key]
            return output
    return ValueError

def flowDataMaker(fsport):
    with open("testflowClientA.json", 'r')as jsonfile:
        data = json.load(jsonfile)
        print(data)
    data["flows"][2]["treatment"]["instructions"][0]["port"] = fsport
    data["flows"][3]["selector"]["criteria"][0]["port"] = fsport
    print(data)
    return data
    # if(outletID == 1):
    #     # Read JSON data into the datastore variable
    #     with open("Flows/Outlets/outlet_1_z1.json", 'r') as f:
    #         datastore = json.load(f)
    #         print(datastore)
    # if(outletID == 2):
    #     # Read JSON data into the datastore variable
    #     with open("Flows/Outlets/outlet_2_z1.json", 'r') as f:
    #         datastore = json.load(f)
    #         print(datastore)
    # if(outletID == 3):
    #     # Read JSON data into the datastore variable
    #     with open("Flows/Outlets/outlet_3_z2.json", 'r') as f:
    #         datastore = json.load(f)
    #         print(datastore)
    # else:
    #     print("Het lukt niet")
    # return(datastore)





def RestCall(fsport):
    #used to construct restcall. (ApiEndpoint is the api endpoint in ONOS, the method is either GET or REST, and the url is the base URL for API calls.
    #parameter example:
    #APIendpoint = /devices
    #url = http://<ip addr>/:8081/
    #data = post JSON data. (depends on the call you want to make, lookup swagger documentation for these values.
    #example:   print(RestCall('GET','http://192.168.122.229:8181', '/restconf/operational/XSQL:XSQL/',None,'username','password'))
    #if(Method == "GET"):
    #    response = requests.get(url + APIendPoint, auth=(username,password))
    ###    if(response.status_code != 200 ):
    #        raise ValueError("no valid API endpoint, returned an error.")
    #    else:
    #        return response
    #elif(Method == "POST"):
    url = 'http://10.0.1.130:8181/onos/v1/flows?appId={}'.format(fsport)
    print(url)
    data = flowDataMaker(fsport)
    print(data)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, data=json.dumps(data), auth=("onos", "rocks"), headers=headers)
        #if (response.status_code != 200):
            #raise ValueError("no valid POST Request, returned an error.")
        #else:
    print(response)
    return response





# use decorators to link the function to a url
@app.route('/')
def home():
    conn = connectDatabaseChecker()

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
        print(request.headers.get('X-Forwarded-For', request.remote_addr))
        bedrijfsNaam = request.form['companyName']
        username = request.form['username']
        password = request.form['password']
        outletID = request.form['outletID']
        clientIP = request.headers.get('X-Forwarded-For', request.remote_addr)

        conn = connectDatabaseChecker()

        try:
            if credentialChecker(password, username, conn) is True:
                print("Succesfully logged in")
                userValues = CustomerInfoChecker(username, conn)
                print(userValues)
                fsport = userValues["fsport"]
                print(fsport)
                RestCall(fsport)
                return render_template('welcome.html', username=username, userValues=userValues)
            else:
                error = 'Invalid Credentials. Please try again.'
        except:
                error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
