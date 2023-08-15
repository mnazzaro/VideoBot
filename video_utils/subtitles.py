from typing import List, Dict, Optional, Tuple

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import math
from datetime import timedelta
import wave
from vosk import Model, KaldiRecognizer
import json

SAMPLE_RATE = 16000

def _format_timestamp (seconds: float) -> str:
    milliseconds = str(seconds - int(seconds))[2:5]
    hhmmss = str(timedelta(seconds=int(seconds)))
    return f'{hhmmss},{milliseconds}'

def _correct_script (true_script: str, word_times: List[Dict]):
    words = true_script.split()
    if len(words) != len(word_times):
        print ('script_correction failed')
        return
    # concerns = []
    # offset = 0
    # first pass to detect problems
    for i in range(len(words)):
        if words[i] != word_times[i]['word']:
            word_times[i]['word'] = words[i]
        # if i + offset >= len(word_times):
        #     break
        # if words[i] == word_times[i + offset]['word']:
        #     continue
        # if words[i] == word_times[i + 1]:
        #     offset += 1

def _generate_srt (word_times: List[Dict], caption_period: float) -> str:
    # total_time = word_times[-1]['end']
    srt = ""
    word_index = 0
    n_captions = 1
    n_words = len(word_times)
    while word_index < n_words:
        print (word_index)
        cur_cap = ''
        cur_cap_words = []
        cur_cap_start_time = word_times[word_index]['start']
        while word_index < n_words and (word_times[word_index]['end'] - cur_cap_start_time < caption_period or \
                                                len(cur_cap_words) == 0):
            cur_cap_words.append(word_times[word_index]['word'])
            word_index += 1
        cur_cap = str(n_captions)
        cur_cap += '\n'
        cur_cap += _format_timestamp(cur_cap_start_time)
        cur_cap += ' --> '
        if word_index == n_words:
            cur_cap += _format_timestamp(word_times[word_index - 1]['end'])
        else:
            cur_cap += _format_timestamp(word_times[word_index]['start'])
        cur_cap += '\n'
        cur_cap += ' '.join(cur_cap_words)
        cur_cap += '\n\n'
        n_captions += 1
        srt += cur_cap
    return srt

# def _generate_word_times (vosk_out: List[Dict], caption_period: float) -> List[Tuple[Tuple[int, int], str]]:
#     res = []
#     word_index = 0
#     n_captions = 1
#     while word_index < len(vosk_out):
#         cur_cap = ''
#         cur_cap_words = []
#         cur_cap_start_time = vosk_out[word_index]['start']
#         while word_index < len(vosk_out) and vosk_out[word_index]['end'] - cur_cap_start_time < caption_period:
#             cur_cap_words.append(vosk_out[word_index]['word'])
#             word_index += 1
#         res.append(((cur_cap_start_time, vosk_out[word_index - 1]['end']), ' '.join(cur_cap_words)))
#     return res
    
def generate_srt (script: str, audio_fpath: str, out_fpath: str, subtitle_len: float=0.5):
    model = Model(lang='en-us')
    wf = wave.open(audio_fpath, "rb")
    kr = KaldiRecognizer(model, wf.getframerate())
    kr.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if not len(data):
            break
        kr.AcceptWaveform(data)
    with open(out_fpath, 'w') as f:
        wt = json.loads(kr.FinalResult())['result']
        _correct_script(script, wt)
        srt = _generate_srt(wt, subtitle_len)
        print (srt)
        f.write(srt)
    return out_fpath

# def write_subtitles (word_times: List[Tuple[Tuple[int, int], str]], vid: VideoFileClip) -> CompositeVideoClip:
    # annotated_clips = [annotate(vid.subclip(from_t, to_t), txt) for (from_t, to_t), txt in word_times]
    # return concatenate_videoclips(annotated_clips)

# def generate_srt (word_times: List[Dict], words_per_caption: int, out_fpath: str):
#     n_captions = math.ceil(len(word_times) / words_per_caption)
#     with open(out_fpath, 'w') as f:
#         for i in range(n_captions):
#             cur_cap = str(i + 1)
#             cur_cap += '\n'
#             cur_cap += _format_timestamp(words_per_second * i)
#             cur_cap += ' --> '
#             cur_cap += _format_timestamp(words_per_second * (i + 1))
#             cur_cap += '\n'
#             cur_cap += ' '.join(words[i * words_per_caption: (i+1) * words_per_caption])
#             cur_cap += '\n\n'
#             f.write(cur_cap)
#     return out_fpath

def annotate(clip, srt_fpath, txt_color='white', fontsize=75, font='Xolonium-Bold', position='center'):
    generator = lambda txt: TextClip(txt, font=font, fontsize=fontsize, color=txt_color, method='caption', stroke_color='black', stroke_width=5)
    subs = SubtitlesClip(srt_fpath, generator)
    return CompositeVideoClip([clip, subs.set_pos(('center', position))])


if __name__=='__main__':
    print (_format_timestamp(6010.23452345))
    SAMPLE_RATE = 16000
    model = Model(lang='en-us')
    wf = wave.open('videos/0/0.wav', "rb")
    kr = KaldiRecognizer(model, wf.getframerate())
    kr.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if not len(data):
            break
        kr.AcceptWaveform(data)
    print (kr.FinalResult())