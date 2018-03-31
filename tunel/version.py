__version__ = "1.0.0"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'tunel'
PACKAGE_URL = "http://www.github.com/vsoch/tunel"
KEYWORDS = 'commander, containers, viewer, hpc, cluster, computing'
DESCRIPTION = "commander and viewer to tunnel commands for HPC"
LICENSE = "LICENSE"

INSTALL_REQUIRES = (
    ('flask', {'min_version': '0.12'}),
    ('flask-restful', {'min_version': None}),
    ('flask-blueprint',{'min_version': None}),
    ('Flask-WTF', {'min_version': None}),
    ('requests', {'min_version': '2.12.4'}),
    ('flask-cors', {'min_version': None}),
    ('pygments', {'min_version': '2.1.3'}),
    ('google-api-python-client', {'min_version': None}),
    ('oauth2client', {'exact_version': '3.0'})
)
