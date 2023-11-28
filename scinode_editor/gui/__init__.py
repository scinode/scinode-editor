import bpy

from . import (
    gui_nodetree,
    gui_node,
    gui_daemon,
    gui_config,
)

classes = (
    gui_nodetree.SCINODE_PT_NodeTreePanel,
    gui_nodetree.NodetreeProperties,
    gui_node.SCINODE_PT_NodePanel,
    gui_daemon.SCINODE_PT_Daemon,
    gui_daemon.SCINODE_UL_Daemon,
    gui_config.SCINODE_PT_config,
)

def register_class():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    scene = bpy.types.Scene
    scene.ntpanel = bpy.props.PointerProperty(type=gui_nodetree.NodetreeProperties)


def unregister_class():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    scene = bpy.types.Scene
    del scene.ntpanel

if __name__ == "__main__":
    register_class()
