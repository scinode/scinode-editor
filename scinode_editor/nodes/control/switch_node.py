

import bpy
from scinode_editor.nodes.base_node import BaseNode


class Switch(BaseNode):
    bl_idname = 'Switch'
    dtype = 'Switch'
    bl_label = "Switch"
    node_type: str = "Switch"

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Input")
        self.inputs.new("ScinodeSocketBool", "Switch")
        self.outputs.new("ScinodeSocketGeneral", "Result")
        self.kwargs = "Input, Switch"

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.switch_node",
            "name": "ScinodeSwitch",
            "type": "class",
        }
