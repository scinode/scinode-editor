import bpy
from scinode_editor.nodes.base_node import BaseNode, update_sockets

class ASEFixAtoms(BaseNode):
    bl_idname = "ASEFixAtoms"
    bl_label = "FixAtoms"

    properties = []

    def init(self, context):
        self.args = "Atoms"
        self.kwargs = "Index"
        self.inputs.new("ScinodeSocketGeneral", "Atoms")
        self.inputs.new("ScinodeSocketInt", "Index")
        self.outputs.new("ScinodeSocketGeneral", "Atoms")

    def get_executor(self):
        return {
            "path": "scinode_ase.executors.constraint",
            "name": "fix_atoms",
            "type": "function",
        }
