import bpy
from scinode_editor.nodes.base_node import BaseNode


class GeneralInput(BaseNode):
    bl_idname = 'GeneralInput'
    bl_label = "Float"

    Input: bpy.props.FloatProperty(name="Integer", default=0.0)

    properties = {'Input': 'kwargs'}

    def init(self, context):
        self.outputs.new("ScinodeSocketFloat", "Result")

    def draw_buttons(self, context, layout):
        layout.prop(self, "Input", text="")

    def get_executor(self):
        return {"path": "xnodes.executors.return_inputs",
                "name": "PropertyToSocket",
                "type": "class",
                }
