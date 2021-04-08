import json
from constants import CONFIG_GUI_PATH
from synthesization import synthesize

# Read the configs provided by GUI (stored in config_gui.json)
with open(CONFIG_GUI_PATH) as f:
    configs = json.load(f)

# Do the synthesization
synthesize(configs)
