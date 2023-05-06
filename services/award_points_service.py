from datetime import datetime
import os
import mysql
import requests
from dotenv import load_dotenv

load_dotenv()

awards = {
    "mastermind": {
        "label": "Mastermind",
        "emoji": ":brain:",
        "points": 100
    },
    "mvp": {
        "label": "Wizard",
        "emoji": ":magic_wand:",
        "points": 50
    },
    "rising_star": {
        "label": "Rising Star",
        "emoji": "🌟",
        "points": 25
    }
}


def award_points(ack, client, body):
    """Returns a modal asking the user to submit details of the award,\
          award recipient and message"""

    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "reward_modal",
            "title": {
                "type": "plain_text",
                "text": "RewardBot",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Spotlight",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "select_user",
                    "dispatch_action": True,
                    "element": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user to reward",
                            "emoji": True
                        },
                        "action_id": "users_select-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Select award recipient",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "dispatch_action": True,
                    "block_id": "award",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                                "text": "Select an award",
                                        "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Mastermind",
                                    "emoji": True
                                },
                                "value": "mastermind"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Most Valuable Player (MVP)",
                                    "emoji": True
                                },
                                "value": "mvp"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Rising Star",
                                    "emoji": True
                                },
                                "value": "rising_star"
                            }
                        ],
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Award",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "reward_message",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "message",
                        "min_length": 5,
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Message",
                        "emoji": True
                    }
                }
            ]
        }
    )


def validate_award(ack, body, view, mysql_connection):
    """Validates that the award recipient is not the awarder and \
        that the awarder has not awarded the recipient more than three times in a quarter"""

    awardee = view["state"]["values"]["select_user"]["users_select-action"]["selected_user"]
    awarder = body["user"]["id"]
    award = view["state"]["values"]["award"]["static_select-action"]["selected_option"]["value"]
    message = view["state"]["values"]["reward_message"]["message"]["value"]

    mycursor = mysql_connection.cursor()

    # Retrieve the number of times the awardee has received awards from awarder
    #  in the current quarter
    sql = "SELECT COUNT(*) FROM audit WHERE awardee = %s AND awarder = %s \
        AND QUARTER(award_date) = %s"
    val = (awardee, awarder, (datetime.now().month+2)//3)
    mycursor.execute(sql, val)
    count = mycursor.fetchone()[0]
    mycursor.close()

    errors = {}

    if awardee == awarder:
        errors["select_user"] = "You cannot award yourself!"

    if count >= 3:
        errors["select_user"] = "You cannot award a person more than three times in a quarter!"

    # If there are errors, acknowledge the submission and show the errors in the modal
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return {}

    ack()

    return {
        "awardee": awardee,
        "awarder": awarder,
        "award": awards[award]["label"],
        "points": awards[award]["points"],
        "emoji": awards[award]["emoji"],
        "message": message
    }


def send_award_message(client, award_info):
    """Sends a message to the public bot channel with the award details"""

    awardee = client.users_info(user=award_info["awardee"])[
        "user"]["real_name"]
    awarder = client.users_info(user=award_info["awarder"])[
        "user"]["real_name"]

    body = {
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                        "type": "plain_text",
                        "text": f'{award_info["award"]} Award {award_info["emoji"]}',
                        "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "plain_text",
                        "text": f'{awarder} just awarded {awardee}\
                            the {award_info["award"]} award!',
                        "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                        "type": "plain_text",
                        "text": award_info["message"],
                        "emoji": True
                }
            }
        ]
    }

    requests.post(
        os.environ.get("SLACK_WEBHOOK_URL"),
        json=body,
        timeout=5
    )


def store_points(award_info, mysql_connection):
    """Stores the award details in the database and creates an audit record"""

    mycursor = mysql_connection.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')

    try:

        # Rollback any previous transaction that was not committed
        if mysql_connection.in_transaction:
            mysql_connection.rollback()

        mysql_connection.start_transaction()

        sql1 = "UPDATE employee SET points = points + %s WHERE slack_id = %s"
        val1 = (award_info["points"], award_info["awardee"])
        mycursor.execute(sql1, val1)

        sql2 = "INSERT INTO audit (awarder, awardee, award, award_date) VALUES (%s, %s, %s, %s)"
        val2 = (award_info["awarder"], award_info["awardee"],
                award_info["award"], current_date)
        mycursor.execute(sql2, val2)

        mysql_connection.commit()

    except mysql.connector.Error as error:
        print(error)
        print("Error occurred during transaction. Rolling back changes.")
        mysql_connection.rollback()

    finally:
        mycursor.close()
