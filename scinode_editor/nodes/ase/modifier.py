import bpy
from scinode_editor.nodes.base_node import BaseNode, update_sockets


class ASECellTransformatoin(BaseNode):
    bl_idname = 'ASECellTransformatoin'
    dtype = 'ASECellTransformatoin'
    bl_label = "CellTransformatoin"

    tol: bpy.props.FloatProperty(name="tol", default=1e-5)
    wrap: bpy.props.BoolProperty(name="wrap", default=True)
    properties = ["tol", "wrap"]

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "prim")
        mat = self.inputs.new("ScinodeSocketFloatMatrix3D", "P")
        mat.i = [1, 0, 0]
        mat.j = [0, 1, 0]
        mat.k = [0, 0, 1]
        self.outputs.new("ScinodeSocketGeneral", "Atoms")
        self.args = "prim, P"
        self.kwargs = "wrap, tol"

    def draw_buttons(self, context, layout):
        layout.prop(self, "tol", text="tol")
        layout.prop(self, "wrap", text="wrap")


    def get_executor(self):
        return {
            "path": "ase.build",
            "name": "make_supercell",
            "type": "function",
        }



class ASEReplaceAtoms(BaseNode):
    bl_idname = 'ASEReplaceAtoms'
    dtype = 'ASEReplaceAtoms'
    bl_label = "ReplaceAtoms"

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Atoms")
        self.inputs.new("ScinodeSocketInt", "Index")
        self.inputs.new("ScinodeSocketString", "Value")
        self.outputs.new("ScinodeSocketGeneral", "Atoms")
        self.args = "Atoms, Index, Value"
        self.kwargs = ""

    def draw_buttons(self, context, layout):
        pass


    def get_executor(self):
        return {
            "path": "scinode_ase.executors.modifier",
            "name": "replace",
            "type": "function",
        }


class ASEDeleteAtoms(BaseNode):
    bl_idname = 'ASEDeleteAtoms'
    dtype = 'ASEDeleteAtoms'
    bl_label = "DeleteAtoms"

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Atoms")
        self.inputs.new("ScinodeSocketInt", "Index")
        self.outputs.new("ScinodeSocketGeneral", "Atoms")
        self.args = "Atoms, Index"
        self.kwargs = ""

    def draw_buttons(self, context, layout):
        pass


    def get_executor(self):
        return {
            "path": "scinode_ase.executors.modifier",
            "name": "delete",
            "type": "function",
        }
