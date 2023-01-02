

from . import (
    basic_type,
)

classes = (
    basic_type.Float,
    basic_type.Integer,
    basic_type.String,
    basic_type.Bool
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
