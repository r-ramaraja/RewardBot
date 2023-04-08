from flask import json
from flask import request 
import requests
from flask import jsonify
from flask import Flask
import pymysql

app = Flask(__name__)


conn= pymysql.connect(
    host= 'localhost',
    user= 'root',
    password= 'pwd',
    db= 'mydb',
    charset= 'utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    #unix_socket= "/tmp/mysql.sock"
    #port= 5400
)
mycursor=conn.cursor()


@app.route('/')
def api_root():
    return 'Hello' 



@app.route('/github', methods=['POST'])
def github():
    if request.headers['Content-Type']=='application/json':
            
        
        resp= request.json
        
        action = resp['action']

        if (action == 'closed'):
            pr = resp['pull_request']   # next  5lines -> path to login i.e Github username
            base = pr['base']
            repo = base['repo']
            owner = repo['owner']
            login = owner['login']
            print('login:' ,login, '\n \n \n')
            #ret = json.dumps(resp, indent = 4)  #to check the contents of the dictionary
            #print ("ret-------\n",ret)
        
            with conn.cursor() as cursor:
                sql = "UPDATE EMP SET points = points + 10 WHERE ID = %s"
                val = login
                cursor.execute(sql, val)
                conn.commit()
                mycursor.execute("SELECT * FROM EMP WHERE ID =  %s", val)
                myresult = mycursor.fetchall()
                print(myresult)
        return 'ret'
       
        
           # return 'ret'
if __name__=='__main__':
    app.run()
