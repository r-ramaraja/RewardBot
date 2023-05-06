# RewardBot

**HokieTechies** <br/>
Dhruveel Chouhan - dhruveel10 <br/>
Fasi Ullah Khan - fasi <br/>
Ramaraja Ramanujan - ramaraja <br/>
Ramnath Raghu - rramnath <br/>
Shaunak Juvekar - jshaunak <br/>

To run the program, use the following command <br/>
flask -app app run -debug

To check the test cases,
1. Go

Use Case Diagrams <br/>
Automatically awarding points after a PR is merged <br/>
 ![SE](https://user-images.githubusercontent.com/66111178/236627111-e2fad205-8976-4a75-84cb-3cd85b221394.png)
 <br/>
The above diagram represents a Use Case where after an employee raises a PR and once it is merged, GitHub and Slack interact using webhooks. The points will be given to the employee and updated in the database. After this, the bot will post a message on the channel saying the employee XYZ has been awarded points for their ABC contribution.
