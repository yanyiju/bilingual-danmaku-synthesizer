# Helper functions

from moviepy_opt_patch import *


class colors:
	"""Color used for printing."""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def apply_patch():
	"""Applies patch to increase speed when many clips are in one composition."""
	from moviepy.video.compositing import CompositeVideoClip as CVC
	from moviepy.video import VideoClip as VC
	CVC.CompositeVideoClip.make_frame = make_frame
	VC.VideoClip.new_blit_on = new_blit_on


def Dprint(message):
	"""Specific print func for this tool."""
	print(f"{colors.HEADER}[Danmaku message]{colors.ENDC} - {message}")


def Dwarn(message):
	"""Specific warning func for this tool."""
	print(f"{colors.WARNING}[Danmaku warning]{colors.ENDC} - {message}")


def Derror(message):
	"""Specific error func for this tool."""
	print(f"{colors.FAIL}[Danmaku error]{colors.ENDC} - {message}")
	