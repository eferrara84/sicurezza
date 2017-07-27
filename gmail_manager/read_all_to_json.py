import pprint

from gmail import Gmail
import json


class Mailwrapper(Gmail):
    """
    Wrapper per selezionare i soli campi d'interesse dalle mail e salvarle in
    un file json
    """
    def __init__(self, gm):
        self.attachments = gm.attachments
        self.body = gm.body
        self.to = gm.to
        self.cc = gm.cc
        self.flags = gm.flags
        self.headers = gm.headers
        self.message_id = gm.message_id
        self.sent_at = gm.sent_at
        self.subject = gm.subject
        self.thread = gm.thread
        self.thread_id = gm.thread_id
        self.to_dict = {'attachments': gm.attachments,
                        'body': gm.body,
                        'to': gm.to,
                        'cc': gm.cc,
                        'flags': gm.flags,
                        'headers': gm.headers,
                        'message_id': gm.message_id,
                        'sent_at': str(gm.sent_at),
                        'subject': gm.subject,
                        'thread': gm.thread,
                        'thread_id': gm.thread_id}


if __name__ == '__main__':

    g = Gmail()
    g.login("tesinasicurezza", "computersecurity")
    emails = g.inbox().mail()
    mailist = []
    for e in emails[:10]:
        e.fetch()
        m = Mailwrapper(e)
        mailist.append(json.dumps(m.to_dict))
        # print e.body

    with open('data.json', 'w') as fp:
            json.dump(mailist,fp)
    g.logout()
