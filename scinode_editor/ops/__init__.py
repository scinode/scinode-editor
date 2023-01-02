
from . import (
    ops_nodetree,
    ops_node,
    ops_daemon,
)

classes = (
    ops_nodetree.NodeTreeLaunch,
    ops_nodetree.NodeTreeUpdateState,
    ops_nodetree.NodeTreeResetState,
    ops_nodetree.EXPORT_OT_Nodetree,
    ops_node.NodeReset,
    ops_node.NodePause,
    ops_node.NodePlay,
    ops_node.NodeCancel,
    ops_daemon.DaemonStart,
    ops_daemon.DaemonStop,
    ops_daemon.DaemonUpdate,
)


def register_class():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_class():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register_class()
