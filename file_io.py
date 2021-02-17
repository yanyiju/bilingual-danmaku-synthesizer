import os
import sys
import json
import shutil
import subprocess

from moviepy.editor import *
from danmaku import *
from constants import *
from logistics import *

def read_files_and_video(configs):
	"""Reads files of comments or translation and generate list of danmaku objects."""
	input_configs = configs[INPUT]
	comm_files, tran_files = dict(), dict()
	file_path = input_configs[FILE_PATH]
	video_path = input_configs[VIDEO_PATH]
	if video_path is None:
		Derror("No video is assigned. Please assign video_path in the input configs.")
	for root, dirs, files in os.walk(file_path):
		for filename in files:
			Dprint("%s is detected and ready to process." % filename)
			[file_type, lang] = filename.split('.')[0].split('_')
			if not lang in languages:
				Dwarn("%s is not supported now, thus ignored." % lang)
			file = open(os.path.join(file_path, filename), 'r')
			if file_type == comments_file_type:
				comm_files[lang] = file
			elif file_type == translation_file_type:
				tran_files[lang] = file
			else:
				Dwarn("%s can not identified, thus ignored." % filename)
	danmakus = []
	for lang in comm_files.keys():
		comments = comm_files[lang].readlines()
		translation = []
		try:
			translation = tran_files[lang].readlines()
		except KeyError:
			Dwarn("No translation file found for language: %s." % lang)
		if len(comments) != len(translation):
			Dwarn("Inconsistent length of comments and translation for language: %s." % lang)
		for i in range(len(comments)):
			comm = comments[i].strip('\n')
			tran = translation[i].strip('\n') if i < len(translation) else ""
			danmakus.append(Danmaku(comm, tran, lang))
	Dprint("All comments and translation have been retrieved.")
	video = VideoFileClip(video_path)
	return danmakus, video


def export_final_video(video, configs):
	"""Export the final video with danmaku."""
	# apply_patch() # no much different
	output_configs = configs[OUTPUT]
	video.write_videofile(	output_configs[VIDEO_NAME],
							audio_codec='aac', 
							threads=output_configs[THREADS],
							codec=output_configs[CODEC],
							bitrate=output_configs[BITRATE])


def export_final_video_ffmpeg(danmaku_videos, configs):
	"""Export the final video mainly with ffmpeg."""
	timestamps = export_danmaku_videos(danmaku_videos)
	insert_danmaku_videos(timestamps, configs)


def export_danmaku_videos(danmaku_videos):
	"""Export all danmaku videos with alpha channel."""
	if os.path.exists(danmaku_videos_output):
		shutil.rmtree(danmaku_videos_output)
	os.makedirs(danmaku_videos_output)

	Dprint("Moviepy will start to export all danmaku textclips. Please wait...")

	danmaku_video_id, danmaku_video_timestamps, progress = 0, {}, 0
	for (v, t) in danmaku_videos:

		# First export image sequence, since currently write_videofile doesn't support argb.
		img_seq_path = os.path.join(danmaku_videos_output, "img_seq", str(danmaku_video_id))
		if not os.path.exists(img_seq_path):
			os.makedirs(img_seq_path)
		img_seq = os.path.join(img_seq_path, "frame%04d.png")
		v.write_images_sequence(img_seq, withmask=True)

		# Second combine the image sequence using ffmpeg (temporary measure)
		danmaku_video_name = "{:0>3d}.mov".format(danmaku_video_id)
		output = os.path.join(danmaku_videos_output, danmaku_video_name)
		command = "ffmpeg -r {fps} -i {imgs} -vcodec qtrle {output}".format(fps=v.fps, imgs=img_seq, output=output)
		subprocess.call(command, shell=True)
		danmaku_video_id += 1
		danmaku_video_timestamps[danmaku_video_name] = t

		# Wait for the development of moviepy ffmpeg tools
		# print(ffmpeg_write_video.__defaults__)
		# print(ffmpeg_write_video.__code__.co_varnames)
		# ffmpeg_write_video(danmaku_video, "test.mov", 24, codec="qtrle", withmask=True)

		progress += 1
		Dprint("Danmaku video completion progress: %d/%d" %(progress, len(danmaku_videos)))

	Dprint("All danmaku videos are exported. Ready for FFmpeg stage.")
	# Save the timestamps in case of user needs
	with open("danmaku_video_timestamps.json", 'w') as f:
		json.dump(danmaku_video_timestamps, f)
	return danmaku_video_timestamps


def insert_danmaku_videos(timestamps, configs):
	"""Insert danmaku videos over the target video using FFmpeg."""
	input_video_path = configs[INPUT][VIDEO_PATH]
	output_path = configs[OUTPUT][VIDEO_NAME]
	bitrate = configs[OUTPUT][BITRATE]
	codec = configs[OUTPUT][CODEC]
	fps = configs[DANMAKU][FPS]
	temp_path = os.path.join(danmaku_videos_output, "temp.avi")

	# Save video file
	video_path = os.path.join(danmaku_videos_output, "base.avi")
	subprocess.call("ffmpeg -i {i} -r {f} -b:v {b} -vcodec {c} {v}"\
		.format(i=input_video_path, f=fps, b=bitrate, c=codec, v=video_path), shell=True)
	Dprint("Video stream reframed and saved.")

	# Save audio file
	audio_path = os.path.join(danmaku_videos_output, "base.wav")
	subprocess.call("ffmpeg -i {v} {a}".format(v=video_path, a=audio_path), shell=True)
	Dprint("Audio stream is saved.")

	## Example of ffmpeg command used here:
	## 	ffmpeg -i a.mp4 -i b.mp4 -filter_complex '[1:v]setpts=PTS-STARTPTS+2/TB[v1];
	## 	[0:v][v1]overlay=eof_action=pass[v2]' -b:v 5M -vcodec h264_videotoolbox -map '[v2]' out.mp4

	# Generate ffmpeg command
	input_streams, input_cmd = [], ["-i " + video_path]
	for (dir_path, dir_names, file_names) in os.walk(danmaku_videos_output):
		for file_name in file_names:
			if file_name.endswith('.mov'):
				input_streams.append(file_name)
				input_cmd.append("-i " + os.path.join(danmaku_videos_output, file_name))
	input_cmd = " ".join(input_cmd) # define input streams
	filter_cond, base= [], "0"
	for i in range(1, len(input_streams) + 1):
		file_name = input_streams[i - 1]
		# Redefine stream starting time
		filter_cond.append("[{id}:v]setpts=PTS-STARTPTS+{t}/TB[{id}d]".format(id=i, t=timestamps[file_name]))
		# Perform the overlay
		output_stream = "v" + str(i)
		filter_cond.append("[{b}][{id}d]overlay=eof_action=pass[{out}]".format(b=base, id=i, out=output_stream))
		base = output_stream
	filter_cond = ";".join(filter_cond)
	command = "ffmpeg -r {fps} {input_cmd} -filter_complex '{filter_cond}' -b:v {bitrate} -vcodec {codec} -map '[{final}]' {output}"\
		.format(fps=fps, input_cmd=input_cmd, filter_cond=filter_cond, bitrate=bitrate, codec=codec, final=base, output=temp_path)
	Dprint("FFmpeg will execute the following command to add danmaku: %s" % command)

	# Remove previous output file if existed
	if os.path.exists(output_path):
		os.remove(output_path)

	# Run ffmpeg command
	subprocess.call(command, shell=True)

	# Combine the final video with audio
	Dprint("Video stream is ready and ready to package audio.")
	subprocess.call("ffmpeg -i {v} -i {a} -b:v {b} -vcodec {c} {o}"\
		.format(v=temp_path, a=audio_path, b=bitrate, c=codec, o=output_path), shell=True)
	Dprint("Congratulations! Final video exported!")

