import numpy as np

from danmaku import *
from moviepy.editor import *

class DanmakuClip(object):
	def __init__(self, danmaku, timestamp):
		self.danmaku = danmaku
		self.speed = 0
		self.comm_clip = None
		self.tran_clip = None
		self.timestamp = timestamp
		self.duration = 0
		self.w = 0
		self.h = 0
		self.pos_h = 0

	def set_subclips(self, fonts, fontsize, comm_color, trans_color, start_pos_w, duration, col_rgb, col_opacity):
		"""Builds text clip with danmaku effect based on given text string."""
		self.comm_clip = TextClip(self.danmaku.comment, fontsize=fontsize, color=comm_color, font=fonts[self.danmaku.language])
		self.tran_clip = TextClip(self.danmaku.translation, fontsize=fontsize, color=trans_color, font=fonts['cn'])
		self.update_size()
		if not col_rgb is None:
			self.comm_clip = self.comm_clip.on_color(color=col_rgb, col_opacity=col_opacity)
			self.tran_clip = self.tran_clip.on_color(color=col_rgb, col_opacity=col_opacity)
		self.duration = duration
		self.speed = (start_pos_w + self.w) / duration

	def update_size(self):
		"""Updates the clips' size after the clips are established."""
		width, height = 0, 0
		if not self.comm_clip is None:
			width = self.comm_clip.w
			height += self.comm_clip.h
		if not self.tran_clip is None:
			width = max(width, self.tran_clip.w)
			height += self.tran_clip.h
		self.w = width
		self.h = height

	def set_animation(self, start_pos, fps):
		"""Set new text clips with the danmaku effect."""
		(pos_w, pos_h) = start_pos
		self.pos_h = pos_h
		fun_comm_pos = lambda t : (pos_w - self.speed * t, pos_h)
		fun_tran_pos = lambda t : (pos_w - self.speed * t, pos_h + self.comm_clip.h)
		self.comm_clip = self.comm_clip.set_pos(fun_comm_pos).set_duration(self.duration).set_fps(fps)
		self.tran_clip = self.tran_clip.set_pos(fun_tran_pos).set_duration(self.duration).set_fps(fps)

