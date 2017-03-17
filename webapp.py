from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
import time
from slacker import OAuth as slack_oauth
from slacker import Slacker
import config
from bottasks import dispatch_event

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', client_id=config.SLACK_CLIENTID)

# SET THIS ENDPOINT IN SLACK APP configuration
@app.route("/slack/oauth")
def oauth():
    error = request.args.get('error')
    if error != 'access_denied':
        code = request.args.get('code')
        response = slack_oauth().access(config.SLACK_CLIENTID, config.SLACK_CLIENTSECRET, code)
        data = response.body
        if 'team_id' not in data:
            return redirect(url_for('home'), message="There was an error installing the app", message_class="error")

        # store somewhere:
        team_id = data['team_id']
        team_name = data['team_name']
        user_id = data['user_id']
        access_token = data['access_token']
        bot_user_id = data['bot']['bot_user_id']
        bot_access_token = data['bot']['bot_access_token']

        flash('App succesfully installed')

        return redirect(url_for('home'))
    else:
        flash('Access denied', 'error')
        return render_template('home.html', message="Access Denied", message_class="error")

#SLACK EVENT ENDPOINT
@app.route("/slack/events", methods=['POST'])
def slack_events():
    # check challenge
    if 'challenge' in request.json:
        return request.json['challenge']

    event = request.json
    #result = events_queue.enqueue(dispatch_event, event)

    dispatch_event.delay(event)

    # TODO: Log result
    return 'OK'
