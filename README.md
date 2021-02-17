# Google Calendar Events to Google Tasks
*This project moves the calendar events into the default task list*

## Use Cases

To keep track and manage the completion of events. Sometimes calendars get exported as events and there is no way to tell if an event (I.E. homework) was completed or not 

## Pre-reqs
* Latest release of Python 3

## Setup

* Download this repository and save all the files into a folder

* Find the Calendar ID of the calendar you want to move to tasks (Settings of the calendar -> Calendar ID)

* Go to the [Google Calendar Api Website](https://developers.google.com/calendar/quickstart/python) and find the **Enable the Google Calendar API** button. Follow the steps and save the .json file as `credentialsCal.json` in your working folder

* Go to the [Google Tasks Api Website](https://developers.google.com/tasks/quickstart/python) and find the **Enable the Google Tasks API** button. Follow the steps and save the .json as `credentialsTask.json` in your working folder

* Run `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib` in the working folder

* Run `python3 driver.py` in the working folder

* Enter the calendar ID when prompted

