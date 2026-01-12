# Tic-Tac-Toe API

Serverless Tic-Tac-Toe API built with AWS Lambda and Python.

## Notes

### How to run your project (or where it is hosted)

https://tic-tac-toe.garifull.in/

### How much time you spent building the project

Aproximately I spend:
* 1 hour to build initial skeleton of the project using base python and sqllite
* 2 hours to refactor initial skeleton and tests
* 1 hour I spend on vide-coding UI
* 1 hour to spin up the project and deploy it to AWS.

### Any assumptions you made

I decided to use AWS serverless infrastructure to host the project becuase it is unusual approach for me but I wanted to experiment with it in scope of simple project.

### Any trade-offs you made

I would expect to have some authenticationa and ACL controls for accesing endpoints and games but I decided to keep it simple. Also I omitted the fac that amount of games stored in DynamoDB might be big so pagination is not implemented as far as it is quick project. 

### Any special/unique features you added

I decded to add UI despite it wasn't part of assessment task becuase to me it is always important to present the project to the user as a whole working application which you can try to use within just few clicks.

### Anything else you want us to know about

Never used AWS lambda before so I decided to use opprtunity to learn it during implementation of this project.

## Feedback

Despite it is a simple project I spend a few fun hours learning AWS lambda and serverless infrastructure.
