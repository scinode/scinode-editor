import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       FloatVectorProperty,
                       PointerProperty,
                       CollectionProperty,
                       )


class ScinodeDaemon(bpy.types.PropertyGroup):
    """
    """
    name: StringProperty(name="name", default='')
    pid: IntProperty(name="pid", default=0)
    workdir: StringProperty(name="workdir", default="")
    lastUpdate: IntProperty(name="lastUpdate", default=100)

    def as_dict(self) -> dict:
        setdict = {
            'name': self.name,
            'lastUpdate': self.lastUpdate,
            'pid': self.pid,
            'workdir': self.workdir,
        }
        return setdict


class Scinode(bpy.types.PropertyGroup):
    """This module defines the cavity properties to extend
    Blender’s internal data.

    """

    settings_daemon: CollectionProperty(name='ScinodeDaemon',
                                         type=ScinodeDaemon)
    process: PointerProperty(name='ScinodeDaemon',
                             type=ScinodeDaemon)
    ui_list_index_daemon: IntProperty(name="ui_list_index_daemon",
                                       default=0)

    def as_dict(self) -> dict:
        setdict = {
        }
        return setdict
