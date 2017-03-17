import re
import random

commands = {
    'listen_to': {},
    'default_reply': None
}

error_reply = u"Sorry sir! I didn't find any results. Let me ask my boss for help and I'll come back to you."


def fast_reply():
    possible_answers = [
        #u"Yes!",
        u"Got it!",
        u"Your whises are my commands!",
        u"Let me fecth the data for you!",
        u"I'm going to make you a dataset you can't refuse! "
    ]
    answer = possible_answers[random.randint(0, len(possible_answers) - 1)]
    return answer


def listen_to(matchstr, flags=0):
    def wrapper(func):
        commands['listen_to'][re.compile(matchstr, flags)] = func
        return func

    return wrapper


def dispatcher(text):

    for matcher in commands['listen_to']:
        m = matcher.search(text)
        if m:
            args = m.groups()
            return commands['listen_to'][matcher], args
    '''
    for expr, func in commands['listen_to'].iteritems():
        matches = re.compile(expr).search(text)
        if matches:
            args = matches.groups()
            return func, args

    '''
    return None, None