# import ffmpeg
import subprocess
import sys


def merge_video_audio(video_path, audio_path, outpath):
    proc = subprocess.Popen(
        f"ffmpeg -y -i {video_path} -i {audio_path} -c copy {outpath}", shell=True), #stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        