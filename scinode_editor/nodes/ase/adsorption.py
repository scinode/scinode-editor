

import bpy
from scinode_editor.nodes.base_node import BaseNode, update_sockets

func_items = [
("Index", "Index", "", 0),
("Site", "Site", "", 1),
]

class ASEAdsorption(BaseNode):
    bl_idname = 'ASEAdsorption'
    dtype = 'ASEAdsorption'
    bl_label = "Adsorption"

    Method: bpy.props.EnumProperty(
        name="Method",
        description="method.",
        items=func_items,
        default='Index',
        update=update_sockets,
    )

    properties = ["Method"]

    def init(self, context):

        self.inputs.new("ScinodeSocketGeneral", "Substrate")
        self.inputs.new("ScinodeSocketGeneral", "Adsorbate")
        self.inputs.new("ScinodeSocketInt", "Attach_atom")
        if self.Method == 'Site':
            self.inputs.new("ScinodeSocketFloatVector3D", "Site")
            self.kwargs = "Method, Height, Site"
        else:
            self.inputs.new("ScinodeSocketInt", "Index")
            self.kwargs = "Method, Height, Index"
        height = self.inputs.new("ScinodeSocketFloat", "Height")
        height.default_value = 2.0
        self.outputs.new("ASEAtoms", "Atoms")
        self.args = "Substrate, Adsorbate, Attach_atom"


    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {
            "path": "scinode_ase.executors.tool",
            "name": "adsorption",
            "type": "function",
        }
