from gmail import Gmail

g = Gmail()
g.login("tesinasicurezza", "computersecurity")
emails = g.inbox().mail()
for e in emails:
	e.fetch()
	print e.__dict__.keys()
g.logout()

# ['body', 'delivered_to', 'fr', 'uid', 'thread', 'to',
#  'cc', 'labels', 'mailbox', 'attachments', 'headers',
#  'html', 'flags', 'sent_at', 'message', 'subject',
#  'thread_id', 'message_id', 'gmail']
