

from . import (
    test_node,
)


classes = (
    test_node.TestFloat,
    test_node.TestAdd,
    test_node.TestGreater,
    test_node.TestLess,
    test_node.TestRange,
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
