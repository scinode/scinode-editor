import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class DFTOptmizer(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'DFTOptmizer'
    bl_label = "Optimizer"
    bl_icon = 'IPO_ELASTIC'

    optimize_method: bpy.props.EnumProperty(
        name="Optimize Method",
        description="Optimize method.",
        items=(
            ("BFGS", "BFGS", "BFGS"),
            ("LBFGS", "LBFGS", "LBFGS"),
            ("MDMin", "MDMin", "MDMin"),
            ("QuasiNewton", "QuasiNewton", "QuasiNewton"),
        ),
        default='BFGS',
    )

    nstep: bpy.props.IntProperty(default=50)
    fmax: bpy.props.FloatProperty(default=0.05)

    def init(self, context):
        self.inputs.new('ScinodeSocketStructure', "Structure")
        self.inputs.new('ScinodeSocketCalculator', "Calculator")

        self.outputs.new('ScinodeSocketStructure', "Trajectory")
        self.outputs.new('ScinodeSocketEnergy', "Energy")
        self.outputs.new('ScinodeSocketForce', "Force")

    def draw_buttons(self, context, layout):
        layout.prop(self, "optimize_method", text="Method")
        layout.prop(self, "nstep")
        layout.prop(self, "fmax")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "nstep")
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "fmax")
