from celery import Celery
import config
from celery.utils.log import get_task_logger
import time
import botutils
import Slacker
import commands

app = Celery('tasks', broker=config.CELERY_BROKER_URL)

logger = get_task_logger(__name__)


@botutils.listen_to('^i want (.*)$')
def want_something(slack_client, message, something=None):
    epoch = time.time()

    slack_client.chat.post_message(message['channel'], botutils.fast_reply(), as_user=True)

    commands.want_something(slack_client, message, something)

    # LOG the event here? maybe in Mixpanel?


@botutils.default_reply()
def default_reply(slack_client, message):

    answer = "Sorry but I didn't understand you. Type *help* for help."

    slack_client.chat.post_message(message['channel'], answer, as_user=True)


@app.task(bind=True, default_retry_delay=0.1)
def dispatch_event(self, event):
    epoch = time.time()
    team_id = event['team_id']

    if 'bot_id' not in event['event']:

        message = {
            'text': event['event']['text'],
            'user': event['event']['user'],
            'channel': event['event']['channel']
        }

        print event

        func, args = botutils.dispatcher(message['text'])

        logger.info('PARSED COMMAND: ' + str(func) + " type: " + command_type)

        # GET BOT ACCESS TOKEN FROM YOUR DATAABASE using team_id
        bot_access_token = 'XXX'
        sc = Slacker(bot_access_token)

        logger.info('message from :' + message['user'])

        # execute command
        try:
            func(sc, message, *args)

        # CATCH API or DATABASE EXCEPTIONS
        except Exception as err:
            logger.error('Problem with connection:' + unicode(err))
            self.retry(exc=err)
        # SOMETHING IS REALLY BROKEN! tell the user and log!
        except Exception as err:
            sc.chat.post_message(message['channel'], botutils.error_reply)
            raise

        logger.info('COMPLETED')
