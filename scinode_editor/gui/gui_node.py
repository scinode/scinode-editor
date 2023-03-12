from bpy.types import Operator, Panel
from bpy.props import (
    IntProperty,
    EnumProperty,
)

from scinode_editor.gui.gui_nodetree import ScinodeBasePanel

class SCINODE_PT_NodePanel(ScinodeBasePanel):
    bl_label = "Node"
    bl_idname = 'SCINODE_PT_NodePanel'

    state: EnumProperty(
            name="state",
            items=[('CREATE', 'CREATE', '', 0),
                ('LAUNCH', 'LAUNCH', '', 1),
                ('RUNNING', 'RUNNING', '', 2),
                ('PAUSED', 'PAUSED', '', 3),
                ('CANCELLED', 'CANCELLED', '', 4),
                ('FINISHED', 'FINISHED', '', 5),
                ('SKIPPED', 'SKIPPED', '', 6)],
            description="",
            default=0,
        )

    def draw(self, context):
        if context.active_node is not None:
            layout = self.layout

            node = context.active_node

            layout.prop(node, "name")
            layout.prop(node, "label")
            layout.prop(node, "state")
            layout.prop(node, "action")
            col = layout.column()
            col.prop(node, 'daemon_name')
            col.prop(node, 'node_type')
            col.prop(node, 'uuid')
            col.operator('scinode.node_update_state', text="Update state", icon = "FILE_REFRESH")
            col.separator()
            col.operator('scinode.node_reset', text="Reset state", icon = "PLAY_REVERSE")
            col.operator('scinode.node_pause', text="Pause", icon = "PAUSE")
            col.operator('scinode.node_play', text="Play", icon = "PLAY")
            col.operator('scinode.node_cancel', text="Calcel", icon = "CANCEL")
