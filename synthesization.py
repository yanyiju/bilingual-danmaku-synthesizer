from danmaku_system import *
from file_io import *

def synthesize(configs):
    """Main operation function."""
    # Load input files and background video
    danmaku, video, audio = read_files_and_video(configs)

    # Prepare danmaku overlaying
    danmakuSystem = DanmakuSystem(video, audio, configs)

    # Method 1: Write out the final video with moviepy (recommended)
    video = danmakuSystem.get_video_with_danmaku(danmaku)
    export_final_video(video, configs)

    # Method 2: Write out the final video with ffmpeg 
    # danmaku_videos = danmakuSystem.get_danmaku_videos_with_mask(danmaku)
    # export_final_video_ffmpeg(danmaku_videos, configs)
    