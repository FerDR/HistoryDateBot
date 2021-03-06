import wikipedia
import facebook
import time
import datetime
from numpy import random
import urllib.request
from pathlib import Path
import os

def upload_comment(graph, post_id, message="", img_path=None):
    if img_path:
        post = graph.put_photo(image=open(img_path, 'rb'),
                               album_path='%s/comments' % (post_id),
                               message=message)
    else:
        post = graph.put_object(parent_object=post_id,
                                connection_name="comments",
                                message=message)
    return post

def upload(message, access_token, img_path=None):
    graph = facebook.GraphAPI(access_token)
    if img_path:
        post = graph.put_photo(image=open(img_path, 'rb'),
                               message=message)
    else:
        post = graph.put_object(parent_object='me',
                                connection_name='feed',
                                message=message)
    return graph, post['post_id']

def getAccessToken(filename='access_token.txt'):
    return Path(filename).read_text().strip()

def get_date(use_timezones=True):
    dt = datetime.datetime.utcnow()
    timezone = None
    if use_timezones:
        timezone = random.randint(-12,15)
        dt+=datetime.timedelta(hours=timezone) 
    day = dt.day
    month = dt.month
    return day, month, timezone

def get_content(day, month):
    months = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    mon = months[month-1]
    title = mon+"_{}".format(day)
    page = wikipedia.page(title,auto_suggest=False)
    con = page.content
    con = con.split('== Events ==\n')[1]
    con = con.split('\n\n\n== References ==')[0]
    return con, title

def get_info(content):
    consplit = content.split('\n\n\n==')
    events = consplit[0].split('\n')
    births = consplit[1].split('==\n')[1].split('\n')
    deaths = consplit[2].split('==\n')[1].split('\n')
    holidays = consplit[3].split('==\n')[1].split('\n')
    r = random.rand()
    if r<0.65:
        event = events[random.randint(len(events))]
        return event, 'Event'
    elif r<0.80:
        birth = births[random.randint(len(births))]
        return birth, 'Birth'
    elif r<0.95:
        death = deaths[random.randint(len(deaths))]
        return death, 'Death'
    else:
        holiday = holidays[random.randint(len(holidays))]
        return holiday, 'Holiday'


def make_text(date, timezone, info, category):
    text = "Today is {} in timezone UTC{}\n\n".format(date.replace('_',' '),timezone)
    if category!='Holiday':
        try:
          year = int(info.split(' – ')[0])
        except:
          year = info.split(' – ')[0]
        fact = info.split(' – ')[1]
        text+="On this day in {}, {}".format(year,fact)
        if category=='Event':
            pass
        elif category=='Birth':
            text+=' was born.'
        elif category=='Death':
            text+=' died.'
    else:
        text+="Today's holiday is {}.".format(info)
    text = text.replace('Hitler','AN AUSTRIAN PAINTER')
    text = text.replace('Argentina', 'VAAAAMOS ARGENTINA CARAJO')
    return text

def get_article(title, info, category,debug=False):
    links = wikipedia.page(title).links
    if category!= 'Holiday':
        words = info.split(' – ')[1].split(' ')
    else:
        words = info.split(' ')
    if debug:
        print (words)
    if category=='Birth' or category=='Death':
        name = ''
        for i in range(max(5,len(words))):
            name += words[i]
            if debug:
                print(name)
            if name in links:
                return name
            if name[0:-1] in links:
                return name[0:-1]
            name+=' '

    if category=='Holiday' or category=='Event':
        for i in range(min(10,len(words))):
            name = ''
            for j in range(min(10-i,len(words)-i)):
                name+=words[i+j]
                if debug:
                    print(name)
                if name in links:
                    return name
                if name[0:-1] in links:
                    return name[0:-1]
                name+=' '

def get_image(link,debug=False):
    if debug:
        print(link)
    page = wikipedia.page(link,auto_suggest=True)
    im = page.images
    if not im:
        return 'nominal'
    img = [imgs for imgs in im if 'png' in imgs or 'jpg' in imgs or 'jpeg' in imgs] 
    url = img[np.random.randint(len(img))]
    form = url.split('.')[-1]
    urllib.request.urlretrieve(url, './image.{}'.format(form))
    return '/home/fer/Documents/Bots/Facebook/SegueBot/HistoryDateBot.{}'.format(form)
    return '/home/fer/Documents/Bots/Facebook/HistoryDateBot/image.{}'.format(form)

def main(debug=False):
    day,month,timezone = get_date()
    content, date = get_content(day,month)
    info, category = get_info(content)
    text = make_text(date,timezone,info,category)
    try:
        img_path = get_image(get_article(date,info,category,debug),debug)
    except:
        img_path = 'nominal'
        #img_path = '/home/fer/BotsFacebook/HistoryDateBot/nominal.png'
    if img_path=='nominal':
        if category=='Event' or category=='Holiday':
            img_path = '/home/fer/Documents/Bots/Facebook/HistoryDateBot/nominal.png'
        elif category=='Birth':
            img_path = '/home/fer/Documents/Bots/Facebook/HistoryDateBot/Birthday.jpeg'
        elif category=='Death':
            img_path = '/home/fer/Documents/Bots/Facebook/HistoryDateBot/Death.jpg'
    gr, p_id = upload(text,getAccessToken(),img_path)
    #print(text,img_path)
