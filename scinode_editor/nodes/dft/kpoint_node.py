

import bpy
from scinode_editor.nodes.base_node import BaseNode


class DFTKpoints(BaseNode):
    bl_idname = "DFTKpoints"
    bl_label = "Kpoints"

    size: bpy.props.IntVectorProperty(name="size", size=3, default=[1, 1, 1])
    offset: bpy.props.FloatVectorProperty(name="offset", size=3, default=[0.0, 0.0, 0.0])
    properties = ['size', 'offset']


    def init(self, context):
        self.args = "size"
        self.kwargs = "offset"
        self.outputs.new("ScinodeSocketGeneral", "Kpoints")

    def get_executor(self):
        return {'path': 'scinode_ase.executors.dft',
                'name': 'kpoints',
                'type': "function"}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)
