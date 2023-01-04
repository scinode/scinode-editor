"""
"""

import bpy
from bpy.types import UIList

from scinode_editor.gui.gui_nodetree import ScinodeBasePanel

class VIEW3D_PT_Scinode_Daemon(ScinodeBasePanel):
    bl_label = "Daemon"
    bl_idname = "VIEW3D_PT_Scinode_Daemon"
    # bl_parent_id = 'VIEW3D_PT_Scinode'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        p = context.scene.scinode_daemon
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        # col.prop(p, "running")
        # col.prop(p, "waiting")
        # col.prop(p, "finished")
        # col.prop(p, "limit")
        # col.prop(p, "past_days")
        # op = col.operator("scinode.daemon_update",
                            #  icon='FILE_REFRESH', text="Update daemon")
        # op.running=p.running
        # op.waiting=p.waiting
        # op.finished=p.finished
        # op.limit=p.limit
        # op.past_days=p.past_days

class SCINODE_UL_Daemon(UIList):
    def draw_item(self, _context, layout, _data, item, icon, active_data, _active_propname, index):
        daemon = item
        custom_icon = 'OBJECT_DATAMODE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.30, align=False)
            split.prop(daemon, "name", text="",
                       emboss=False)
            row = split.row()#align=True)
            row.emboss = 'NONE_OR_STATUS'
            row.prop(daemon, "computer", text="")
            row.prop(daemon, "pid", text="")
            row.prop(daemon, "lastUpdate", text="")
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon=custom_icon)


class SCINODE_PT_Daemon(ScinodeBasePanel):
    bl_label = "Daemon list"
    bl_idname = "SCINODE_PT_Daemon"
    # bl_parent_id = 'VIEW3D_PT_Scinode'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        ba = context.scene.Scinode
        if len(ba.settings_daemon) > 0:
            ui_list_index_daemon = min(ba.ui_list_index_daemon, len(ba.settings_daemon) - 1)
            kb = ba.settings_daemon[ui_list_index_daemon]
        else:
            kb = None

        row = layout.row()

        rows = 3
        if kb:
            rows = 5
        row.template_list("SCINODE_UL_Daemon", "", ba,
                          "settings_daemon", ba, "ui_list_index_daemon", rows=rows)

        col = row.column(align=True)
        op = col.operator("scinode.daemon_update", icon='FILE_REFRESH', text="")
        op = col.operator("scinode.daemon_stop", icon='PAUSE', text="")
        op = col.operator("scinode.daemon_start", icon='PLAY', text="")
        # op = col.operator("scinode.daemon_delete", icon='REMOVE', text="")
        col.separator()

        if kb:
            col.separator()

            sub = col.column(align=True)

            split = layout.split(factor=0.4)
            row = split.row()

            row = split.row()
            row.alignment = 'RIGHT'

            sub = row.row(align=True)
            sub.label()  # XXX, for alignment only

            sub = row.row()
            layout.use_property_split = True
            row = layout.row()
            row.prop(kb, "name", text="name")
            col = layout.column()
            sub = col.column(align=True)
            sub.prop(kb, "workdir", text="workdir")
            sub.prop(kb, "pid", text="pid")
            sub.prop(kb, "lastUpdate", text="lastUpdate")
