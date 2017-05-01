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
import uuid
import os


# SERVER CONFIGURATION ##############################################
class SingularityServer(Flask):

    def __init__(self, *args, **kwargs):
        super(SingularityServer, self).__init__(*args, **kwargs)

        self.containers = get_containers()
        self.bases = get_bases()
        self.tmpdir = tempfile.mkdtemp()
        self.image = None # Holds image to run
        self.cli = Singularity()


app = SingularityServer(__name__)

from api import *
from auth import *
from views import *
from containers import *

if __name__ == '__main__':
    if not os.path.exists('client_id.json'):
        print('Client secrets file (client_id.json) not found in the app path.')
        exit()
    app.debug = True
    app.secret_key = str(uuid.uuid4())
    app.run(host='0.0.0.0')
