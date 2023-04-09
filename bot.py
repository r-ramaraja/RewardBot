import os
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
#from slack_sdk.errors import SlackApiError
import pymysql
#import threading

env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

SLACK_BOT_TOKEN="xoxb-4939757670293-5014373908853-bE5C4vhYVOyMkQy2hVzLa4Uy"
SLACK_APP_TOKEN="xapp-1-A050H5EGGEP-5105101526448-a75eff24384bb00c0260028b636c4b43a91cbf36df5410fa8e42fabc05747bcb"

app = App(token=SLACK_BOT_TOKEN, name="Hw Bot")

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
id = "dhruveel10"

@app.event("app_home_opened") #for now it will print on the slack channel everytime we refresh it
def say_hw(message, say):
    #i = i+1
    #say("hello world ")
    with conn.cursor() as cursor:
        mycursor.execute("SELECT * FROM emp")
        print_db = mycursor.fetchall()
        print(print_db)
        #ack()
        say("10 points is rewarded to the employee.") #here we will have to fetch the username via flask declared variable


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()