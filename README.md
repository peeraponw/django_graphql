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
3) Please note that this repo includes an example database. It would be nice to backup the `db.sqlite3` making further progress.

## Completed work
### Create user
Run the following command in GraphiQL
```
mutation {
  createUser (
    username: "{username}",
    password1: "{password}",
    email: "{email}"
  ) {
    user{
        id
        username
        email
    }
  }
}
```
where `{username}`, `{password}`, and `{email}` are strings of your choice. 
### Obtain Token
To authenticate the any action by a user, a token which belongs to the correspodning user is required. This token can be obtained by the following command
```
mutation {
  obtainToken (
    username: {username},
  	password: {password},
  ) {
    token
  }
}
```
where `{username}` and `{password}` are the username and password of the corresponding user. This method is complete only if the user has already been created and the given `{username}` and `{password}` match each other. This command returns token of the user which is used for authenticated query.

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

### Clock In / Clock Out
With the authenticated header as `Me` query, the `ClockIn` and `ClockOut` mutations can be requested accordingly as follows:

```
mutation{
    clockIn{
        user{
            username
        }
        clock{
            clockedIn
        }
    }
}
```
```
mutation{
    clockOut{
        user{
            username
        }
        clock{
            clockedIn
            clockedOut
        }
    }
}
```
The `ClockIn` allows the user to create a new record and save the their current timestamp while the `ClockOut` finds the latest record which has already been clocked in but not yet clocked out. Please note that this version does not include fail safe mechanisms, e.g., double clock in. 

### Current Clock
This query finds the `Clock` object which has been clocked in but not yet clocked out and provide its details. 
```
query {
    currentClock{
        user{
            username
        }
        clockedIn
        clockedOut
    }
}
```

### Clocked Hours
This query returns the amount of working hours of the authenticated user. This repo includes a example database to test this query. Please note that there is one record which has not been clocked out. The `today` hours may show differently.

```
query{
    clockedHours{
        today
        currentWeek
        currentMonth
    }
```

### Clocks (Bonus)
This query returns all clocks of all users.
```
query{
    clocks{
        user{
            username
        }
        clockedIn
        clockedOut
    }
}
```

### myClocks (Bonus)
This query returns all clocks of the authenticated user.
```
query{
  myClocks{
    user{
      username
    }
    clockedIn
    clockedOut
  }
}