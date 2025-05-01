# Master of Jokes

## Documentation

This section aims to explain our team's decision and assumptions

### Design

During the implementation of the "Joke List" page, we were unsure of
of whose jokes to display (i.e, only not authored or all), so we made a
decision to include all jokes. There a user can view all jokes, update
and delete ones that he/she owns and rate and take (if possible) ones that
he/she does not.

#### Front End

Master of Joke uses Flask (with Jinja templates) to serve the majority
of the Front End. The Status Page (and subsequent pages) uses React.

##### Instruction

To run the Front end, make sure you are in the `fe` folder.

`cd ./fe/`

Once you are in the `fe` folder, run the following commands:

`npm i` and `npm start`

> Note: > `npm i` install all the node modules,
> and `npm start` to start the Front end application.

#### Back End

Master of Jokes uses Flask to serve all of the API endpoints for the
application.

##### Instruction

To run the Back end, make sure you are in the root folder,
i.e. `master-of-jokes` folder.

Once you are in the root folder, run the following commands:

`. .venv/bin/activate` and `flask --app moj run`

> Note: `. .venv/bin/activate` activates python virtual
> environment and `flask --app moj run` starts the Back end application
>
> > Add `host=0.0.0.0` to the end `flask ...` command to expose
> > the application to the network.

> Note: run `flask --app moj add-moderator` to create an admin with
> `testadmin` username and `Test123` password.
