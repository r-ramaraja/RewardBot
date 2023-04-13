from slack_bolt import App,request
import os
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import pymysql
import threading

reward_counts = {}
lock = threading.Lock()

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = App(token=os.environ['SLACK_TOKEN'], signing_secret=os.environ['SIGNING_SECRET'])

BOT_ID = app.client.users_info(user=app.client.auth_test()['user_id'])['user']['id']

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password=os.environ['DATABASE_PWD'],
  database="employee_database")

mycursor = mydb.cursor()



@app.command("/start")
def bot_start(ack, body, logger):
    user_name = body['user_name']
    channel_id = body['channel_id']
    channel_name = body['channel_name']
    if channel_name == "reward":
        app.client.chat_postMessage(channel=channel_id, text=f'''Welcome to the reward channel {user_name}. 
        You can provide your points to other employees by using the slash command /reward followed by the user_name 
        and the reason you are awarding the points.\nExample) /reward <user_name> Helped me in solving a bug''')
    elif channel_name == "leaderboard":
        app.client.chat_postMessage(channel=channel_id, text=f'''Welcome to the leaderboard {user_name}. 
        You can display the leaderboard by using the slash command /show ''')
    else:
        app.client.chat_postMessage(channel=channel_id, text=f"Welcome to this channel {user_name}.")
    # Send an acknowledgement response to the Slack API
    ack()


@app.command("/show")
def bot_start(ack, body, logger):
    user_name = body['user_name']
    channel_id = body['channel_id']
    channel_name = body['channel_name']
    
    mycursor.execute( "SELECT * FROM EMPLOYEE_DETAILS order by points desc" )
    rows = mycursor.fetchall()
    max_length = 30
    app.client.chat_postMessage(channel=channel_id, text=f'''-----------------------------------------------------''')
    for row in rows:
        
        name_length = len(row[1])
        padding =  ' '*(max_length-name_length)
        name = row[1]+padding
        app.client.chat_postMessage(channel=channel_id, text=f'''{name} |  {row[2]} points  |
         \n-----------------------------------------------------''')

    # Send an acknowledgement response to the Slack API
    ack()

@ app.command("/reward")
def handle_command(ack, respond, command):
    # Get the text following the slash command
    user_name = command['user_name']
    channel_id = command['channel_id']
    channel_name = command['channel_name']
    command_text = command['text']
    employee_rewarded = command_text.split(" ", 1)[0]

    if len(command_text.split(" ", 1)) > 1:
        reward_reason = command_text.split(" ", 1)[1]
    else:
        reward_reason = ""

    # Process the command text here
    # ...
    # Respond to the user
    if channel_name == "reward":
        mycursor.execute(
            "SELECT points FROM EMPLOYEE_DETAILS WHERE user_name = %s", (employee_rewarded,))
        user = mycursor.fetchone()
        if not employee_rewarded:
            respond(
                f"Input Text received: {command_text}.\nEmployee Name should not be empty! Please Enter a name. For more details, give the slash command /start")
        elif not user:
            respond(
                f"Input Text received: {command_text}.\nI could not find '{employee_rewarded}' in our Employee Database. Try again")
        else:
            if user_name.lower() == employee_rewarded.lower():
                respond(
                    f"Input Text received: {command_text}.\nYou should not reward points to yourself")
            elif reward_reason == "":
                respond(
                    f"Input Text received: {command_text}.\nPlease Justify why you are giving the point")
            elif len(reward_reason.split(" ")) == 1:
                respond(
                    f"Input Text received: {command_text}.\nOne word Justification is not sufficient. Please Elaborate the contribution")
            else:
                mycursor.execute(
                    "SELECT attempts FROM audit WHERE user_name = %s", (user_name,))
                reward_count = mycursor.fetchone()[0]
                if(reward_count >= 3):
                    respond(
                        f"Input Text received: {command_text}.\nYou can give points only for a maximum number of 3 times.")
                else:
                    lock.acquire()
                    try:
                        sql = "UPDATE EMPLOYEE_DETAILS SET points = %s WHERE user_name = %s"
                        val = (user[0]+20, employee_rewarded)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        sql2 = "UPDATE audit SET attempts = %s WHERE user_name = %s"
                        val2 = (reward_count+1, user_name)
                        mycursor.execute(sql2, val2)
                        mydb.commit()
                        respond(
                            f"Input Text received: {command_text}.\n20 points is rewarded to the employee '{employee_rewarded}'. The comment you gave is '{reward_reason}'")
                    except SlackApiError as e:
                        print("Error: {}".format(e))
                    except pymysql.Error as e:
                        print("Error: {}".format(e))
                        mydb.rollback()
                    finally:
                        # Release lock when finished accessing database
                        lock.release()
    else:
        respond("Wrong channel.If you are willing to reward another employee, use the reward channel")

    ack()


if __name__ == "__main__":
    handler = SocketModeHandler(app = app, app_token=os.environ['SLACK_API_TOKEN'])
    handler.start()