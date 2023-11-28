

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class DFTOER(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'DFTOER'
    bl_label = "OER"

    site: bpy.props.EnumProperty(
        name="site",
        description="site.",
        items=[("Normal", "Normal", "", 0),
            ("O", "O", "", 1),
            ("H", "H", "", 2),
            ],
        default='Normal',
    )

    properties = {
                "site": "kwargs",
                }

    def init(self, context):
        self.inputs.new("ScinodeSocketFloat", "H2O")
        self.inputs.new("ScinodeSocketFloat", "H2")
        self.inputs.new("ScinodeSocketFloat", "OH")
        self.inputs.new("ScinodeSocketFloat", "O")
        self.inputs.new("ScinodeSocketFloat", "OOH")
        self.outputs.new("ScinodeSocketGeneral", "OverPotential")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Energy")

    def draw_buttons(self, context, layout):
        layout.prop(self, "site", text="")


    def get_executor(self):
        return {"path": "xnodes.executors.dft.oer_node",
                "name": "OER",
                "has_run": True,
                }
