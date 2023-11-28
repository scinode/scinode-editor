import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class DFTNEB(bpy.types.Node, ScinodeTreeNode):
    '''NEB node'''
    bl_idname = 'DFTNEB'
    bl_label = "NEB"
    bl_icon = 'SMOOTHCURVE'


    neb_method: bpy.props.EnumProperty(
        name="NEB Method",
        description="NEB method.",
        items=(
            ("aseneb", "aseneb", "aseneb"),
            ("improvedtangent", "improvedtangent", "improvedtangent"),
            ("eb", "eb", "eb"),
            ("spline", "spline", "spline"),
            ("string", "string", "string"),
        ),
        default='aseneb',
    )

    interpolate_method: bpy.props.EnumProperty(
        name="interpolate Method",
        description="interpolate method.",
        items=(
            ("linearly", "linearly", "linearly"),
            ("idpp", "idpp", "idpp"),
        ),
        default='linearly',
    )

    nstep: bpy.props.IntProperty(default=50)
    fmax: bpy.props.FloatProperty(default=0.05)
    spring: bpy.props.FloatProperty(name="spring",
                description="Spring constant(s) in eV/Ang.",
                default=0.1)
    climb: bpy.props.BoolProperty(name="climb",
                description="Use a climbing image (default is no climbing image).",
                default=False)
    remove_rotation_and_translation: bpy.props.BoolProperty(name="remove_rotation_and_translation",
                description="TRUE actives NEB-TR for removing translation and rotation during NEB. By default applied non-periodic systems.",
                default=False)

    def init(self, context):
        self.inputs.new('ScinodeSocketStructure', "Start")
        self.inputs.new('ScinodeSocketStructure', "End")
        self.inputs.new('ScinodeSocketCalculator', "Calculator")


        self.outputs.new('ScinodeSocketStructure', "Trajectory")
        self.outputs.new('ScinodeSocketEnergy', "Energy")
        self.outputs.new('ScinodeSocketForce', "Force")


    def draw_buttons(self, context, layout):
        layout.prop(self, "neb_method", text="Method")
        layout.prop(self, "interpolate_method", text="Interpolate")
        layout.prop(self, "spring")
        layout.prop(self, "climb")
        layout.prop(self, "remove_rotation_and_translation")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "nstep")
        layout.prop(self, "fmax")
