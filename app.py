#!/usr/bin/python3.6
import datetime
import os
import praw
import pytz
import requests
import time
import re
import accountdetails

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
    latest_video_id = str(re.compile(r'"videoId": "(.*?)"').search(str(latest_video)).group(1))
    latest_video_title = re.compile(r'"title": "(.*?)"').search(str(latest_video)).group(1)
    new_video = open('Leeham_Latest.txt', 'r+')
    previous_video_id = str(new_video.read())
    print('The ID Of The Previous Video Is {}'.format(previous_video_id),end='\n')
    print('The ID Of The Latest Video Is {}'.format(latest_video_id),
          end='\n {} \n'.format('------------------'))
    
    if latest_video_id != previous_video_id:
        print('Recording New Video id',
              end='\n {} \n'.format('------------------'))
        new_video.close()
        new_video = open('Leeham_Latest.txt', 'w')
        new_video.write('{}'.format(latest_video_id))
        new_video.close()
        return latest_video_id, latest_video_title
    else:
        print('No New Video Found', end='\n {} \n'.format('------------------'))
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


print('Logging In  To Reddit', end='\n {} \n'.format('------------------'))
reddit = praw.Reddit(user_agent='This is a thing that gives you stuff by /u/Zetaphor',
                         client_id=accountdetails.details['clientid'], client_secret=accountdetails.details['clientsecret'],
                         username=accountdetails.details['username'], password=accountdetails.details['password'])

sub = reddit.subreddit("Leeham")
mod = sub.mod
settings = mod.settings()

writeinfo()
sidebar_contents = settings['description']
new_sidebar = open('LeehamSidebar.txt', 'r').read()
LeehamInfo = open('LeehamInfo.txt', 'r').read()
new_sidebar = new_sidebar + LeehamInfo
sub.mod.update(description=new_sidebar)
latest_video_details = get_latest()
if latest_video_details != None:
    print('Submitting New Video', end='\n {} \n'.format('------------------'))
    sub.submit(latest_video_details[1], url='https://www.youtube.com/watch?v={}'.format(latest_video_details[0])).mod.distinguish(sticky=False)
    print('Done')





