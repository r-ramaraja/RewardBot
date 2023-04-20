from flask import json
from flask import request 
import requests
from flask import jsonify
from flask import Flask
import os
from pathlib import Path
import pymysql

app = Flask(__name__)

#slack hook
web_hook = 'https://hooks.slack.com/services/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'

conn= pymysql.connect(
    host= 'localhost',
    user= 'root',
    password= 'apple mango',
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
            
            
            with conn.cursor() as cursor:
                sql = "UPDATE EMP SET points = points + 20 WHERE ID = %s"
                val = login
                cursor.execute(sql, val)
                conn.commit()
                mycursor.execute("SELECT * FROM EMP WHERE ID =  %s", val)
                myresult = mycursor.fetchall()
                print(myresult)
                
                #using the webooks print
                slack_msg = {'text': '20 points are rewarded to the employee', 'id':login}
                requests.post(web_hook, data=json.dumps(slack_msg))
                id_msg = {'text': login}
                requests.post(web_hook, data=json.dumps(id_msg))
        
        return 'login'
       
        
           # return 'ret'
if __name__=='__main__':
    app.run()