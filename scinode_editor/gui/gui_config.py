

import bpy
from bpy.types import Menu, Panel, UIList
from bpy.props import (
    BoolProperty,
    FloatProperty,
    EnumProperty,
    StringProperty,
)
from scinode_editor.gui.gui_nodetree import ScinodeBasePanel

class SCINODE_PT_config(ScinodeBasePanel):
    bl_label = "Configuration"
    bl_idname = "SCINODE_PT_config"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass
