from services import leaderboard_service


def construct_leaderboard_events(app, mysql_connection):

    @app.command("/leaderboard")
    def handle_reward_command(ack, body, client):
        """Handle response to leaderboard Slack slash command"""

        leaderboard_service.display_leaderboard(
            ack, body, client, mysql_connection)

    return app
