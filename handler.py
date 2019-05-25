import json
import mechanize
import boto3
import datetime
import random

def fill(event, context):
    LOGIN_URL = 'https://industry.socs.binus.ac.id/learning-plan/auth/login'
    LOGBOOK_URL = 'https://industry.socs.binus.ac.id/learning-plan/student/log-book/insert'

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('logfill-table')

    response = table.get_item(
    Key={
            'id': '2001577604',
        }
    )

    # print(response)
    logbook_data = response['Item']
    username = logbook_data['id']
    password = logbook_data['password']

    # check datetime, if not saturday ors sunday, abort the function
    day_of_week = datetime.datetime.today().weekday()
    # if it's weekend
    if(day_of_week == 6 or day_of_week == 7):
        clock_in = '0'
        clock_out = '0'
        activity = 'off'
        description = 'off'
    #if it's weekday
    else:
        activity_dict = logbook_data['activity']
        
        clock_in = '7'
        clock_out = '18'

        # at the end of the day
        # these are just normal dictionary
        activity = random.choice(list(activity_dict))
        description = activity_dict[activity]

    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.addheaders = [('User-agent', 'Firefox')]

    # login to get session n shit
    br.open(LOGIN_URL)

    br.form = br.forms()[0]
    br.form['username'] = username
    br.form['password'] = password
    req = br.submit()

    # post stuff on logbook
    br.open(LOGBOOK_URL)

    br.form = br.forms()[2]
    br.form['clock-in'] = clock_in
    br.form['clock-out'] = clock_out
    br.form['activity'] = activity
    br.form['description'] = description
    br.submit()

    # send ses here!

    body = {
        "message": "yay mechanize working, but it's not done yet",
        "activity": activity,
        "description": description,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
