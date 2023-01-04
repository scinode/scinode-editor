

import bpy
from scinode_editor.nodes.base_node import BaseNode


class Update(BaseNode):
    bl_idname = 'Update'
    dtype = 'Update'
    bl_label = "Update"
    node_type: str = "Update"

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Input")
        self.inputs.new("ScinodeSocketGeneral", "Update")
        self.outputs.new("ScinodeSocketGeneral", "Result")
        self.kwargs = "Input, Update"

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.update_node",
            "name": "ScinodeUpdate",
            "type": "class",
        }
