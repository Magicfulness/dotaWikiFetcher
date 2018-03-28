import datetime

def days(beforeDate, afterDate = datetime.datetime.today(), form = "%d %m %Y"):
	beforeDate = datetime.datetime.strptime(beforeDate, form)
	timeDelta = afterDate - beforeDate
	return int(timeDelta.total_seconds()/86400)
