def construct_github_events(app):

    @app.event("message")
    def handle_message_events(body, logger):
        """Handle response to GitHub pull request merge message event"""

        logger.info(body)

    return app
