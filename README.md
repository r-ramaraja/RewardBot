# RewardBot

**HokieTechies** <br/>
Dhruveel Chouhan - dhruveel10 <br/>
Fasi Ullah Khan - fasi <br/>
Ramaraja Ramanujan - ramaraja <br/>
Ramnath Raghu - rramnath <br/>
Shaunak Juvekar - jshaunak <br/>

<hr>
Use Case: Integrating our RewardBot with GitHub<br/>

Preconditions:<br/>
The employee should be present in the database.<br/>
The employee should have raised a PR.<br/>

Main Flow:<br/>
The bot will award the points to the employee who raised the PR once it is merged[S1]. The bot will also post a message on the common channel and will inform everyone about awarding the points[S2]. <br/>

Subflows:<br/>
[S1] Once the PR is merged, it automatically award points to the employee and will update the database.<br/>
[S2] It will post a message on the slack channel saying, Employee ABC has been awarded xyz points for their so and so contribution. <br/>
