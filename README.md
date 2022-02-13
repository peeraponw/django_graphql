# django_graphql

This project is a part of AnyFactory Backend Engineer Interview. The goal is to build a **GraphQL API** to clock in and out.

## Installation running the server
1) Open Terminal and `cd` to the directory of your choice.
2) Clone the repository 
`git clone https://github.com/peeraponw/django_graphql.git`
3) Activate the virtual environment 
`source venv/bin/activate`
4) Install the requirements 
`pip install requirements.txt`

## Running server and GraphiQL
1) Run Django server
`python manage.py runserver`
2) Open a web-browser (e.g. Chrome, Firefox) and browse to 
`localhost:8000/graphql/`

## Completed work
### Create user
Run the following command in GraphiQL
```
mutation {
  createUser (
    username: "{username}",
    password1: "{password}",
    password2: "{password}",
    email: "{email}"
  ) {
    success
    errors
    refreshToken
    token
  }
}
```
where `{username}`, `{password}`, and `{email}` are strings  your choice. You will receive token as a long string as per success of the user creation.
### Obtain Token
To authenticate the any action by a user, a token which belongs to the correspodning user is required. This token can be obtained by the following command
```
mutation {
  obtainToken (
    username: {username},
  	password: {password},
  ) {
    success
    errors
    refreshToken
    token
  }
}
```
where `{username}` and `{password}` are the username and password of the corresponding user. This method is complete only if the user has already been created and the `{username}` and `{password}` match the user. This command returns token of the user which is used during the authenticated query.

### Me
To validate the authenticated GraphQL query, Postman is used in this process. A POST request can be fired to `localhost:8000/graphql/` with its **body** as a GraphQL query as follows:
```
query {
    me{
        username
    }
}
```
and **headers** with `KEY=Authorization` and `VALUE=JWT {token}` where `{token}` is obtained from the `obtainToken` query.

## TO-DOs
Clock in and Clock out functionalities shall be applied in the upcoming stage. These two commands will update `Clock` table which contains `clock_id`, `user`, `clockin` and `clockout` columns where `clock_id` is the primary key of this table.
### Clock In
Upon calling this command with autorization token (as specified in `Me` command), the following command can be called:
```
mutation{
    clockIn
}
```
This will first check if this user has any rows with data in `clockin` but no data in `clockout`, in other words, a running clock. If yes, update the `clockout` on that row with the current time or its `clockin` +8 hours, whichever is lower. This assumes that no user tries to cheat the system.
Once the `clockin` and `clockout` match, create another row with `clockin` of current time and no data in `clockout`.

### Clock Out
Upon calling this command with autorization token (as specified in `Me` command), the following command can be called:
```
mutation{
    clockOut
}
```
This command checks the latest row of the corresponding user whose `clockin` exists but not `clockout` and update the `clockout` with the current time. If there is no eligible row, i.e., the user has not yet clocked in before clocking out, this will return an error message.


### Current Clock
Upon calling this command with autorization token (as specified in Me command), the following command can be called:
```
query{
    currentClock{
        id,
        hours
    }
}
```
This command calculate the number of hours of the running clock by compaing the latest `clockin` and the current time.


### Clocked Hours
Upon calling this command with autorization token (as specified in Me command), the following command can be called:
```
query{
    clockedHours{
        today,
        currentWeek,
        currentMonth
    }
}
```
This command calculates the number of hours that the user has been clocked for today, current week, as well as current month. An aggregation function shall be used for this purpose.