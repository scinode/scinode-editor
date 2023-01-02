

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode, update_sockets

func_items = [
    ("combine_vector", "Combine", "", 0),
    ("seperate_vector", "Seperate", "", 1),
]


class Vector3DMath(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Vector3DMath'
    dtype = 'Vector3DMath'
    bl_label = "Vector_Math"

    function: bpy.props.EnumProperty(
        name="function",
        description="function.",
        items=func_items,
        default='combine_vector',
        update=update_sockets,
    )

    properties = ["function"]

    def init(self, context):
        if self.function == 'combine_vector':
            self.inputs.new("ScinodeSocketFloat", "X")
            self.inputs.new("ScinodeSocketFloat", "Y")
            self.inputs.new("ScinodeSocketFloat", "Z")
            self.outputs.new("ScinodeSocketFloat", "Result")
            self.args = "X, Y, Z"
        elif self.function == 'seperate_vector':
            self.inputs.new("ScinodeSocketFloatVector3D", "Vector")
            self.outputs.new("ScinodeSocketFloat", "X")
            self.outputs.new("ScinodeSocketFloat", "Y")
            self.outputs.new("ScinodeSocketFloat", "Z")
            self.args = "Vector"

    def draw_buttons(self, context, layout):
        layout.prop(self, "function", text="")

    def get_executor(self):
        return {"path": "scinode_math.vector",
                "name": self.function,
                "type": "function",
                }
