
# from . import ()
from . import base_node

classes = [base_node.ScinodeTreeBaseNode,
]

from scinode_editor import enable_module, disable_module

modules = [
    "python_builtin",
    "control",
    "batoms",
    "ase",
    'test',
    'input',
    "math",
    "utils",
    "dft",
    "QE",

]


def register_class():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    enable_module("scinode_editor.nodes.", modules)



def unregister_class():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    disable_module("scinode_editor.nodes.", modules)


if __name__ == "__main__":
    register_class()
