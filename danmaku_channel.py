from danmaku import *
from danmaku_clip import *

class DanmakuChannel(object):
	def __init__(self, id, height, length, pos_h):
		self.id = id
		self.height = height
		self.length = length
		self.pos_h = pos_h
		self.last_danmaku_clip = None

	def accept_new_danmaku_clip(self, clip):
		"""Gives the result that if this channel can still accept new clips."""
		if not self.has_conflict(clip):
			self.last_danmaku_clip = clip
			return True
		return False

	def has_conflict(self, clip):
		"""Judges if the new clip will chase upto the last clip in this channel."""
		if self.last_danmaku_clip is None:
			return False
		t1 = self.last_danmaku_clip.timestamp
		l1 = self.last_danmaku_clip.w
		s1 = self.last_danmaku_clip.speed
		t2 = clip.timestamp
		s2 = clip.speed
		return s1 * (t2 - t1) < l1 or s2 * (t1 + (self.length + l1)/s1 - t2) >= self.length
