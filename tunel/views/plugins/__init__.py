from tunel.server import app
from .utils import generate_plugins
import re
import os

plugins = os.path.abspath(os.path.dirname(__file__))

# A key for a plugin is in format PLUGIN_<module>_ENABLED
enabled = generate_plugins()

# Globus
if "globus" in enabled:
    from .globus import *
