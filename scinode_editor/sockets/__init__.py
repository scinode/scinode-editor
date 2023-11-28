
from . import (
    general_socket,
    special_socket,
    ase_socket,
)

classes = (
    general_socket.ScinodeSocketGeneral,
    general_socket.ScinodeSocketFloat,
    general_socket.ScinodeSocketInt,
    general_socket.ScinodeSocketString,
    general_socket.ScinodeSocketBool,
    general_socket.ScinodeSocketFloatVector3D,
    general_socket.ScinodeSocketIntVector3D,
    general_socket.ScinodeSocketFloatMatrix3D,
    special_socket.ScinodeSocketJoin,
    ase_socket.ScinodeSocketAtoms,
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
