# RewardBot

[![Pylint](https://github.com/r-ramaraja/RewardBot/actions/workflows/pylint.yml/badge.svg)](https://github.com/r-ramaraja/RewardBot/actions/workflows/pylint.yml)
[![Pytest](https://github.com/r-ramaraja/RewardBot/actions/workflows/pytest.yml/badge.svg)](https://github.com/r-ramaraja/RewardBot/actions/workflows/pytest.yml)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=r-ramaraja_RewardBot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=r-ramaraja_RewardBot)

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
- Use `ngrok` to expose the local server to the internet. `ngrok http <port_number>`. Eg. `ngrok http 8081`. Refer [here](https://ngrok.com/docs#getting-started-expose) for more details.
- You should be good to go now. You can interact with the bot in Slack!

## Tests

To run the tests, do the following,

- Clone the repository using `git clone https://github.com/r-ramaraja/RewardBot.git`
- Setup Python virtual environment,
  
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

- Install the dependencies using `pip install -r requirements.txt`
- Run the tests using `pytest` from the root directory

## Features

### Leaderboard

The leaderboard feature allows users to see the top ten performers. The user issues a Slack slash command by typing `/leaderboard`, which prompts the RewardBot to retrieve the top ten performers and send the leaderboard as a direct message.

#### Use Case

Display the leaderboard showing the name of the top ten performers and their accumulated points.

#### Preconditions

- The employee should have the necessary permissions to interact with the bot.
- There should be valid entries in the database of the respective employees and their details.

#### Main Flow

The employee will invoke a slash command which will then trigger the Reward Bot [S1]. The Reward Bot will then show the leaderboard to the employee on a private channel [S2].

#### Sub Flow

[S1] Employee invokes the bot using the `/leaderboard` slash command.
[S2] The bot then sends a direct message containing the leaderboard of the top ten performers to the employee who invoked the command.

#### User Diagram

![Leaderboard User Diagram](https://drive.google.com/uc?id=1ca0ftlt0QLbxDLF-p23SiYqBsLNsh3-4)

You can view details about the other features [here](https://github.com/r-ramaraja/RewardBot/wiki/Features)

## Documentation

Project Proposal: [Link](docs/proposal.pdf)
Design Sketches: [Link](docs/design_sketches.pdf)
Final Report: [Link](docs/final_report.pdf)
Demo Presentation: [Link](docs/demo.pdf)

## Organization

```bash
├── LICENSE
├── README.md
├── app.py
├── .env
├── data
│   └── tables.sql
├── docs
│   ├── final-report.pdf
│   ├── proposal-design-sketch.pdf
│   └── proposal.pdf
├── requirements.txt
├── services
│   ├── __init__.py
│   ├── award_points_service.py
│   ├── github_integration_service.py
│   └── leaderboard_service.py
├── settings
│   └── mysql_settings.py
├── slack
│   ├── __init__.py
│   ├── award_points_events.py
│   ├── github_integration_events.py
│   └── leaderboard_events.py
└── tests
    ├── __init__.py
    └── test_leaderboard_service.py
```

- `app.py` is the entry point of the application.
- `data/tables.sql` contains the SQL script to create the required tables.
- `docs/` contains the documentation regarding the project (report, proposal, demo).
- `requirements.txt` contains the list of dependencies.
- `services/` contains the business logic of the application.
- `settings/` contains the settings for the application.
- `slack/` contains the Slack event handlers.
- `tests/` contains the unit tests for the application.
- `.env` contains the environment variables for the application.

## Workflows

- Pylint: [Link](https://github.com/r-ramaraja/RewardBot/actions/workflows/pylint.yml)
- Pytest: [Link](https://github.com/r-ramaraja/RewardBot/actions/workflows/pytest.yml)
- Sonar: [Link](https://sonarcloud.io/dashboard?id=r-ramaraja_RewardBot)

## Cloud Deployment

- Flask Service: https://rewardbot.onrender.com
- MySQL DB: https://cloud.cs.vt.edu/p/c-k7rk9:p-lj9rm/workload/deployment:rewardbot:mysql

Note: The MySQL DB deployed in cloud.cs.vt.edu is not running due to a `429 Too Many Requests` error. We believe this is a problem with cloud.cs.vt.edu and not our application. Since, the MySQL DB is not running, the Flask service in the cloud is not running either.
