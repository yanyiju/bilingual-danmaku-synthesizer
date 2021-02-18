中文 | [English](README_EN.md)

# 私人订制双语弹幕合成工具
私人订制双语弹幕合成工具（Bilingual Danmaku Synthesizer Tool，缩写BDST）适用于想要模拟弹幕效果的评论视频制作，基于用户输入外语评论及对应中文翻译自动合成双语弹幕并随机叠加于原视频之上。

## 效果演示
用户可以通过改动配制文件中的参数来定制弹幕风格，包括弹幕存活时间、弹幕文字颜色、弹幕字体、弹幕字体大小、弹幕显示区域、弹幕背景颜色等等。演示效果的视频文件及动图在[这里](./Demo)。

![效果动画](./Demo/demo.gif)
![效果动画 弹幕配备背景颜色](./Demo/demo_bkgd.gif)

因为这个项目是受[洛飕飕@bilibili](https://space.bilibili.com/2505015)的评论视频启发，这里暂时借用其作品来demo展示。(原作者本人已许可)

![真实效果动画](./Demo/sousou_work.gif)
![真实效果动画 弹幕配备背景颜色](./Demo/sousou_work_bkgd.gif)

## 安装依赖
脚本语言使用python3，并基于标准库和MoviePy开发。本工具的依赖树：
```
BDST
└── MoviePy (required)
    ├── FFmpeg (required)
    ├── ImageMagick (required)
    └── Pygame (optional)
```

MoviePy库会使用FFmpeg这一最常用的视频处理开源软件。在执行脚本前，请先依据官方文档安装[MoviePy](https://zulko.github.io/moviepy/install.html)。初次使用MoviePy时，FFmpeg会自动通过镜像安装，所以用户**无需自行安装**[FFmpeg](https://ffmpeg.org/download.html)。通常使用pip平台安装MoviePy即可：
```
pip install moviepy
```

此外，因为本工具涉及文字层的使用，[ImageMagick](https://www.imagemagick.org/script/download.php)其作为MoviePy目前在文字处理方面依赖也必须安装（[详情](https://zulko.github.io/moviepy/install.html#other-optional-but-useful-dependencies)）。对于Mac用户，通常使用Homebrew安装预编译版ImageMagick：
```
brew install imagemagick
```

对于本工具，[Pygame](https://www.pygame.org/wiki/GettingStarted)可以选择暂不安装。

## 使用流程
### 准备工作
#### 视频准备
用户请先行准备好目标视频。视频格式接受.ogv，.mp4，.mpeg，.avi，.mov等任何FFmpeg支持的格式。

#### 评论和翻译文件
目前脚本只接受TXT格式的文件。请确保评论文件和翻译文件的语句**根据行数一一对应**，例如对于第100行的评论语句，其对应翻译应该在翻译文件的第100行。[这里](InputFiles_example/)提供一个例子，后续可能会优化这一步骤。

评论文件的命名格式为```comments_[评论语言].txt```，例如英语评论文件请命名为```comments_eng.txt```；日语评论文件请命名为```comments_jp.txt```。对应的中文翻译文件的命名格式为```translation_[评论语言].txt```，例如英语评论的翻译文件请命名为```translation_eng.txt```；日语评论的翻译文件请命名为```translation_jp.txt```。

因目前评论语言仅支持英语与日语，所以用户至多有四个文件。请将所有文件置于```InputFiles/```文件夹或某一特定文件夹内。

### 设定配置文件
用户可以在[```config_override.py```](config_override.py)中添加参数自定义值来覆盖存放于[```config_default.py```](config_default.py)中的默认参数配置。配置文件中包含三大部分，分别为输入、弹幕和输出。

#### 关于输入
该部分参数位于关键字***input***下，主要关于目标视频路径以及TXT输入文件路径。
| 参数 | 用途 | 备注 |
| :----- | :----: | :----: |
| video_path | 目标视频的文件地址[**必需**] | 如果视频在当前文件目录下，<br>直接输入视频文件名即可，<br>例如```'video_name.mp4'```，<br>另注意路径表达在不同操作系统中的不同。|
| audio_path | 用于替换的音频文件地址 | 默认为```None```，<br>即沿用原视频的音轨。<br>仅限使用MoviePy导出时有效。|
| file_path | 评论与翻译的TXT文件地址 | 默认在```InputFiles/```下，<br>如果用户直接修改该文件夹中的TXT文件，<br>则无需添加或修改此参数。|
| video_duration | 目标视频的选取范围 | 默认为```None```，<br>即整条视频会被使用。<br>例如要选取目标视频中第10秒到第100秒的部分，<br>则可以修改为[10, 100]。<br>仅限使用MoviePy导出时有效。|

#### 弹幕风格
该部分参数位于关键字***danmaku***下，主要关于弹幕的外观设计。
| 参数 | 用途 | 备注 |
| :----- | :----: | :----: |
| fonts | 各语言的字体文件路径 | 预设字体存放于```Fonts/```路径下，<br>用户可以视需求添加字体然后修改此参数。<br>若是已经安装在操作系统内的字体，<br>则可以直接填写字体名称取代路径。<br>使用moviepy内```TextClip.list('font')```<br>可以罗列操作系统内字体。|
| fontsize | 评论及翻译字体大小 | 默认大小为30像素。|
| comment_color | 评论字体颜色 | 默认颜色为白色，值为```'white'```。使用MoviePy内```TextClip.list('color')```<br>可以罗列所有颜色选项。|
| translation_color | 翻译字体颜色 | 默认颜色为白色，值为```'white'```。使用MoviePy内```TextClip.list('color')```<br>可以罗列所有颜色选项。|
| duration | 弹幕存活时间 | 默认存活时间为10秒。|
| fps | 弹幕运动帧数 | 默认使用60帧。<br>最终视频帧数取决于合成中帧率最高的部分。<br>一般正常视频不超过60帧。 |
| background_rgb | 弹幕背景颜色 | 默认弹幕背景为黑色。<br>支持RGB格式，例如[255, 0, 0]是红色。|
| background_opacity | 弹幕背景透明度 | 默认值为0，即弹幕背景不会开启。<br>可替换为任一位于[0, 1]的数。<br>仅限使用MoviePy导出时有效。|
| coverage | 弹幕显示区域 | 默认值为1，可替换为任一位于(0, 1]的数。|
| time_range_to_appear | 弹幕在视频中可以出现的时间段 | 默认为```None```，<br>即弹幕可以在任意时间点出现。<br>例如弹幕只能在前100秒出现，<br>则可以修改为[0, 100]。|

#### 关于输出
该部分参数位于关键字***output***下，主要关于视频的导出选项。
| 参数 | 用途 | 备注 |
| :----- | :----: | :----: |
| codec | 视频编码方式 | 默认```'libx264'```，其他包括```'mpeg4'```、```'rawvideo'```等。<br>详情请参照MoviePy官方文档关于[视频导出](https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#moviepy.video.VideoClip.ImageClip.write_videofile)的部分。|
| bitrate | 视频比特率 | 默认比特率为10000k。|
| threads | 导出时使用线程数 | 默认线程数为8。<br>此参数受限于用户电脑CPU配置能提供的线程数。<br>线程数越高，导出渲染速度越快。<br>MoviePy源代码仅支持使用CPU，若想使用GPU加速，请参照[备注](#关于使用GPU加速moviepy导出视频)以及FFmpeg的[硬件加速教程](https://trac.ffmpeg.org/wiki/HWAccelIntro)。|
| video_name | 导出视频文件名字 | 默认文件名为```'video_danmaku.mp4'```，<br>导出位置位于本工具文件夹内。<br>用户如修改编码参数，请相应在此参数中修改文件扩展名。|

### 导出包含弹幕的视频
在上述步骤一切准备就绪后，用户便可以在终端中执行```app.py```脚本文件以导出最终视频。
```
python3 app.py
```

## 备注

### 关于使用GPU加速MoviePy导出视频（目前阶段不建议）
MoviePy的导出效率完全取决于FFmpeg的导出效率，而不巧的是MoviePy剪切多个VideoClip时非常昂贵。但即便如此，根据测试经验，封装三分钟左右的视频和200条弹幕的总耗时也不会超过20分钟。未来待MoviePy开发完善，本工具可能会提供新的导出方法以及硬件加速方法。

如果因为您弹幕过多或其他原因导致长达数小时的渲染时间，目前则只能建议您通过降低分辨率和帧率来降低导出时间。如果您的硬件支持FFmpeg（[详情](https://trac.ffmpeg.org/wiki/HWAccelIntro)），并鉴于MoviePy仍在开发中，本工具暂时提供一种使用FFmpeg的迂回方法。

请修改位于```app.py```最后一部分的导出代码成如下：
```
# Method 1: Write out the final video with moviepy (recommended)
# video = danmakuSystem.get_video_with_danmaku(danmaku)
# export_final_video(video, configs)

# Method 2: Write out the final video with ffmpeg 
danmaku_videos = danmakuSystem.get_danmaku_videos_with_mask(danmaku)
export_final_video_ffmpeg(danmaku_videos, configs)
```
即注释掉第一个方法并取消注释第二个方法。第二个方法可以实现使用FFmpeg的硬件加速目的，但这并不能保证导出时间的缩短，原因是```danmaku_videos```是一系列包含透明通道和弹幕运动的文字剪辑，这一部分目前还是只能由moviepy导出，速度较慢。```export_final_video_ffmpeg```会先将之前的文字剪辑导出成mov文件，然后和目标视频打包，这一过程则可以使用硬件加速。想要单独导出每个弹幕运动视频的用户也可以尝试这一办法，但不推荐。

**注意！** 
如果您选择使用如上办法，请选择适当的视频编码格式，FFmpeg提供的硬件加速编码在[这里](https://trac.ffmpeg.org/wiki/HWAccelIntro)，例如：对于Mac用户，您可以选择```h264_videotoolbox```；对于NVIDIA硬件用户，您可以选择```h264_nvenc```。**如果您没有在配置文件中修改视频编码，则硬件加速不会执行。**

更多参考链接：
* [Github: Current method to export video with mask #1502](https://github.com/Zulko/moviepy/issues/1502)
* [Github: How can I speed up moviepy by gpu？ #923](https://github.com/Zulko/moviepy/issues/923)
* [Github: ffmpeg 4.0 NVIDIA NVDEC-accelerated Support ? #790](https://github.com/Zulko/moviepy/issues/790)
* [Github: Concatenating VideoFileClip is too slow #961](https://github.com/Zulko/moviepy/issues/961)
* [Moviepy: FFMPEG tools](https://zulko.github.io/moviepy/ref/ffmpeg.html)
* [Stackoverflow: FFMPEG with moviepy](https://stackoverflow.com/questions/63837260/ffmpeg-with-moviepy)
* [Stackoverflow: Concat videos too slow using Python MoviePY](https://stackoverflow.com/questions/56413813/concat-videos-too-slow-using-python-moviepy)



