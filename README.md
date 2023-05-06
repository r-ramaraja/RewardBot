# RewardBot

**HokieTechies** <br/>
Dhruveel Chouhan - dhruveel10 <br/>
Fasi Ullah Khan - fasi <br/>
Ramaraja Ramanujan - ramaraja <br/>
Ramnath Raghu - rramnath <br/>
Shaunak Juvekar - jshaunak <br/>

To run the program you will have to do the following steps <br/>
1. Create a Slack channel
2. Go to https://api.slack.com/ and create an app for your channel
3. Go to Install App page and copy the given link and paste it against SLACK_BOT_TOKEN as a String in the env file.
4. Now click on Reinstall to Workspace button and select the channel that you RewardBot to be associated with. At the buttom of the page a Webhook URL would be generated, copy it and paste it env file for the variable SLACK_WEBHOOK_URL
5. Go to Basic Information page, copy and paste your Signing Secret in the env file. Scroll down and under App-Level Tokens click on Generate Tokens and Scope. Give a name to the token and select connections:write. Copy the link generate and paste it for SLACK_APP_TOKEN.
6. Now that we have our Slack environment setup, lets set our database.
7. In the data folder, we have our database schema. Use the schema and create a database and insert a few employees.
8. Keep the database server running.
9. In the env file, enter all the details about your database for the approriate variablex
10. Run the flask server using the command flask -app app run -debug
11. The localhost address generated after running the above command, paste it in your ngrok server and it will generate a new look that we will use to connect to webhooks.
12. The link generated by ngrok server, copy it and paste it 
13.
14.
15.



To check the test cases,
1. Go

Use Case Diagrams <br/>
Automatically awarding points after a PR is merged <br/>
 ![SE](https://user-images.githubusercontent.com/66111178/236627111-e2fad205-8976-4a75-84cb-3cd85b221394.png)
 <br/>
The above diagram represents a Use Case where after an employee raises a PR and once it is merged, GitHub and Slack interact using webhooks. The points will be given to the employee and updated in the database. After this, the bot will post a message on the channel saying the employee XYZ has been awarded points for their ABC contribution.
