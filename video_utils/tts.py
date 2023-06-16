import pyttsx3
import requests
from pydub import AudioSegment
from pydub.playback import play
from textwrap import wrap
import subprocess

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[11].id)

def generate_audio (script: str, out_fpath: str):
    engine.save_to_file(script, out_fpath)
    engine.say(script)
    engine.runAndWait()

def _mp3_2_wav (src_fpath: str, dst_fpath: str):
    AudioSegment.from_mp3(src_fpath).export(dst_fpath, format='wav')

def _speed_up (src_fpath: str, dst_fpath: str):
    subprocess.run(
        [
            'ffmpeg',
            '-i',
            src_fpath,
            '-filter:a',
            'atempo=1.5',
            dst_fpath,
            '-y'
        ]
    )

BRIAN_URL = 'https://api.streamelements.com/kappa/v2/speech?voice=Brian&text='
def generate_audio_brian (script: str, tmp_fpath: str, out_fpath: str):
    max_chars = 1000
    with open(tmp_fpath, 'wb') as f:
        for s in wrap(script, max_chars):
            req = requests.get(BRIAN_URL + s)
            f.write(req.content)
    _mp3_2_wav(tmp_fpath, tmp_fpath)
    _speed_up (tmp_fpath, out_fpath)
    return out_fpath

if __name__=='__main__':
    with open('hi.mp3', 'wb') as f:
        f.write(generate_audio_brian('hello my name is Brian', ''))