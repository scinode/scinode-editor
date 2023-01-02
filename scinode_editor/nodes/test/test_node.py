

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class TestFloat(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'TestFloat'
    bl_label = "Float Node"
    bl_icon = "VIEW_ORTHO"

    Float: bpy.props.FloatProperty(name="Float", default=0.0)

    properties = ["Float"]

    def init(self, context):
        self.kwargs = "Float"
        self.outputs.new("ScinodeSocketFloat", "Float")

    def draw_buttons(self, context, layout):
        layout.prop(self, "Float", text="Float")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_float",
        }

class TestAdd(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'TestAdd'
    bl_label = "Add Node"
    bl_icon = "VIEW_ORTHO"

    t: bpy.props.FloatProperty(name="t", default=0.0)

    properties = ["t"]

    def init(self, context):
        self.inputs.new("ScinodeSocketFloat", "x")
        self.inputs.new("ScinodeSocketFloat", "y")
        self.outputs.new("ScinodeSocketFloat", "Result")
        self.kwargs = "t, x, y"

    def draw_buttons(self, context, layout):
        layout.prop(self, "t", text="t")

    def get_executor(self):
        return {"path": "scinode.executors.test",
                "name": "test_add",
                }

class TestGreater(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'TestGreater'
    bl_label = "Greater Node"
    bl_icon = "VIEW_ORTHO"

    t: bpy.props.FloatProperty(name="t", default=0.0)

    properties = ["t"]


    def init(self, context):
        self.inputs.new("ScinodeSocketFloat", "x")
        self.inputs.new("ScinodeSocketFloat", "y")
        self.outputs.new("ScinodeSocketFloat", "Result")
        self.args = ""
        self.kwargs = "t, x, y"

    def draw_buttons(self, context, layout):
        layout.prop(self, "t", text="t")

    def get_executor(self):
        return {"path": "scinode.executors.test",
                "name": "test_greater",
                }

class TestLess(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'TestLess'
    bl_label = "Less Node"
    bl_icon = "VIEW_ORTHO"

    t: bpy.props.FloatProperty(name="t", default=0.0)

    properties = ["t"]


    def init(self, context):
        self.inputs.new("ScinodeSocketFloat", "x")
        self.inputs.new("ScinodeSocketFloat", "y")
        self.outputs.new("ScinodeSocketFloat", "Result")
        self.args = ""
        self.kwargs = "t, x, y"

    def draw_buttons(self, context, layout):
        layout.prop(self, "t", text="t")

    def get_executor(self):
        return {"path": "scinode.executors.test",
                "name": "test_less",
                }

class TestRange(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'TestRange'
    bl_label = "Range Node"
    bl_icon = "VIEW_ORTHO"

    t: bpy.props.FloatProperty(name="t", default=0.0)

    properties = ["t"]


    def init(self, context):
        self.inputs.new("ScinodeSocketInt", "start")
        self.inputs.new("ScinodeSocketInt", "stop")
        self.inputs.new("ScinodeSocketInt", "step")
        self.outputs.new("ScinodeSocketGeneral", "Result")
        self.kwargs = "start, stop, step"

    def draw_buttons(self, context, layout):
        layout.prop(self, "t", text="t")

    def get_executor(self):
        return {
            "path": "scinode.executors.test",
            "name": "test_range",
        }
