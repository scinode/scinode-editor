import bpy
from bpy.types import NodeSocket
import numpy as np


class ScinodeSocket(NodeSocket):
    '''Scinode socket type'''
    bl_idname = 'ScinodeSocket'
    bl_label = "Scinode Socket "

    default_value: bpy.props.FloatProperty(
        name="Value",
        description="float value",
        default=0.0,
    )

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 1, 0.5)

    def get_default_value(self):
        return self.default_value

    def set_default_value(self, value):
        self.default_value = value

class ScinodeSocketGeneral(ScinodeSocket):
    '''Scinode socket General type'''
    bl_idname = 'ScinodeSocketGeneral'
    bl_label = "Scinode Socket General"


    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def get_default_value(self):
        return None

    def set_default_value(self, value):
        pass

class ScinodeSocketFloat(ScinodeSocket):
    bl_idname = 'ScinodeSocketFloat'
    bl_label = "Scinode Socket Float"

    default_value: bpy.props.FloatProperty(
        name="Value",
        description="float value",
        default=0.0,
    )


class ScinodeSocketInt(ScinodeSocket):
    bl_idname = 'ScinodeSocketInt'
    bl_label = "Scinode Socket Integer"

    default_value: bpy.props.IntProperty(
        name="Value",
        description="Integer value",
        default=0,
    )


class ScinodeSocketString(ScinodeSocket):
    bl_idname = 'ScinodeSocketString'
    bl_label = "Scinode Socket String"

    default_value: bpy.props.StringProperty(
        name="Value",
        description="Integer value",
        default="",
    )


class ScinodeSocketBool(ScinodeSocket):
    bl_idname = 'ScinodeSocketBool'
    bl_label = "Scinode Socket Bool"

    default_value: bpy.props.BoolProperty(
        name="Value",
        description="Integer value",
        default=False,
    )



class ScinodeSocketFloatVector3D(ScinodeSocket):
    bl_idname = 'ScinodeSocketFloatVector3D'
    bl_label = "Scinode Socket Vector"

    default_value: bpy.props.FloatVectorProperty(
        name="Value",
        description="Float Vector value",
        size=3,
        default=[0, 0, 0],
    )

    def get_default_value(self):
        return np.array(self.default_value)

class ScinodeSocketIntVector3D(ScinodeSocket):
    bl_idname = 'ScinodeSocketIntVector3D'
    bl_label = "Scinode Socket Vector"

    default_value: bpy.props.IntVectorProperty(
        name="Value",
        description="Int Vector value",
        size=3,
        default=[0, 0, 0],
    )

    def get_default_value(self):
        return np.array(self.default_value)


class ScinodeSocketFloatMatrix3D(ScinodeSocket):
    bl_idname = 'ScinodeSocketFloatMatrix3D'
    bl_label = "Scinode Socket Matrix"

    i: bpy.props.FloatVectorProperty(
        name="Value",
        description="Float Vector value",
        size=3,
        default=[0, 0, 0],
    )
    j: bpy.props.FloatVectorProperty(
        name="Value",
        description="Float Vector value",
        size=3,
        default=[0, 0, 0],
    )
    k: bpy.props.FloatVectorProperty(
        name="Value",
        description="Float Vector value",
        size=3,
        default=[0, 0, 0],
    )

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            col = layout.column()
            col.label(text=text)
            row = col.row()
            row.prop(self, "i", text="")
            row = col.row()
            row.prop(self, "j", text="")
            row = col.row()
            row.prop(self, "k", text="")

    def draw_color(self, context, node):
        return (1, 0.4, 1, 0.5)

    def get_default_value(self):
        return np.array([self.i, self.j, self.k])

    def set_default_value(self, value):
        self.i = value[0]
        self.j = value[1]
        self.k = value[2]
