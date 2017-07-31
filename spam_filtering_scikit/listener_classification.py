#!/usr/bin/env python
# -*- coding: utf-8 -*-

import switchboard
import thread
import email
from sqlalchemy import create_engine
from spam_filtering_scikit.classification import classification
import numpy as np


import argparse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ACCOUNT = 'tesinasicurezza@gmail.com'
CONN_SPEC = {'host': 'imap.gmail.com',
             'port': 993,
             'auth': {
                 'type': 'plain',
                 'username': ACCOUNT,
                 'password': 'computersecurity'}};

def count_words(line, dictionary):
    words = line.split()
    feature_vec = np.zeros(3000)
    for word in words:
        wordID = 0
        for i, d in enumerate(dictionary):
            if d[0] == word:
                wordID = i
                feature_vec[wordID] = words.count(word)
    return feature_vec


class ListenerWorker(switchboard.Fetcher):
    """
    A basic Switchboard worker that will listen for new email
    notifications.  When it receives a notification, it fetches the
    raw email from Switchboard and parses it using the email module.
    """

    def opened(self):
        """
        Connect to the websocket, and ensure the account is connected and
        the INBOX is being watched, and then start watchingAll.
        """
        def post_setup((cmds, resps)):
            """Post setup callback."""
            logger.info("Setup complete, listening...")

        self.send_cmds(('connect', CONN_SPEC),
                       ('watchMailboxes', {'account': ACCOUNT,
                                           'list': ['INBOX']}),
                       ('watchAll', {})).then(post_setup)

    def received_new(self, msg):
        """
        Called when a new message is received.
        """
        logger.info("Subject: %s, From: %s, To: %s",
                    msg['subject'], msg['from'], msg['to'])

        print "Payload: "+msg.get_payload()
        print classification(msg.get_payload())



def main(url):
    """Create, connect, and block on the listener worker."""
    try:
        listener = ListenerWorker(url)
        listener.connect()
        listener.run_forever()
    except KeyboardInterrupt:
        listener.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Loop echo listener")
    parser.add_argument("--url", default="ws://192.168.50.2:8080/workers")
    args = parser.parse_args()
    main(args.url)
