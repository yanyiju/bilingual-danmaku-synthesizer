# config_default.py

configs = {
    'input': {
        'video_path': None,
        'audio_path': None,
        'file_path': 'InputFiles/',
        'video_duration': None
    },
    'danmaku': {
        'fonts': {
            'eng': 'TimesNewRoman',
            'jp': 'Fonts/Japanese/Hiragino_Mincho_Pro_W6.otf',
            'cn': 'Fonts/Chinese/SourceHanSerif/SourceHanSerif-Heavy.ttc'
        },
        'fontsize': 30,
        'comment_color': 'white',
        'translation_color': 'white',
        'duration': 10,
        'fps': 60,
        'background_rgb': [0, 0, 0],
        'background_opacity': 0.5,
        'coverage': 1,
        'time_range_to_appear': None
    },
    'output': {
        'codec': 'libx264',
        'bitrate': '10000k',
        'threads': 8, 
        'video_name': 'video_danmaku.mp4'
    }
}
