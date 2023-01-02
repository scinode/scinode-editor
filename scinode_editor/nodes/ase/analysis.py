

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode, update_sockets


class ASEAtomsAttribute(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'ASEAtomsAttribute'
    dtype = 'ASEAtomsAttribute'
    bl_label = "AtomsAttribute"


    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Atoms")
        self.kwargs = "Atoms"
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {"path": "scinode_ase.analysis.atoms_attribute",
                "name": "atoms_attribute",
                "type": "function",
                }

class ASEEOS(bpy.types.Node, ScinodeTreeNode):
    bl_idname = "ASEEOS"
    bl_label = "EOS"

    properties = []


    def init(self, context):
        self.args = ""
        self.kwargs = "Structures,Energies"
        Structures = self.inputs.new("ScinodeSocketGeneral", "Structures")
        Energies = self.inputs.new("ScinodeSocketGeneral", "Energies")
        self.outputs.new("ScinodeSocketFloat", "V0")
        self.outputs.new("ScinodeSocketFloat", "E0")
        self.outputs.new("ScinodeSocketFloat", "B")

    def get_executor(self):
        return {'path': 'scinode_ase.executors.analysis',
                'name': 'eos',
                'type': 'function'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)
