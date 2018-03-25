'''

Copyright (c) 2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import logging
import os
import sys

class Logman:

    def __init__(self,stream=True,MESSAGELEVEL=None):
        self.level = get_logging_level(MESSAGELEVEL)
        if stream == True:
            logging.basicConfig(stream=sys.stdout,level=self.level)
        else:
            logging.basicConfig(level=self.level)
        self.logger = logging.getLogger('bone-age')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logging_level(MESSAGELEVEL=None):
    '''get_logging_level will return a logging level based on first
    a variable going into the function, then an environment variable
    MESSAGELEVEL, and then the default is DEBUG.
    :param MESSAGELEVEL: the level to get.
    '''
    if MESSAGELEVEL == None:
        MESSAGELEVEL = os.environ.get("MESSAGELEVEL","DEBUG")

    if MESSAGELEVEL in ["DEBUG","INFO"]:
        print("Environment message level found to be %s" %MESSAGELEVEL)

    if MESSAGELEVEL == "FATAL":
        return logging.FATAL

    elif MESSAGELEVEL == "CRITICAL":
        return logging.CRITICAL

    elif MESSAGELEVEL == "ERROR":
        return logging.ERROR

    elif MESSAGELEVEL == "WARNING":
        return logging.WARNING

    elif MESSAGELEVEL == "INFO":
        return logging.INFO

    elif MESSAGELEVEL in "DEBUG":
        return logging.DEBUG

    return logging.DEBUG

bot = Logman()
