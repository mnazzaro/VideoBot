from typing import Optional
import os
import shutil
import argparse

from video_utils.subtitles import generate_srt, annotate
from video_utils.video_processing import random_clip
from reddit_scraper import filter
from services.qa_checks.script_checks import run_script_qa_checks
from services.qa_checks.video_checks import run_video_qa_checks
from services.gpt import create_caption
from services.tts import text_to_wav
from upload_apis.tiktok_api import upload

from moviepy.editor import AudioFileClip, CompositeAudioClip

def generate_videos (subreddit: str, root_fpath, sort_by: str = 'hot', period: Optional[str] = None, max_videos: int = 10, min_upvotes: int = 5000):
    scripts = filter(subreddit, max_videos, min_upvotes, sort_by, period)
    for i, t_script in enumerate(scripts):
        path = f'{root_fpath}/{i}'
        try:
            os.mkdir(path)
        except FileExistsError:
            shutil.rmtree(path)
            os.mkdir(path)
        script = run_script_qa_checks(t_script)
        audio = AudioFileClip(text_to_wav (script, os.path.join(path, 'audio.wav')))
        srt = generate_srt(script, os.path.join(path, 'audio.wav'), os.path.join(path, 'subtitles.srt'))
        vid = random_clip('/home/markn/Documents/RedditBot/mc_parkour.mp4', audio.duration)
        while run_video_qa_checks(vid):
            print ("Failed Video QA, resampling")
            vid = random_clip('/home/markn/Documents/RedditBot/mc_parkour.mp4', audio.duration)
        comp_audio = CompositeAudioClip([audio])
        vid.audio = comp_audio
        final = annotate(vid, srt, font='Super-Boys', fontsize=80)
        final.write_videofile(os.path.join(path, f'{i}.mp4'))
        yield create_caption(script)



# if __name__== '__main__':
#     generate_videos('tifu', 'videos', max_videos=10, min_upvotes=1000, sort_by='top', period='week')

                              
# arg parse
parser = argparse.ArgumentParser(
    description='generate',
)

parser.add_argument('dir', help='Output directory')
# parser.add_argument('fname', help='Output video name')

parser.add_argument('-r', '--subreddit')

parser.add_argument('-s', '--sort-by', 
                    help='hot, rising, top, etc.')

parser.add_argument('-p', '--period', 
                    help='period if sort by top (week, month, etc.)')

parser.add_argument('-m', '--min-upvotes')

args = parser.parse_args()

print (args.subreddit)

for caption in generate_videos(args.subreddit, args.dir, args.sort_by, args.period,  1, int(args.min_upvotes)):
    upload(os.path.join(args.dir, '0/0.mp4'), caption + ' #reddit #redditstories #funnyvideo #funnystory #storytime', 'chrome')

