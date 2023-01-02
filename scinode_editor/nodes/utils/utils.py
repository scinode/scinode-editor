

import bpy
from bpy.types import Node
from scinode_editor.nodes.base_node import ScinodeTreeNode


class Print(Node, ScinodeTreeNode):
    bl_idname = 'Print'
    dtype = 'Print'
    bl_label = "Print"

    debug_text: bpy.props.StringProperty(name="debug_text", default='')

    properties = {}

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Input")
        self.kwargs = "Input"

    def draw_buttons(self, context, layout):
        texts = self.debug_text.split(',')
        for text in texts:
            layout.label(text=text)

    def output(self):
        pass

    def get_executor(self):
        return {
            "path": "scinode.executors.built_in",
            "name": "PropertyToSocket",
            "type": "class",
        }

    def update_state(self):
        """Update the debug text.
        """
        data = self.get_dbdata({"uuid": self.uuid})
        if data is None:
            return
        inputs = self.get_input_parameters_from_db()
        if inputs is None:
            return
        if 'Input' in inputs:
            text = inputs['Input']['value']
            text = str(text)
            # multilines
            n = len(text)
            text = text[0:min(n, 1000)]
            self.debug_text = text
            print(self.debug_text)



class Input_to_Output(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "UtilsInput_to_Output"
    bl_label = "Input_to_Output"

    properties = []

    def init(self, context):
        self.args = "Input"
        self.kwargs = ""
        Input = self.inputs.new("ScinodeSocketGeneral", "Input")
        self.outputs.new("ScinodeSocketGeneral", "Output")

    def get_executor(self):
        return {'path': 'scinode.executors.built_in', 'name': 'InputToSocket', 'has_run': False}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)
