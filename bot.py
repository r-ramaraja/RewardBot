import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import mysql.connector


env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']


# message_counts = {}
reward_counts = {}

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.environ['DATABASE_PWD'],
  database="employee_database"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM EMPLOYEE_DETAILS")

# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)


# @slack_event_adapter.on('message')
# def message(payload):
#     event = payload.get('event',{})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')
#     if BOT_ID != user_id:
#         if user_id in message_counts:
#             message_counts[user_id]+=1
#         else:
#             message_counts[user_id] = 1
#         client.chat_postMessage(channel='#test', text=text)
    
# @app.route('/message-count', methods=['POST'])
# def message_count():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')
#     message_count = message_counts.get(user_id,0)
#     client.chat_postMessage(channel=channel_id, text=f"The message count of the user is: {message_count}")
#     return Response(), 200

@app.route('/start', methods=['POST'])
def bot_start():
    data = request.form
    user_name= data.get('user_name')
    channel_id = data.get('channel_id')
    channel_name = data.get('channel_name')
    print(data)
    if channel_name == "reward":
        client.chat_postMessage(channel=channel_id, text=f"Welcome to this channel {user_name}. You can provide your points to other employees by using the slash command /reward followed by the user_name and the reason you are awarding the points.\nExample) /reward <user_name> Helped me in solving a bug")
    else:
        client.chat_postMessage(channel=channel_id, text=f"Welcome to this channel {user_name}")
    return Response(), 200

@app.route("/reward", methods=["POST"])
def handle_command():
    # Get the text following the slash command
    data = request.form
    command_text = request.form["text"]
    user_name= data.get('user_name')
    channel_id = data.get('channel_id')
    channel_name = data.get('channel_name')
    employee_rewarded = command_text.split(" ", 1)[0]
    if len(command_text.split(" ", 1)) > 1:
        reward_reason = command_text.split(" ", 1)[1]
    else:
        reward_reason = ""

    # Process the command text here
    # ...
    # Respond to the user
    if channel_name == "reward":
        mycursor.execute("SELECT points FROM EMPLOYEE_DETAILS WHERE user_name = %s", (employee_rewarded,))
        user = mycursor.fetchone()
        if not employee_rewarded:
            client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nEmployee Name should not be empty! Please Enter a name. For more details, give the slash command /start")
        elif not user:
            client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nNo Such employee present. Try again")
        else:
            if user_name.lower() == employee_rewarded.lower():
                client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nYou should not reward points to yourself")
            elif reward_reason=="":
                client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nPlease Justify why you are giving the point")
            elif len(reward_reason.split(" ")) == 1:
                client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nOne word Justification is not sufficient. Please Elaborate the contribution")
            else:
                if user_name in reward_counts:
                    reward_counts[user_name]+=1
                else:
                    reward_counts[user_name] = 1
                reward_count = reward_counts.get(user_name,0)
                if(reward_count>3):
                    client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\nYou can give points only for a maximum number of 3 times.")
                else:
                    sql = "UPDATE EMPLOYEE_DETAILS SET points = %s WHERE user_name = %s"
                    val = (user[0]+20, employee_rewarded)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    client.chat_postMessage(channel=channel_id,text=f"Input Text received: {command_text}.\n20 points is rewarded to the employee '{employee_rewarded}'. The comment you gave is '{reward_reason}'")
    else:
        client.chat_postMessage(channel=channel_id,text="Wrong channel.If you are willing to reward another employee, use the reward channel")
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)


    #