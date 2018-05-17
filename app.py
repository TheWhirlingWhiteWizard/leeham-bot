#!/usr/bin/python3.6
import datetime
import os
import praw
import pytz
import requests
import time
import re

Info_Channel = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCpNooCUr-Q01rjgqxzjvztg&key=AIzaSyC4ucWTSN3s7d4KrqJ9ZOYZ-ezvzwTSGsg"
Info_Channel_2 = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCpNooCUr-Q01rjgqxzjvztg&maxResults=1&order=date&type=video&key=AIzaSyC4ucWTSN3s7d4KrqJ9ZOYZ-ezvzwTSGsg"

reallist = ['\"','{','}','\n',']']
sdata = requests.get(Info_Channel).content
latest_video = requests.get(Info_Channel_2).content
def get_sdata():
    viewcount = re.compile(r'"viewCount": "(.*?)"').search(str(sdata)).group(1)
    subscribers = re.compile(r'"subscriberCount": "(.*?)"').search(str(sdata)).group(1)
    videoCount = re.compile(r'"videoCount": "(.*?)"').search(str(sdata)).group(1)
    return viewcount, subscribers, videoCount


def get_latest():
    latest_video_id = re.compile(r'"videoId": "(.*?)"').search(str(latest_video)).group(1)
    latest_video_title = re.compile(r'"title": "(.*?)"').search(str(latest_video)).group(1)
    new_video = open('Leeham_Latest.txt', 'r+')
    if latest_video_id not in new_video.read():
        new_video.close()
        new_video = open('Leeham_Latest.txt', 'a+')
        new_video.write('\n {}'.format(latest_video_id))
        new_video.close()
        print('hey')
        return latest_video_id, latest_video_title
    else:
        return None
    new_video.close()


def writeinfo():
    info = get_sdata() 
    subscribers = '* Subscribers: ' + info[1]
    videos = '* Videos: ' + info[2]
    views = '* Views: ' + info[0]
    ValueList = ['\n',subscribers,videos,views]

    f = open('LeehamInfo.txt', 'w')
    for item in ValueList:
        f.write("%s\n" % item)
    f.close()







reddit = praw.Reddit(user_agent='This is a thing that gives you stuff by /u/Zetaphor',
                         client_id='sIqEEPr8jjRblQ', client_secret="DXEBpMvOYReGeoWdOULcyRgkfNw",
                         username='Leeham_Bot', password='6srZH0kO6lXIPs')

sub = reddit.subreddit("Leeham")
mod = sub.mod
settings = mod.settings()

writeinfo()
sidebar_contents = settings['description']
new_sidebar = open('LeehamSidebar.txt', 'r').read()
print (new_sidebar)
LeehamInfo = open('LeehamInfo.txt', 'r').read()
new_sidebar = new_sidebar + LeehamInfo
sub.mod.update(description=new_sidebar)
latest = get_latest()
if latest != None:
    sub.submit(latest[1], url='https://www.youtube.com/watch?v={}'.format(latest[0])).mod.distinguish(sticky=False)
    print('hey')





