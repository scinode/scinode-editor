import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class DFTVibration(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'DFTVibration'
    bl_label = "Vibration"
    bl_icon = 'FORCE_HARMONIC'

    method: bpy.props.EnumProperty(
        name="Method",
        description="Method.",
        items=(
            ("Standard", "Standard", "Standard"),
            ("Frederiksen", "Frederiksen", "Frederiksen"),
        ),
        default='Standard',
    )

    nstep: bpy.props.IntProperty(default=50)
    delta: bpy.props.FloatProperty(default=0.01)

    def init(self, context):
        self.inputs.new('ScinodeSocketStructure', "Structure")
        self.inputs.new('bnodessocket.calculator', "Calculator")

        self.outputs.new('ScinodeSocketStructure', "Structure")
        self.outputs.new('ScinodeSocketEnergy', "vib")
        self.outputs.new('NodeSocketFloat', "ZPE")

    def draw_buttons(self, context, layout):
        layout.prop(self, "method", text="Method")
        layout.prop(self, "nstep")
        layout.prop(self, "delta")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "nstep")
        layout.prop(self, "delta")
