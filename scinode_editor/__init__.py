'''
Copyright (C) 2022 <Xing Wang>
<xingwang1991@gmail.com>

Created by <Xing Wang>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Scinode Editor",
    "author": "Xing Wang",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location":    "SciNode Editor",
    "description": """Design computational workflow using SciNode and Blender node editor.""",
    "warning": "",
    "category": "Node",
}


import bpy
# install pip dependencies
from .install import pip_dependencies
pip_dependencies.install()

from . import (
    logger,
    bpy_data,
    preferences,
    node_catagory,
    node_tree,
)

logger.set_logger(bl_info["version"])

classes_bpy_data = [
    # internal data first
    bpy_data.ScinodeDaemon,
    bpy_data.Scinode,
]

import importlib

modules = [
    'sockets',
    'nodes',
    'ops',
    'gui',
]


def enable_module(path, modules):
    for key in modules:
        module = importlib.import_module("{}{}".format(path, key))
        module.register_class()

def disable_module(path, modules):
    for key in modules:
        module = importlib.import_module("{}{}".format(path, key))
        module.unregister_class()


classes = (
node_tree.ScinodeTree,
)


def register():
    from bpy.types import Object, Scene
    from bpy.utils import register_class
    import nodeitems_utils

    for cls in classes_bpy_data:
        register_class(cls)

    Object.Scinode = bpy.props.PointerProperty(name='Scinode',
                                    type=bpy_data.Scinode)
    Scene.Scinode = bpy.props.PointerProperty(type=bpy_data.Scinode)

    preferences.register_class()

    for cls in classes:
        register_class(cls)
    enable_module("scinode_editor.", modules)
    nodeitems_utils.register_node_categories('BNODES', node_catagory.node_categories)


def unregister():
    from bpy.types import Object, Scene
    import nodeitems_utils
    from bpy.utils import unregister_class

    del Object.Scinode
    del Scene.Scinode

    disable_module("scinode_editor.", modules)
    nodeitems_utils.unregister_node_categories('BNODES')

    for cls in reversed(classes):
        unregister_class(cls)

    for cls in reversed(classes_bpy_data):
        unregister_class(cls)
    preferences.unregister_class()


if __name__ == "__main__":
    register()
