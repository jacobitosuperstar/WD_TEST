# WD_TEST

## ARCHITECTURE


## DATA MODELS


## INDEX

- [SET UP](#set-up)
  - [RUNNING THE APP](#running-the-app)
- [SERVICE DETAILS](#service-details)
  - [STACK USED](#stack-used)
  - [RUNNING THE TESTS](#running-the-tests)
  - [SCOPE AND LIMITATIONS](#scope-and-limitations)

# SET UP

## RUNNING THE APP

To user the application having docker installed in your computer is a must, and
you can download it from this [link][1]

to run the application locally, from the command line you can run the command
`docker-compose up` from this directory. To run the application as a background
or detached from the terminal window, you can run the command
`docker-compose up -d` or `docker-compose up --detach`.

To run commands inside the `web` service container you can run this while the
application is running.

`docker-compose exec web /bin/bash`

With this you will be able to be in the server environment and run magene
commands needed to execute the tests.

# SERVICE DETAILS

## STACK USED

Instead of using the recomended packages (flask or fastAPI), I opted for Django
to display the OOP paradigm in the creation of the backend, where I created a
`base` application on which I would store the base model of the application,
the base mixins and the base class based views covering all the CRUD
operations.

RabbitMQ was used as a message broker and task queue to distribute the
notifications to the different consumers.

Created two simple consumers using PIKA to easily intereact with the sended
messages.

For simplicity and ease of use, I used SQLite instead of a Postgress container
as the database..

## RUNNING THE TESTS

To run the tests, you have to enter to the bash environment in the `web`
service container, and now in that bash environment run `python manage.py test`
to execute all the tests, or if you want to run the tests of a single module
you can run `python manage.py test {module_name}`

the different modules that are present are:

- clients
- preferences
- notifications

Instead of having singular test for each of the functionalities of the CRUD, I
packed them in workflows of creation and listing and creation, update and
deletion.

When testing the notifications being send, even tho in the main service we get
a data stream as we move along the users, you could check the console of the
different consumers to see that they are getting the respected messages.

## SCOPE AND LIMITATIONS

Within the scope of the challenge, that was basically send notifications to the
clients regarding listings and offerings, depending of their prefered method of
contact (email or SMS), I took some liberties regarding the database schema and
the processes around the application, which are,

- The notification table just saves the message. The idea is that we are not
  going to save in the database to who and through what means the notification
  is going to be send. We normally would just log that information and use
  other means to analyze the logs.
- The notification endpoint, distributes the latest notification updated to all
  the clients and depending of the preference, the notification is send through
  both means, one or none. As the notifications are being send, we create a
  strem on which we send the message and the client to whom the notification
  was sended to.
- Even tho in this example the notifications are save the same(be SMS or
  email), from my experience, SMS messages are a charfield, because of the
  character limitations and email messages are a text field when saved. Because
  of it I used two different services to consume each type of message, and two
  queues to route them.
- Because of the fast startup time of the consumers, a 10 second delay was
  added so the rabbitMQ container can start before them.

[1]: https://www.docker.com
