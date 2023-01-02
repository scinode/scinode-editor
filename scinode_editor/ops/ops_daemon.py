import bpy
import bmesh
from bpy.types import Operator
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       IntProperty,
                       EnumProperty,
                       )

class DaemonStop(Operator):
    bl_idname = "scinode.daemon_stop"
    bl_label = "Stop daemon"
    bl_description = ("Stop daemon")
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        from scinode.daemon.daemon import ScinodeDaemon
        index = context.scene.Scinode.ui_list_index_daemon
        daemon = context.scene.Scinode.settings_daemon[index]
        daemon = ScinodeDaemon(daemon.name)
        daemon.stop()
        self.report({"INFO"}, f'Daemon<{daemon.name}> is Stopped')
        bpy.ops.scinode.daemon_update()
        return {'FINISHED'}


class DaemonStart(Operator):
    bl_idname = "scinode.daemon_start"
    bl_label = "Start daemon"
    bl_description = ("Start daemon")
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        from scinode.daemon.daemon import ScinodeDaemon
        index = context.scene.Scinode.ui_list_index_daemon
        daemon = context.scene.Scinode.settings_daemon[index]
        daemon = ScinodeDaemon(daemon.name)
        daemon.start()
        self.report({"INFO"}, f'Daemon<{daemon.name}> is Stopped')
        bpy.ops.scinode.daemon_update()
        return {'FINISHED'}

class DaemonUpdate(Operator):
    bl_idname = "scinode.daemon_update"
    bl_label = "Update daemon"
    bl_description = ("Update daemon list")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        from scinode.database.daemon import DaemonDB
        scinode = context.scene.Scinode
        scinode.settings_daemon.clear()
        daemondb = DaemonDB()
        data = daemondb.get_data(0)
        for d in data:
            item = scinode.settings_daemon.add()
            item.name = d['name']
            item.lastUpdate = d["lastUpdate"]
            item.pid = d["pid"]
        return {'FINISHED'}
