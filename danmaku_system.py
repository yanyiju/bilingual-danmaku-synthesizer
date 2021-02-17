import random

from moviepy.editor import *
from moviepy.video.io.ffmpeg_writer import ffmpeg_write_video
from danmaku import *
from danmaku_clip import *
from danmaku_channel import *
from constants import *

class DanmakuSystem(object):
	def __init__(self, video, configs):
		danmaku_configs = configs[DANMAKU]
		self.video = video
		self.channels = []
		self.coverage = danmaku_configs[COVERAGE]
		self.window_w = video.w
		self.window_h = video.h * min(self.coverage, 1)
		self.danmaku_configs = danmaku_configs
		channel_height = 8/3 * danmaku_configs[FONTSIZE]
		self.channel_num = int(self.window_h/channel_height)
		for i in range(self.channel_num):
			self.channels.append(DanmakuChannel(i, channel_height, self.window_w, channel_height * i))

	def generate_danmaku_clip_objects(self, danmaku):
		"""Builds clips for the given danmaku and assigns timestamps randomly."""
		timestamps = list(range(int(self.video.duration))) * self.channel_num
		timestamps = random.sample(timestamps, len(danmaku))
		timestamps.sort()
		random.shuffle(danmaku)
		danmaku_clips = []
		for i in range(len(danmaku)):
			danmaku_clips.append(DanmakuClip(danmaku[i], timestamps[i]))
		return danmaku_clips

	def fill_danmaku_and_get_clips(self, danmaku):
		"""Distributes danmaku into spare channels and forms danmaku animation."""
		danmaku_clips = self.generate_danmaku_clip_objects(danmaku)
		final_danmaku_clips = []
		for danmaku_clip in danmaku_clips:
			danmaku_clip.set_subclips(	self.danmaku_configs[FONTS], 
										self.danmaku_configs[FONTSIZE], 
										self.danmaku_configs[COMMENT_COLOR], 
										self.danmaku_configs[TRANSLATION_COLOR],
										self.window_w, 
										self.danmaku_configs[DURATION],
										self.danmaku_configs[BACKGROUND_RGB],
										self.danmaku_configs[BACKGROUND_OPACITY])
			for channel in self.channels:
				accepted = channel.accept_new_danmaku_clip(danmaku_clip)
				if accepted:
					danmaku_clip.set_animation((self.window_w, channel.pos_h), self.danmaku_configs[FPS])
					final_danmaku_clips.append(danmaku_clip)
					break
		return final_danmaku_clips

	def get_video_with_danmaku(self, danmaku, audio=None):
		"""Generates the final video with the new added danmaku."""
		danmaku_clips = self.fill_danmaku_and_get_clips(danmaku)
		clips_to_composite = [self.video] # used for final composition
		for danmaku_clip in danmaku_clips:
			start_time = danmaku_clip.timestamp
			clips_to_composite += [danmaku_clip.comm_clip.set_start(start_time), \
				danmaku_clip.tran_clip.set_start(start_time)]
			# self.video = CompositeVideoClip([self.video, 
			# 								danmaku_clip.comm_clip.set_start(start_time), 
			# 								danmaku_clip.tran_clip.set_start(start_time)])
		self.video = CompositeVideoClip(clips_to_composite)
		if audio:
			self.video = self.video.set_audio(audio)
		return self.video

	def get_danmaku_videos_with_mask(self, danmaku):
		"""Get all danmaku clips with alpha channel."""
		danmaku_clips = self.fill_danmaku_and_get_clips(danmaku)
		background = ColorClip(size =self.video.size, color =[0, 0, 0]).set_duration(1).set_fps(24)
		danmaku_videos = []
		for danmaku_clip in danmaku_clips:
			danmaku_video = CompositeVideoClip([background.set_opacity(0), 
												danmaku_clip.comm_clip, 
												danmaku_clip.tran_clip])
			danmaku_video.set_mask(danmaku_video.to_mask())
			danmaku_videos.append((danmaku_video, danmaku_clip.timestamp))
		return danmaku_videos
