import requests
import re

def get_image(url):
    try:
        return re.findall('img src="(.+?)"',requests.get(url).text)[1]
    except:
        return 'https://socialistmodernism.com/wp-content/uploads/2017/07/placeholder-image.png'

print(get_image("https://www.foxnews.com/politics/white-house-defends-dhs-disinformation-board-not-sure-who-opposes-that-effort"))