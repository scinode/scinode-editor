
import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode

class Getattr(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "Getattr"
    bl_label = "Getattr"


    properties = []

    def init(self, context):
        self.kwargs = ""
        self.args = "Source, Name"
        self.inputs.new("ScinodeSocketGeneral", "Source")
        self.inputs.new("ScinodeSocketString", "Name")
        self.outputs.new("ScinodeSocketGeneral", "Result")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "getattr",
            "type": "function",
        }

class Setattr(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "Setattr"
    bl_label = "Setattr"


    properties = []

    def init(self, context):
        self.kwargs = ""
        self.args = "Source, Name, Value"
        self.inputs.new("ScinodeSocketGeneral", "Source")
        self.inputs.new("ScinodeSocketString", "Name")
        self.inputs.new("ScinodeSocketString", "Value")
        self.outputs.new("ScinodeSocketGeneral", "Result")

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setattr",
            "type": "function",
        }


class Getitem(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "Getitem"
    bl_label = "Getitem"


    properties = []

    def init(self, context):
        self.kwargs = ""
        self.args = "Source, Index"
        self.inputs.new("ScinodeSocketGeneral", "Source")
        self.inputs.new("ScinodeSocketInt", "Index")
        self.outputs.new("ScinodeSocketGeneral", "Result")

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "getitem",
            "type": "function",
        }


class Setitem(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "Setitem"
    bl_label = "Setitem"


    properties = []

    def init(self, context):
        self.kwargs = ""
        self.args = "Source, Index, Value"
        self.inputs.new("ScinodeSocketGeneral", "Source")
        self.inputs.new("ScinodeSocketInt", "Index")
        self.inputs.new("ScinodeSocketGeneral", "Value")
        self.outputs.new("ScinodeSocketGeneral", "Result")

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setitem",
            "type": "function",
        }


node_list = [
    Getattr,
    Setattr,
    Getitem,
    Setitem,
]

def register_class():
    from bpy.utils import register_class
    for name in node_list:
        register_class(name)

def unregister_class():
    from bpy.utils import unregister_class
    for name in node_list:
        unregister_class(name)
