

## write by qingluan 
# this is a config file
# include db and debug , static path 
import os
from os import path
# here to load all controllers
from Qtornado.log import LogControl
from Qtornado.db import *
from controller import *

# load ui modules
import ui
import sys
from qlib.data.stream import lfsr
from functools import partial
from qlib.data.stream import passpack, passunpack

# db engine 
# db_engine = pymongo.Connection()['local']
db_connect_cmd = r'database="./db.sql"'
db_engine = SqlEngine(database="./db.sql")


# static path 
rdir_path = os.path.dirname(__file__)
static_path = rdir_path + r"\static" if sys.platform.startswith("win") else "./static"
files_path = rdir_path + r".\static\files" if sys.platform.startswith("win") else "./static/files"
# set log level
LogControl.LOG_LEVEL |= LogControl.OK
LogControl.LOG_LEVEL |= LogControl.INFO

password = b'fuck this'
de_and_en = partial(lfsr, password)


Settings = {
        'db':db_engine,
        'L': LogControl,
        'debug':True,
        'pack':partial(passpack, password),
        'unpack':partial(passunpack, password),
        "ui_modules": ui,
        'de_and_en':de_and_en,
        'autoreload':True,
        'cookie_secret':'This string can be any thing you want',
        'static_path' : static_path,
    }


## follow is router
try:
    os.mkdir(files_path)
except FileExistsError:
    pass
#
appication = tornado.web.Application([
                (r'/',IndexHandler),
                # add some new route to router
		(r'/relay',RelayHandler),
#<route></route>
                # (r'/main',MainHandler),
         ],**Settings)


# setting port 
port = 9000

