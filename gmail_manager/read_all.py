from gmail import Gmail

g = Gmail()
g.login("tesinasicurezza", "computersecurity")
emails = g.inbox().mail()
for e in emails:
	e.fetch()
	print e.body
g.logout()

