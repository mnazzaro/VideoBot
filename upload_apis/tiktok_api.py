from tiktok_uploader.upload import upload_video, upload_videos
from tiktok_uploader.auth import AuthBackend

import os


def upload (video_path:str, description: str, browser: str):
    upload_video(filename=video_path, cookies='/home/markn/Documents/RedditBot/cookies.txt', 
                  description=description, browser=browser)

if __name__=='__main__':
    upload('tiktok_churn/0/0.mp4', 
           'Wait this is actually so wholesome #reddit #redditstories #funnyvideo #funnystory #wholesome',
           'chrome')