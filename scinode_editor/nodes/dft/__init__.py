

from . import (
    optmizer_node,
    kpoint_node,
    vibration_node,
    neb_node,
    oer_node,
)


classes = (
    kpoint_node.DFTKpoints,
    optmizer_node.DFTOptmizer,
    vibration_node.DFTVibration,
    neb_node.DFTNEB,
    oer_node.DFTOER,
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
