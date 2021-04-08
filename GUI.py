#!/usr/bin/env python3

import sys
import json
import subprocess
import tkinter as tk
from tkinter import StringVar, IntVar, DoubleVar, LEFT, RIGHT, BOTH, Toplevel
from tkinter.ttk import *
from tkinter import font as tkFont
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter.filedialog import askdirectory, askopenfilename

from config_default import configs
from constants import *

# This import may cause unexpected crash on Mac due to IDLE x Tkinter conflict 
# (not sure, it should be fixed in latest python3.9 
#   [https://www.python.org/download/mac/tcltk/], 
# but I still encounter this issue), and the specific reason remains unknown.
# from synthesization import synthesize 


class ConfigGUI():
    def __init__(self, configs):
        # GUI window initialization
        self.root = tk.Tk()
        self.root.title("Bilingual Danmaku Synthesizer")
        self.root.configure(bg=GUI_THEME_COLOR)
        self.default_configs = configs

        # Constants of font/size/dimension
        self.helv_bold = tkFont.Font(family='Helvetica', weight='bold')
        self.lab_w = 15 # width of label
        self.btn_w = 15 # width of button component
        self.ent_w = 35 # width of entry component
        self.top_pady = (10, 0)
        self.btm_pady = (0, 10)
        self.btn_padx = 15 # padx for the action buttons

        # Build variables in input configs
        self.video_path = StringVar(self.root, name=VIDEO_PATH)
        self.audio_path = StringVar(self.root, name=AUDIO_PATH)
        self.file_path = StringVar(self.root, name=FILE_PATH)

        # Build variables in danmaku configs
        self.CN_font_path = StringVar(self.root, name=FONTS + "_cn")
        self.JP_font_path = StringVar(self.root, name=FONTS + "_jp")
        self.EN_font_path = StringVar(self.root, name=FONTS + "_eng")
        self.fontsize = DoubleVar(self.root, name=FONTSIZE)
        self.comment_color = StringVar(self.root, name=COMMENT_COLOR)
        self.translation_color = StringVar(self.root, name=TRANSLATION_COLOR)
        self.duration = DoubleVar(self.root, name=DURATION)
        self.fps = DoubleVar(self.root, name=FPS)
        self.bkgd_r = DoubleVar(self.root, name="bkgd_r")
        self.bkgd_g = DoubleVar(self.root, name="bkgd_g")
        self.bkgd_b = DoubleVar(self.root, name="bkgd_b")
        self.background_opacity = DoubleVar(self.root, name=BACKGROUND_OPACITY)
        self.coverage = DoubleVar(self.root, name=COVERAGE)
        self.time_range_beg = IntVar(self.root, name=TIME_RANGE + "_beg")
        self.time_range_end = IntVar(self.root, name=TIME_RANGE + "_end")

        # Build variables in output configs
        self.codec = StringVar(self.root, name=CODEC)
        self.bitrate = StringVar(self.root, name=BITRATE)
        self.threads = IntVar(self.root, name=THREADS)
        self.video_name = StringVar(self.root, name=VIDEO_NAME)

        # Initialize variables
        self.reset_vars()

        # Notebook configs
        self.add_config_notebook()

        # Action buttons
        self.add_action_buttons()


    def add_config_notebook(self):
        """Add the notebook display different configs in various tabs."""
        # Build notebook for configs
        self.notebook = Notebook(self.root)

        # Build GUI for different config tabs
        self.input_configs = Frame(self.notebook)
        self.build_input_config_ui()
        self.danmaku_configs = Frame(self.notebook)
        self.build_danmaku_config_ui()
        self.output_configs = Frame(self.notebook)
        self.build_output_config_ui()

        # Build tabs
        self.notebook.add(self.input_configs, text="Input Configs")
        self.notebook.add(self.danmaku_configs, text="Danmaku Configs")
        self.notebook.add(self.output_configs, text="Output Configs")
        self.notebook.pack()
    

    def add_action_buttons(self):
        """Add several action buttons outside the notebook."""
        # Help and Reset button
        Button(self.root, text="Help", command=self.start_synthesization)\
            .pack(side=LEFT, fill=BOTH, padx=self.btn_padx, pady=self.btm_pady)
        Button(self.root, text="Reset", command=self.reset_vars)\
            .pack(side=LEFT, fill=BOTH, padx=self.btn_padx, pady=self.btm_pady)

        # Start button
        Button(self.root, text="Start Synthesization", command=self.start_synthesization)\
            .pack(side=RIGHT, fill=BOTH, padx=self.btn_padx, pady=self.btm_pady)


    def reset_vars(self):
        """Function for resetting all variables under root."""
        configs = self.default_configs

        # Default input configs
        self.root.setvar(name=VIDEO_PATH, value=configs[INPUT][VIDEO_PATH])
        self.root.setvar(name=AUDIO_PATH, value=configs[INPUT][AUDIO_PATH])
        self.root.setvar(name=FILE_PATH, value=configs[INPUT][FILE_PATH])

        # Default danmaku configs
        self.root.setvar(name=FONTS + "_cn", value=configs[DANMAKU][FONTS]["cn"])
        self.root.setvar(name=FONTS + "_jp", value=configs[DANMAKU][FONTS]["jp"])
        self.root.setvar(name=FONTS + "_eng", value=configs[DANMAKU][FONTS]["eng"])
        self.root.setvar(name=FONTSIZE, value=configs[DANMAKU][FONTSIZE])
        self.root.setvar(name=COMMENT_COLOR, value=configs[DANMAKU][COMMENT_COLOR])
        self.root.setvar(name=TRANSLATION_COLOR, value=configs[DANMAKU][TRANSLATION_COLOR])
        self.root.setvar(name=DURATION, value=configs[DANMAKU][DURATION])
        self.root.setvar(name=FPS, value=configs[DANMAKU][FPS])
        self.root.setvar(name="bkgd_r", value=configs[DANMAKU][BACKGROUND_RGB][0])
        self.root.setvar(name="bkgd_g", value=configs[DANMAKU][BACKGROUND_RGB][1])
        self.root.setvar(name="bkgd_b", value=configs[DANMAKU][BACKGROUND_RGB][2])
        self.root.setvar(name=BACKGROUND_OPACITY, value=configs[DANMAKU][BACKGROUND_OPACITY])
        self.root.setvar(name=COVERAGE, value=configs[DANMAKU][COVERAGE])
        self.root.setvar(name=TIME_RANGE + "_beg", value=None)
        self.root.setvar(name=TIME_RANGE + "_end", value=None)

        # Default output configs
        self.root.setvar(name=CODEC, value=configs[OUTPUT][CODEC])
        self.root.setvar(name=BITRATE, value=configs[OUTPUT][BITRATE])
        self.root.setvar(name=THREADS, value=configs[OUTPUT][THREADS])
        self.root.setvar(name=VIDEO_NAME, value=configs[OUTPUT][VIDEO_NAME])


    def build_input_config_ui(self):
        """Build the UI frame for the input configs."""
        # Input property::video_path
        Label(self.input_configs, text="Video Path: ", width=self.lab_w)\
            .grid(row=0, column=0, pady=self.top_pady)
        Entry(self.input_configs, textvariable=self.video_path, width=self.ent_w)\
            .grid(row=0, column=1, pady=self.top_pady)
        Button(self.input_configs, text="Choose video", width=self.btn_w, command=self.getSelFilenameFunc(self.video_path))\
            .grid(row=0, column=2, padx=self.btn_padx, pady=self.top_pady)

        # Input property::audio_path
        Label(self.input_configs, text="Audio Path: ", width=self.lab_w)\
            .grid(row=1, column=0)
        Entry(self.input_configs, textvariable=self.audio_path, width=self.ent_w)\
            .grid(row=1, column=1)
        Button(self.input_configs, text="Choose audio", width=self.btn_w, command=self.getSelFilenameFunc(self.audio_path))\
            .grid(row=1, column=2)

        # Input property::file_path
        Label(self.input_configs, text="TXT File Path: ", width=self.lab_w)\
            .grid(row=2, column=0)
        Entry(self.input_configs, textvariable=self.file_path, width=self.ent_w)\
            .grid(row=2, column=1)
        Button(self.input_configs, text="Choose file directory", width=self.btn_w, command=self.getSelPathFunc(self.file_path))\
            .grid(row=2, column=2)


    def build_danmaku_config_ui(self):
        """Build the UI frame for the danmaku configs."""
        # Danmaku property::fonts::cn
        Label(self.danmaku_configs, text="Chinese Font: ", width=self.lab_w)\
            .grid(row=0, column=0, pady=self.top_pady)
        Entry(self.danmaku_configs, textvariable=self.CN_font_path, width=self.ent_w)\
            .grid(row=0, column=1, pady=self.top_pady)
        Button(self.danmaku_configs, text="Choose Font File", width=self.btn_w, command=self.getSelFilenameFunc(self.CN_font_path))\
            .grid(row=0, column=2, padx=self.btn_padx, pady=self.top_pady)

        # Danmaku property::fonts::jp
        Label(self.danmaku_configs, text="Japanese Font: ", width=self.lab_w)\
            .grid(row=1, column=0)
        Entry(self.danmaku_configs, textvariable=self.JP_font_path, width=self.ent_w)\
            .grid(row=1, column=1)
        Button(self.danmaku_configs, text="Choose Font File", width=self.btn_w, command=self.getSelFilenameFunc(self.JP_font_path))\
            .grid(row=1, column=2)

        # Danmaku property::fonts::eng
        Label(self.danmaku_configs, text="English Font: ", width=self.lab_w)\
            .grid(row=2, column=0)
        Entry(self.danmaku_configs, textvariable=self.EN_font_path, width=self.ent_w)\
            .grid(row=2, column=1)
        Button(self.danmaku_configs, text="Choose Font File", width=self.btn_w, command=self.getSelFilenameFunc(self.EN_font_path))\
            .grid(row=2, column=2)

        # Danmaku property::fontsize
        Label(self.danmaku_configs, text="Fontsize: ", width=self.lab_w).grid(row=3, column=0)
        Entry(self.danmaku_configs, textvariable=self.fontsize, width=self.ent_w).grid(row=3, column=1)

        # Danmaku property::comment_color
        Label(self.danmaku_configs, text="Comment color: ", width=self.lab_w).grid(row=4, column=0)
        Entry(self.danmaku_configs, textvariable=self.comment_color, width=self.ent_w).grid(row=4, column=1)

        # Danmaku property::translation_color
        Label(self.danmaku_configs, text="Translation color: ", width=self.lab_w).grid(row=5, column=0)
        Entry(self.danmaku_configs, textvariable=self.translation_color, width=self.ent_w).grid(row=5, column=1)

        # Danmaku property::duration
        Label(self.danmaku_configs, text="Duration: ", width=self.lab_w).grid(row=6, column=0)
        Entry(self.danmaku_configs, textvariable=self.duration, width=self.ent_w).grid(row=6, column=1)

        # Danmaku property::fps
        Label(self.danmaku_configs, text="FPS: ", width=self.lab_w).grid(row=7, column=0)
        Entry(self.danmaku_configs, textvariable=self.fps, width=self.ent_w).grid(row=7, column=1)

        # Danmaku property::background_rgb
        Label(self.danmaku_configs, text="Background RGB: ", width=self.lab_w).grid(row=8, column=0)
        rgb_entry = Frame(self.danmaku_configs)
        Label(rgb_entry, text="R").pack(side=LEFT)
        Entry(rgb_entry, textvariable=self.bkgd_r, width=5).pack(side=LEFT)
        Label(rgb_entry, text="G").pack(side=LEFT)
        Entry(rgb_entry, textvariable=self.bkgd_g, width=5).pack(side=LEFT)
        Label(rgb_entry, text="B").pack(side=LEFT)
        Entry(rgb_entry, textvariable=self.bkgd_b, width=5).pack(side=LEFT)
        rgb_entry.grid(row=8, column=1)

        # Danmaku property::background_opacity
        Label(self.danmaku_configs, text="Background Opacity: ", width=self.lab_w).grid(row=9, column=0)
        Entry(self.danmaku_configs, textvariable=self.background_opacity, width=self.ent_w).grid(row=9, column=1)

        # Danmaku property::coverage
        Label(self.danmaku_configs, text="Coverage: ", width=self.lab_w).grid(row=10, column=0)
        Entry(self.danmaku_configs, textvariable=self.coverage, width=self.ent_w).grid(row=10, column=1)

        # Danmaku property::background_opacity
        Label(self.danmaku_configs, text="Time Range: ", width=self.lab_w).grid(row=11, column=0)
        range_entry = Frame(self.danmaku_configs)
        Label(range_entry, text="from").pack(side=LEFT)
        Entry(range_entry, textvariable=self.time_range_beg, width=5).pack(side=LEFT)
        Label(range_entry, text="to").pack(side=LEFT)
        Entry(range_entry, textvariable=self.time_range_end, width=5).pack(side=LEFT)
        range_entry.grid(row=11, column=1)


    def build_output_config_ui(self):
        """Build the UI frame for the output configs."""
        # Output property::codec
        Label(self.output_configs, text="Codec: ", width=self.lab_w).grid(row=0, column=0, pady=self.top_pady)
        Entry(self.output_configs, textvariable=self.codec, width=self.ent_w).grid(row=0, column=1, pady=self.top_pady)


    def start_synthesization(self):
        """Function combined with the main action button."""
        # showinfo(title="Start Synthesization", message="Your request is being processed. Please wait for several minutes.")
        try:
            self.openConfirmWindow(self.getFinalConfigs())
        except Exception as e:
            showerror(message=str(e))

    def openConfirmWindow(self, configs):
        """Open a new window for user to confirm."""
        confirmWindow = tk.Toplevel(self.root)
        confirmWindow.title("Request Confirmation")

        def getSynthesizeFunc(configs):
            """Return the synthesize function with user's configs."""
            def synthesize_func():
                # close the confirmation window
                confirmWindow.destroy()

                # dump the final configs into a json file
                with open(CONFIG_GUI_PATH, 'w') as fp:
                    json.dump(configs, fp, indent=4)

                # use subprocess to work around instead of directly using synthesize
                subprocess.Popen("python3 app_gui.py", stdout=sys.stdout, shell=True) # unsynchronized cmd
                # subprocess.call("python3 app_gui.py", shell=True) # synchronized cmd
            return synthesize_func
    
        # A Label widget to show in toplevel
        tk.Label(confirmWindow, text="Are you good to go with the following configs?", font=self.helv_bold).pack()
        Label(confirmWindow, text=json.dumps(configs, indent=4)).pack(padx=10, pady=10)
        tk.Button(confirmWindow, text="I Confirmed", font=self.helv_bold, command=getSynthesizeFunc(configs)).pack(pady=self.btm_pady)


    def getSelPathFunc(self, path):
        """Return path selection function."""
        def selectPath():
            path_ = askdirectory()
            path.set(path_)
        return selectPath


    def getSelFilenameFunc(self, filename):
        """Return file selection function."""
        def selectFilename():
            filename_ = askopenfilename()
            filename.set(filename_)
        return selectFilename


    def getFinalConfigs(self):
        """Return the final configs after user submission."""
        final_configs = dict(self.default_configs)

        # Update variables in input configs
        final_configs[INPUT][VIDEO_PATH] = self.root.getvar(name=VIDEO_PATH)
        final_configs[INPUT][AUDIO_PATH] = self.root.getvar(name=AUDIO_PATH)
        final_configs[INPUT][FILE_PATH] = self.root.getvar(name=FILE_PATH)

        # Update variables in danmaku configs
        final_configs[DANMAKU][FONTS]["cn"] = self.root.getvar(name=FONTS + "_cn")
        final_configs[DANMAKU][FONTS]["jp"] = self.root.getvar(name=FONTS + "_jp")
        final_configs[DANMAKU][FONTS]["eng"] = self.root.getvar(name=FONTS + "_eng")
        final_configs[DANMAKU][FONTSIZE] = self.root.getvar(name=FONTSIZE)
        final_configs[DANMAKU][COMMENT_COLOR] = self.root.getvar(name=COMMENT_COLOR)
        final_configs[DANMAKU][TRANSLATION_COLOR] = self.root.getvar(name=TRANSLATION_COLOR)
        final_configs[DANMAKU][DURATION] = self.root.getvar(name=DURATION)
        final_configs[DANMAKU][FPS] = self.root.getvar(name=FPS)
        final_configs[DANMAKU][BACKGROUND_RGB] = [\
            self.root.getvar(name="bkgd_r"), \
            self.root.getvar(name="bkgd_g"), \
            self.root.getvar(name="bkgd_b") \
        ]
        final_configs[DANMAKU][BACKGROUND_OPACITY] = self.root.getvar(name=BACKGROUND_OPACITY)
        final_configs[DANMAKU][COVERAGE] = self.root.getvar(name=COVERAGE)
        final_configs[DANMAKU][TIME_RANGE] = [\
            self.root.getvar(name=TIME_RANGE + "_beg"), \
            self.root.getvar(name=TIME_RANGE + "_end") \
        ]

        # Update variables in output configs
        final_configs[OUTPUT][CODEC] = self.root.getvar(name=CODEC)
        final_configs[OUTPUT][BITRATE] = self.root.getvar(name=BITRATE)
        final_configs[OUTPUT][THREADS] = self.root.getvar(name=THREADS)
        final_configs[OUTPUT][VIDEO_NAME] = self.root.getvar(name=VIDEO_NAME)

        return final_configs


configGUI = ConfigGUI(configs)
configGUI.root.mainloop()
