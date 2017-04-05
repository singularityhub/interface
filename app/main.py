from flask import (
    Flask, 
    url_for
)

from singularity.cli import Singularity
from utils import (
    get_containers,
    get_bases
)
import tempfile
import os


# SERVER CONFIGURATION ##############################################
class SingularityServer(Flask):

    def __init__(self, *args, **kwargs):
        super(SingularityServer, self).__init__(*args, **kwargs)

        # Set up temporary directory on start of application
        self.containers = get_containers()
        self.bases = get_bases()
        self.tmpdir = tempfile.mkdtemp()
        self.image = None # Holds image to run
        self.cli = Singularity()


app = SingularityServer(__name__)

from api import *
from views import *

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
