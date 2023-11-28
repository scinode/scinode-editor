

from . import (
    scatter_node,
    switch_node,
    update_node,
)

classes = (
    scatter_node.Scatter,
    update_node.Update,
    switch_node.Switch,
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
