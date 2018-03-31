from tunel.server import app
import re
import os

plugins = os.path.abspath(os.path.dirname(__file__))

# A key for a plugin is in format PLUGIN_<module>_ENABLED

for key,enabled in app.config.items():

    # Variable that indicates plugin enabled or not
    if key.startswith('PLUGIN_') and key.endswith('_ENABLED'):

        plugin = (re.sub('PLUGIN_|_ENABLED', '', key) or '').lower()

        # Keep these hard coded for tighter control
        if plugin == "globus" and enabled:
            from .globus import *
