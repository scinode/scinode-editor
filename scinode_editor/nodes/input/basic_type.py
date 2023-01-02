import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class Integer(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Integer'
    bl_label = "Integer"

    Integer: bpy.props.IntProperty(name="Integer", default=0)

    properties = ["Integer"]

    def init(self, context):
        self.nodetree = self.id_data
        self.outputs.new("ScinodeSocketInt", "Integer")
        self.kwargs = "Integer"

    def draw_buttons(self, context, layout):
        layout.prop(self, "Integer", text="")

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "PropertyToSocket",
            "type": "class",
        }


class Float(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Float'
    bl_label = "Float"

    Float: bpy.props.FloatProperty(name="Float", default=0.0)

    properties = ["Float"]

    def init(self, context):
        self.outputs.new("ScinodeSocketFloat", "Float")
        self.kwargs = "Float"

    def draw_buttons(self, context, layout):
        layout.prop(self, "Float", text="")

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "PropertyToSocket",
            "type": "class",
        }



class String(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'String'
    bl_label = "String"

    String: bpy.props.StringProperty(name="String", default="")

    properties = ["String"]

    def init(self, context):
        self.outputs.new("ScinodeSocketString", "String")
        self.kwargs = "String"

    def draw_buttons(self, context, layout):
        layout.prop(self, "String", text="")

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "PropertyToSocket",
            "type": "class",
        }


class Bool(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Bool'
    bl_label = "Bool"

    Bool: bpy.props.BoolProperty(name="Bool", default=True)

    properties = ["Bool"]

    def init(self, context):
        self.outputs.new("ScinodeSocketBool", "Bool")
        self.kwargs = "Bool"

    def draw_buttons(self, context, layout):
        layout.prop(self, "Bool", text="")

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "PropertyToSocket",
            "type": "class",
        }
