# RewardBot

[![Pylint](https://github.com/r-ramaraja/RewardBot/actions/workflows/pylint.yml/badge.svg)](https://github.com/r-ramaraja/RewardBot/actions/workflows/pylint.yml)
[![Pytest](https://github.com/r-ramaraja/RewardBot/actions/workflows/pytest.yml/badge.svg)](https://github.com/r-ramaraja/RewardBot/actions/workflows/pytest.yml)

## Description

RewardBot was developed as part of the course project  for CS5704 - Software Engineering at Virginia Tech in Spring '23'. RewardBot is a smart bot-based reward and recognition system for software engineering teams. It solves the problem of existing rewards and recognition systems which suffer from multiple flaws, including a lack of transparency, difficulty in quantifying rewards, and poorly defined actionable objectives. RewadBot is a Slack bot that utilizes gamification principles to recognize and reward employees effectively. RewardBot awards points based on individuals’ contributions to projects and their involvement in the open-source community. These accumulated points are displayed on a leaderboard and can be redeemed for various rewards, boosting employee motivation and fostering a healthy competitive environment.

## Team Info

Name: Hokie Techies  
Members:

- [Ramaraja Ramanujan](https://github.com/r-ramaraja) - ramaraja
- [Dhruveel Chouhan](https://github.com/dhruveel10) - dhruveel10
- [Shaunak Juvekar](https://github.com/shaunakjuvekar) - jshaunak
- [Fasi Ullah Khan Mohammed](https://github.com/fasikhan03) - fasi
- [Ramnath Raghu](https://github.com/rramnath-vt) - rramnath

## Setup

To setup and run the project locally, do the following,

- Clone the repository using `git clone https://github.com/r-ramaraja/RewardBot.git`
- Setup Python virtual environment,
  
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

- Install the dependencies using `pip install -r requirements.txt`
- Create and setup a Slack app. Refer [here](https://github.com/r-ramaraja/RewardBot/wiki/Slack-App-Setup) for more details.
- Setup a MySQL server and create a database. Refer [here](https://dev.mysql.com/doc/mysql-getting-started/en/) for more details.
- Populate the [.env](.env) file with the MySQL server details.
- Run the SQL script given [here](data/tables.sql) to create the required tables.
- We are assuming that the employee details are already in the DB. So, insert a few employee records into the `employee` table. Eg.
  
```sql
INSERT INTO employee 
VALUES ('Ramaraja Ramanujan', 'r-ramaraja', 'U04SNJYHQ6P', 0);
```

- To find the slack id of a user, do the following,
  - Open the user's full profile in Slack
  - Click on the vertical ellipsis (⋮) in the top right corner
  - Click on `Copy member ID`
- Run the project using `flask --app app run --debug --port <port_number>`. Eg. `flask --app app run --debug --port 8081`
- Use `ngrok` to expose the local server to the internet. `ngrok http <port_number>`. Eg. `ngrok http 8081`. Refer [this](https://ngrok.com/docs#getting-started-expose) for more details.
- You should be good to go now. You can interact with the bot in Slack!

## Tests

To run the tests, do the following,

- Install the dependencies using `pip install -r requirements.txt`
- Run the tests using `pytest` from the root directory
