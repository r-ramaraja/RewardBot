import services.leaderboard_service as leaderboard_service


def construct_leaderboard_events(app, mysql_connection):

    @app.command("/leaderboard")
    def handle_reward_command(ack, body, client):
        print(body)
        leaderboard_service.display_leaderboard(
            ack, body, client, mysql_connection)

    return app
