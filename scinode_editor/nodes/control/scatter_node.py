

import bpy
from scinode_editor.nodes.base_node import BaseNode


class Scatter(BaseNode):
    bl_idname = 'Scatter'
    dtype = 'Scatter'
    bl_label = "Scatter"
    node_type: str = "Scatter"

    properties = []

    def init(self, context):
        socket = self.inputs.new("ScinodeSocketGeneral", "Input")
        socket.link_limit = 100
        socket = self.inputs.new("ScinodeSocketGeneral", "Stop")
        socket.link_limit = 100
        self.outputs.new("ScinodeSocketGeneral", "Result")
        self.kwargs = "Input, Stop"

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.scatter_node",
            "name": "ScinodeScatter",
            "type": "class",
        }
