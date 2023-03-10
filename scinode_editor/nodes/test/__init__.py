

from . import (
    test_node,
    test_node_group,
)


classes = (
    test_node.TestFloat,
    test_node.TestAdd,
    test_node.TestSqrt,
    test_node.TestGreater,
    test_node.TestLess,
    test_node.TestRange,
    test_node_group.TestSqrtAdd,
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
