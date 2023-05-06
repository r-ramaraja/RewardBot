def display_leaderboard(ack, body, client, mysql_connection):
    """Retrieves the top 10 performers and sends a message to the user"""

    ack()

    user = body["user_id"]

    mycursor = mysql_connection.cursor()
    sql = "SELECT full_name, points FROM employee ORDER BY points DESC LIMIT %s"
    val = (10, )
    mycursor.execute(sql, val)
    result = mycursor.fetchall()

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Leaderboard :sports_medal:",
                "emoji": True
            }
        },
        {
            "type": "divider"
        }
    ]

    # Construct the message blocks to send to the user
    for index, row in enumerate(result):

        text = f'{row[0]} - {row[1]} points'

        if index == 0:
            text = "🥇 " + text
        elif index == 1:
            text = "🥈 " + text
        elif index == 2:
            text = "🥉 " + text
        else:
            text = f"{index+1}. " + text

        blocks.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": text,
                "emoji": True
            }
        })

        blocks.append({
            "type": "divider"
        })

    client.chat_postMessage(channel=user, blocks=blocks)
