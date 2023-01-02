"""
Logger
"""
import bpy
import sys
from tempfile import gettempdir
from pathlib import Path
import logging
import os

scinode_editor_dir = os.path.dirname(Path(__file__).parent)



# logger = logging.getLogger('scinode_editor')
logger = logging.getLogger(__name__)
root_logger = logging.getLogger("scinode_editor")

def set_logger(version):
    # formatter = ('%(levelname)-8s '
    #                             '[%(funcName)-20s]: %(message)s')
    formatter = ('%(levelname)s '
                    '[%(name)-10s %(funcName)-10s]: %(message)s')
    logging.basicConfig(stream=sys.stdout,
                        format=formatter,
                        level=logging.INFO
                        )
    # add logger file
    filepath = Path(gettempdir()) / ("beautiful_nodes.log")
    root_logger.info("Log file: " + str(filepath))
    file_handler = logging.FileHandler(filepath, mode="w")
    file_handler.setFormatter(logging.Formatter(formatter))
    root_logger.addHandler(file_handler)
    root_logger.info("Blender version: {} ".format(bpy.app.version_string))
    root_logger.info("Python version: {} ".format(sys.version))
    root_logger.info("SciNode Editor version: {} ".format(version))
    root_logger.info("SciNode Editor directory: {} ".format(scinode_editor_dir))


def update_logging_level():
    prefs = bpy.context.preferences.addons['scinode_editor'].preferences
    root_logger.setLevel(prefs.logging_level)


def print_time(key, value):
    return '{}: {}'.format(key, value)
