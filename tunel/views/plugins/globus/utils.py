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

import grp
import os
import pwd
import tempfile


def do_transfer(client,
                source_endpoint, 
                dest_endpoint, 
                images):
    '''transfer a source_image from source_endpoint to dest_endpoint named
       as dest_image using client

       Parameters
       ==========
       client: the globus sdk client with transfer client 
       source_endpoint: transfer FROM this endpoint
       dest_endpoint: transfer TO this endpoint
       images: a list of (source, dest) to send in the single transaction

    '''

    for image_set in images:
        source_image = image_set[0]
        dest_image = image_set[1]
        tdata = globus_sdk.TransferData(client.transfer_client, 
                                        source_endpoint,
                                        dest_endpoint,
                                        label="SRegistry Transfer with Tunel",
                                        sync_level="checksum")

        tdata.add_item(source_image, dest_image)

    # Send back a single link to show
    return client.transfer_client.submit_transfer(tdata)


def generate_transfer_name():
    '''generate a temporary name in tunel-user home to send or receive a file
    '''
    tmp = next(tempfile._get_candidate_names())
    return "/home/tunel-user/container.%s.simg" %tmp


def generate_transfer_file(container):
    '''This will generate a temporary file to use for the transfer, so that
       the same container file isn't being read in two places, not that this
       would be super risky :) We also move the file into the tunel-user's
       home, which is the only place we want to expose to the actual endpoint.

       Parameters
       ==========
       container: the full path to the container under roots home.

    '''

    tmp = generate_transfer_name()
            
    # The owner has to be the tunel-user

    shutil.copyfile(container, tmp)
    uid = pwd.getpwnam("tunel-user").pw_uid
    gid = grp.getgrnam("tunel-user").gr_gid
    os.chown(tmp, uid, gid)

    os.environ.putenv('USER', 'tunel-user')
    os.environ['USER'] = 'tunel-user'

    st = os.stat(tmp)
    os.chmod(tmp, st.st_mode | stat.S_IEXEC)
    return tmp
