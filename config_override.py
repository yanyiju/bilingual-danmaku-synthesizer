# config_override.py

configs = {
    'input': {
        # Replace with your video path in the following.
        'video_path': 'sousou.mp4',
        'file_path': 'InputFiles_example/'
    },
    'danmaku': {
		# Add your customized danmaku style changes here.
		# You can change the following features,
		# 	fonts: fonts of English/Japanese/Chinese (英语/日语/中文字体)
		# 	fontsize: size of the danmaku font (弹幕字体大小)
		# 	comment_color: color of the comments (弹幕评论部分颜色)
		# 	translation_color: color of the translation (弹幕中文翻译部分颜色)
		# 	duration: lifetime of the danmaku (弹幕存活时间)
		# 	use60fps: whether export video of 60fps (是否使用60帧) [recommended (建议开启)]
		# 	background_rgb: RGB color of danmaku' background (弹幕背景颜色)
		# 	background_opacity: opacity of danmaku' background (弹幕背景透明度)[注：用ffmpeg导出会失效]
        #   coverage: portion of emerging area of danmaku over the video (弹幕显示区域)

		# You can refer the default settings in config_default.py file.
    },
    'output': {
        # Add your customized video output settings here.
        # You can change the following features,
        # 	codec: video encoding method (视频导出编码)[FFmpeg硬件加速: h264_videotoolbox, h264_nvenc]
        # 	bitrate: video bitrate (视频比特率)
        #   threads: cpu threads used for exporting video (视频导出使用CPU线程数，建议尽量高)
        #   video_name: output video name, 'video_danmaku.mp4' defaultly (输出文件名)

        # You can refer the default settings in config_default.py file.
    }
}