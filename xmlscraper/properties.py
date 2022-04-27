from xmlscraper.xmlscraper.settings import USER_AGENT
from datetime import datetime, timedelta

today = datetime.date(datetime.today() - timedelta(days = 1))
today_string = datetime.strftime(today, '%Y-%m-%d')
