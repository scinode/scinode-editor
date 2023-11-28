import bpy
from scinode_editor.nodes.base_node import BaseNode


class SurfaceAnalysis(BaseNode):
    bl_idname = 'SurfaceAnalysis'
    bl_label = "Surface Analysis"

    height: bpy.props.FloatProperty(name="height", default=2.0)

    properties = {"height": "kwargs"}

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Surface")
        self.outputs.new("ScinodeSocketGeneral", "Ontop")
        self.outputs.new("ScinodeSocketGeneral", "Bridge")
        self.outputs.new("ScinodeSocketGeneral", "Hollow")
        # self.outputs.new("ScinodeSocketGeneral", "Index")

    def draw_buttons(self, context, layout):
        layout.prop(self, "height", text="height")

    def get_executor(self):
        return {"path": "xnodes.executors.pymatgen.surface",
                "name": "SurfaceAnalysis",
                "has_run": True,
                }
