import bpy
from bpy.types import Panel
from bpy.props import (
    IntProperty,
    BoolProperty,
)
from scinode_editor.handlers import register, unregister

class ScinodeBasePanel(Panel):
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Scinode"

    @classmethod
    def poll(cls, context):
        if context.space_data.node_tree is not None:
            nodetree = context.space_data.node_tree
            return nodetree.bl_idname == "ScinodeTree"
        return False

class SCINODE_PT_NodeTreePanel(ScinodeBasePanel):
    bl_label = "Node Tree"
    bl_idname = 'SCINODE_PT_NodeTreePanel'


    def draw(self, context):
        nt = context.space_data.node_tree
        ntpanel = context.scene.ntpanel
        layout = self.layout
        row = layout.row()
        col = layout.column()
        col.prop(nt, 'daemon_name')
        col.prop(ntpanel, 'auto_update_state')
        col.operator('scinode.nodetree_launch', text="Launch", icon = "AUTO")
        col.separator()
        col.operator('scinode.nodetree_update_state', text="Update state", icon = "FILE_REFRESH")
        col.separator()
        col.operator('scinode.nodetree_reset', text="Reset", icon = "PLAY_REVERSE")
        col.separator()
        col.operator('scinode.nodetree_export', text="Export", icon = "EXPORT")
        col.separator()




class NodetreeProperties(bpy.types.PropertyGroup):

    def Callback_auto_update_state(self, context):
        from scinode_editor.handlers import register, unregister
        if self.auto_update_state:
            register()
        else:
            unregister()

    auto_update_state: BoolProperty(name="auto_update_state",
                       default=False,
                       description="Auto update state",
                       update=Callback_auto_update_state,
                       )
