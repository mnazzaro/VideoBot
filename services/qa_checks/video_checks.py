from moviepy.editor import VideoFileClip
import numpy as np

def _check_for_duplicate_frames (clip: VideoFileClip) -> bool:
    duration = clip.duration
    sample_frames = (duration * 0.8, duration * 0.9)
    return np.array_equal(clip.get_frame(sample_frames[0]), 
                          clip.get_frame(sample_frames[1]))

def run_video_qa_checks (clip: VideoFileClip) -> bool:
    return _check_for_duplicate_frames(clip)
