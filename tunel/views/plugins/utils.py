'''

Copyright (C) 2017-2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import re
from tunel.server import app

def generate_plugins():
    '''return a list of active plugin names based on config settings
    '''
    plugins = []
    for key,enabled in app.config.items():
        # Variable that indicates plugin enabled or not
        if key.startswith('PLUGIN_') and key.endswith('_ENABLED'):
            plugin = (re.sub('PLUGIN_|_ENABLED', '', key) or '').lower()
            plugins.append(plugin)

    return plugins
