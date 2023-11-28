

from . import (
    batoms_node,
)

classes = (
    batoms_node.Batoms,
    batoms_node.ViewBatoms,
    batoms_node.BatomsScaleCell,
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
