

import bpy
from scinode_editor.nodes.base_node import BaseNode, update_sockets


class ASEAtoms(BaseNode):
    """
    """
    bl_idname = 'ASEAtoms'
    dtype = 'ASEAtoms'
    bl_label = "Atoms"

    properties = []

    def init(self, context):
        symbols = self.inputs.new("ScinodeSocketString", "symbols")
        symbols.default_value = 'H'
        self.inputs.new("ScinodeSocketGeneral", "positions")
        self.outputs.new("ASEAtoms", "Atoms")
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")
        self.args = ""
        self.kwargs = "symbols, positions"

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {
            "path": "scinode_ase.executors.build.atoms",
            "name": "atoms",
            "type": "function",
        }



class ASEBulk(BaseNode):
    """
    """
    bl_idname = 'ASEBulk'
    dtype = 'ASEBulk'
    bl_label = "Bulk"


    properties = []

    def init(self, context):
        name = self.inputs.new("ScinodeSocketString", "name")
        name.default_value = 'Pt'
        self.inputs.new("ScinodeSocketString", "crystalstructure")
        self.inputs.new("ScinodeSocketFloat", "a")
        self.inputs.new("ScinodeSocketFloat", "b")
        self.inputs.new("ScinodeSocketFloat", "c")
        self.inputs.new("ScinodeSocketFloat", "alpha")
        self.inputs.new("ScinodeSocketBool", "orthorhombic")
        self.inputs.new("ScinodeSocketBool", "cubic")
        self.args = "name"
        self.kwargs = "crystalstructure, a, b, c, alpha, orthorhombic, cubic"
        self.outputs.new("ASEAtoms", "Atoms")
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {"path": "scinode_ase.executors.build.bulk",
                "name": "bulk",
                "type": "function",
                }


class ASEMolecule(BaseNode):
    bl_idname = 'ASEMolecule'
    dtype = 'ASEMolecule'
    bl_label = "Molecule"

    properties = []

    def init(self, context):
        formula = self.inputs.new("ScinodeSocketString", "formula")
        formula.default_value = 'H2O'
        self.inputs.new("ScinodeSocketFloat", "vacuum")
        self.args = "formula"
        self.kwargs = "vacuum"
        self.outputs.new("ASEAtoms", "Atoms")
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {"path": "scinode_ase.executors.build.molecule",
                "name": "molecule",
                "type": "function",
                }




func_items = [
("fcc100", "fcc100", "", 0),
("fcc110", "fcc110", "", 1),
("fcc111", "fcc111", "", 2),
("fcc211", "fcc211", "", 3),
("fcc111_root", "fcc111_root", "", 4),
("bcc100", "bcc100", "", 5),
("bcc110", "bcc110", "", 6),
("bcc111", "bcc111", "", 7),
("bcc111_root", "bcc111_root", "", 8),
("hcp10m10", "hcp10m10", "", 9),
("hcp0001", "hcp0001", "", 10),
("hcp0001_root", "hcp0001_root", "", 11),
("diamond100", "diamond100", "", 12),
("diamond111", "diamond111", "", 13),
]

class ASESurface(BaseNode):
    bl_idname = 'ASESurface'
    dtype = 'ASESurface'
    bl_label = "Surface"

    function: bpy.props.EnumProperty(
        name="function",
        description="function.",
        items=func_items,
        default='fcc111',
        update=update_sockets,
    )

    properties = ["function"]

    def init(self, context):
        symbol = self.inputs.new("ScinodeSocketString", "symbol")
        symbol.default_value = 'Pt'
        size = self.inputs.new("ScinodeSocketIntVector3D", "size")
        size.default_value = [1, 1, 4]
        self.inputs.new("ScinodeSocketFloat", "a")
        if self.function in ['fcc100', 'fcc110', 'fcc111', 'fcc211',
                             'bcc100', 'bcc110', 'bcc111',
                             'diamond100', 'diamond111']:
            print("function: ", self.function)
            vacuum = self.inputs.new("ScinodeSocketFloat", "vacuum")
            vacuum.default_value = 5.0
            self.inputs.new("ScinodeSocketBool", "orthogonal")
            periodic = self.inputs.new("ScinodeSocketBool", "periodic")
            periodic.default_value = True
            self.args = "symbol"
            self.kwargs = "function, size, a, vacuum, orthogonal, periodic"
        elif self.function in ['hcp0001', 'hcp10m10']:
            print("function: ", self.function)
            self.inputs.new("ScinodeSocketFloat", "c")
            vacuum = self.inputs.new("ScinodeSocketFloat", "vacuum")
            vacuum.default_value = 5.0
            self.inputs.new("ScinodeSocketBool", "orthogonal")
            periodic = self.inputs.new("ScinodeSocketBool", "periodic")
            periodic.default_value = True
            self.args = "symbol"
            self.kwargs = "function, size, a, c, vacuum, orthogonal, periodic"
        self.outputs.new("ASEAtoms", "Atoms")
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")

    def draw_buttons(self, context, layout):
        layout.prop(self, "function", text="")

    def get_executor(self):
        return {"path": "scinode_ase.executors.build.surface",
                "name": "surface",
                "type": "function",
                }
