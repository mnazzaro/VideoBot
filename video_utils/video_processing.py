from moviepy.editor import *
from moviepy.video.fx import crop
import random

def trim (vid: VideoFileClip, start_time: float, end_time: float) -> VideoFileClip:
    return vid.subclip(start_time, end_time)
    
def random_clip (vid_fpath: str, duration_sec: float) -> VideoFileClip:
    vid = VideoFileClip(vid_fpath)
    l = vid.duration
    if duration_sec > l:
        return vid
    start_time = random.random() * (l - duration_sec)
    trimmed = trim (vid, start_time, start_time + duration_sec)
    middle = (trimmed.w / 2, trimmed.h / 2)
    return crop.crop(trimmed, x_center = middle[0], y_center = middle[1], width=607.5, height=1080)

if __name__=='__main__':
    random_clip('mc_parkour.mp4', 'mc_parkour_clip.mp4', 60)
