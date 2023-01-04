
import bpy
from scinode_editor.nodes.base_node import BaseNode

node_names = []


class QEPWParameter(BaseNode):
    bl_idname = "QEPWParameter"
    bl_label = "PWParameter"



    calculation: bpy.props.EnumProperty(name="calculation",
                items = [
                    ("scf", "scf", "", 0),
                    ("relax", "relax", "", 1),
                    ("nscf", "nscf", "", 2),
                    ("bands", "bands", "", 3),
                    ("relax", "relax", "", 4),
                    ("md", "md", "", 5),
                    ("vc-relax", "vc-relax", "", 6),
                    ("vc-md", "vc-md", "", 7),],
                default=0)
    ecutwfc: bpy.props.FloatProperty(name="ecutwfc", default=30)
    occupations: bpy.props.EnumProperty(name="occupations",
                items = [
                    ("smearing", "smearing", "", 0),
                    ("tetrahedra", "tetrahedra", "", 1),
                    ("tetrahedra_lin", "tetrahedra_lin", "", 2),
                    ("tetrahedra_opt", "tetrahedra_opt", "", 3),
                    ("fixed", "fixed", "", 4),
                    ("from_input", "from_input", "", 5),],
                default=0)
    smearing: bpy.props.EnumProperty(name="smearing",
                items = [
                    ("gaussian", "gaussian", "", 0),
                    ("methfessel-paxton", "methfessel-paxton", "", 1),
                    ("marzari-vanderbilt", "marzari-vanderbilt", "", 2),
                    ("fermi-dirac", "fermi-dirac", "", 3),],
                default=0)
    degauss: bpy.props.FloatProperty(name="degauss", default=0.02)
    nspin: bpy.props.IntProperty(name="nspin", default=1)
    properties = ['calculation', 'ecutwfc', 'occupations', 'smearing', 'degauss', 'nspin']


    def init(self, context):
        self.args = ""
        self.kwargs = "calculation,ecutwfc,occupations,smearing,degauss,nspin"
        self.outputs.new("ScinodeSocketGeneral", "Parameter")

    def get_executor(self):
        return {'path': 'scinode.executors.built_in', 'name': 'PropertyToSocket', 'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEPWParameter)

class QEDosParameter(BaseNode):
    bl_idname = "QEDosParameter"
    bl_label = "DosParameter"



    deguass: bpy.props.FloatProperty(name="deguass", default=0.01)
    Emin: bpy.props.FloatProperty(name="Emin", default=-10)
    Emax: bpy.props.FloatProperty(name="Emax", default=10)
    DeltaE: bpy.props.FloatProperty(name="DeltaE", default=0.02)
    properties = ['deguass', 'Emin', 'Emax', 'DeltaE']


    def init(self, context):
        self.args = ""
        self.kwargs = "deguass,Emin,Emax,DeltaE"
        self.outputs.new("ScinodeSocketGeneral", "Parameter")

    def get_executor(self):
        return {'path': 'scinode.executors.built_in', 'name': 'PropertyToSocket', 'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEDosParameter)

class QEProjwfcParameter(BaseNode):
    bl_idname = "QEProjwfcParameter"
    bl_label = "ProjwfcParameter"



    deguass: bpy.props.FloatProperty(name="deguass", default=0.01)
    Emin: bpy.props.FloatProperty(name="Emin", default=-10)
    Emax: bpy.props.FloatProperty(name="Emax", default=10)
    DeltaE: bpy.props.FloatProperty(name="DeltaE", default=0.02)
    properties = ['deguass', 'Emin', 'Emax', 'DeltaE']


    def init(self, context):
        self.args = ""
        self.kwargs = "deguass,Emin,Emax,DeltaE"
        self.outputs.new("ScinodeSocketGeneral", "Parameter")

    def get_executor(self):
        return {'path': 'scinode.executors.built_in', 'name': 'PropertyToSocket', 'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEProjwfcParameter)

class QEPseudo_SSSP(BaseNode):
    bl_idname = "QEPseudo_SSSP"
    bl_label = "Pseudo_SSSP"



    Pseudo: bpy.props.EnumProperty(name="Pseudo",
                items = [
                    ("SSSP_1.1.2_PBE_efficiency", "SSSP_1.1.2_PBE_efficiency", "", 0),
                    ("SSSP_1.1.2_PBE_precision", "SSSP_1.1.2_PBE_precision", "", 1),],
                default=0)
    properties = ['Pseudo']


    def init(self, context):
        self.args = ""
        self.kwargs = "Pseudo"
        self.outputs.new("ScinodeSocketString", "Pseudo")

    def get_executor(self):
        return {'path': 'scinode.executors.built_in',
                'name': 'PropertyToSocket',
                'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEPseudo_SSSP)

class QEPW(BaseNode):
    bl_idname = "QEPW"
    bl_label = "PW"



    Directory: bpy.props.StringProperty(name="Directory", default="")
    properties = ['Directory']


    def init(self, context):
        self.args = ""
        self.kwargs = "Directory,Structure,Kpoints,Pseudo,Parameter,Scheduler"
        Structure = self.inputs.new("ScinodeSocketGeneral", "Structure")
        Kpoints = self.inputs.new("ScinodeSocketGeneral", "Kpoints")
        Pseudo = self.inputs.new("ScinodeSocketString", "Pseudo")
        Parameter = self.inputs.new("ScinodeSocketGeneral", "Parameter")
        Scheduler = self.inputs.new("ScinodeSocketGeneral", "Scheduler")
        self.outputs.new("ScinodeSocketGeneral", "Structure")
        self.outputs.new("ScinodeSocketGeneral", "Energy")
        self.outputs.new("ScinodeSocketGeneral", "Force")
        self.outputs.new("ScinodeSocketGeneral", "Calculator")

    def get_executor(self):
        return {'path': 'scinode_ase.executors.qe.pw',
                'name': 'PW',
                'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEPW)

class QEDos(BaseNode):
    bl_idname = "QEDos"
    bl_label = "Dos"



    directory: bpy.props.StringProperty(name="directory", default="")
    prefix: bpy.props.StringProperty(name="prefix", default="")
    properties = ['directory', 'prefix']


    def init(self, context):
        self.args = ""
        self.kwargs = "directory,prefix,Calculator,Parameter,Scheduler"
        Calculator = self.inputs.new("ScinodeSocketGeneral", "Calculator")
        Parameter = self.inputs.new("ScinodeSocketGeneral", "Parameter")
        Scheduler = self.inputs.new("ScinodeSocketGeneral", "Scheduler")
        self.outputs.new("ScinodeSocketGeneral", "Energies")
        self.outputs.new("ScinodeSocketGeneral", "Dos")

    def get_executor(self):
        return {'path': 'scinode_ase.executors.qe.dos', 'name': 'Dos', 'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEDos)

class QEProjwfc(BaseNode):
    bl_idname = "QEProjwfc"
    bl_label = "Projwfc"



    directory: bpy.props.StringProperty(name="directory", default="")
    prefix: bpy.props.StringProperty(name="prefix", default="")
    properties = ['directory', 'prefix']


    def init(self, context):
        self.args = ""
        self.kwargs = "directory,prefix,Calculator,Parameter,Scheduler"
        Calculator = self.inputs.new("ScinodeSocketGeneral", "Calculator")
        Parameter = self.inputs.new("ScinodeSocketGeneral", "Parameter")
        Scheduler = self.inputs.new("ScinodeSocketGeneral", "Scheduler")
        self.outputs.new("ScinodeSocketGeneral", "Energies")
        self.outputs.new("ScinodeSocketGeneral", "Pdos")

    def get_executor(self):
        return {'path': 'scinode_ase.executors.qe.projwfc', 'name': 'Projwfc', 'type': 'class'}

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text=key)

node_names.append(QEProjwfc)
def register_class():
    from bpy.utils import register_class
    for name in node_names:
        register_class(name)

def unregister_class():
    from bpy.utils import unregister_class
    for name in node_names:
        unregister_class(name)
