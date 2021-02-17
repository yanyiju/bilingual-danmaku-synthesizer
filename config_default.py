# config_default.py

configs = {
    'input': {
        'video_path': None,
        'file_path': 'InputFiles/'
    },
    'danmaku': {
        'fonts': {
            'eng': 'TimesNewRoman',
            'jp': 'Fonts/日本語/ヒラギノ明朝 Pro W6.otf',
            'cn': 'Fonts/中文/思源宋体/SourceHanSerif-Heavy.ttc'
        },
        'fontsize': 30,
        'comment_color': 'white',
        'translation_color': 'white',
        'duration': 10,
        'fps': 60,
        'background_rgb': [0, 0, 0],
        'background_opacity': 0.5,
        'coverage': 1
    },
    'output': {
        'codec': 'libx264',
        'bitrate': '10000k',
        'threads': 8, 
        'video_name': 'video_danmaku.mp4'
    }
}
