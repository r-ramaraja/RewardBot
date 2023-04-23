from flask import json
from flask import request 
import requests
from flask import jsonify
from flask import Flask
import os
from pathlib import Path
import pymysql
from dotenv import load_dotenv

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

web_hook = os.getenv('web_hook')

conn= pymysql.connect(
    host= os.getenv('host'),
    user= os.getenv('user'),
    password= os.getenv('password'),
    db= os.getenv('db'),
    charset= 'utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
mycursor=conn.cursor()


@app.route('/github', methods=['POST'])
def github():
    if request.headers['Content-Type']=='application/json':
            
        resp = request.json
        
        action = resp['action']

        if (action == 'closed' and resp['pull_request']['merged']):
            #extracting the username from the pull request so that points can be awarded to that user
            pr = resp['pull_request']   
            base = pr['base']
            repo = base['repo']
            owner = repo['owner']
            login = owner['login']
            print('login:' ,login, '\n \n \n')
            
            #updating the database
            with conn.cursor() as cursor:
                sql = "UPDATE EMP SET points = points + 20 WHERE ID = %s"
                val = login
                cursor.execute(sql, val)
                conn.commit()
                
                #using the slack webhook to display the messages on the Slack Channel
                slack_msg = {'text': '20 points are rewarded to the employee', 'id':login}
                requests.post(web_hook, data=json.dumps(slack_msg))
                id_msg = {'text': login}
                requests.post(web_hook, data=json.dumps(id_msg))
    return 200    
if __name__=='__main__':
    app.run()
