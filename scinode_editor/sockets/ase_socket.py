import bpy
from bpy.types import (
    NodeSocket,
)
from scinode_editor.sockets.general_socket import ScinodeSocket
from scinode_ase.serialization.atoms import SerializeAtoms

class ScinodeSocketAtoms(ScinodeSocket, SerializeAtoms):
    '''Scinode socket Atoms type'''
    bl_idname = 'ASEAtoms'
    bl_label = "Scinode Socket Calculator"

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 1, 0.5)

    def get_default_value(self):
        """Get default value."""
        from ase.atoms import Atoms
        return Atoms()

    def set_default_value(self, value):
        """Set default value."""
        pass


class ScinodeSocketCalculator(NodeSocket):
    '''Scinode socket calculator type'''
    bl_idname = 'ScinodeSocketCalculator'
    bl_label = "Scinode Socket Calculator"

    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 1, 0.5)


class ScinodeSocketStructure(NodeSocket):
    '''Scinode socket structure type'''
    bl_idname = 'ScinodeSocketStructure'
    bl_label = "Scinode Socket Structure"

    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 1, 0.5)


class ScinodeSocketKpoint(NodeSocket):
    '''Scinode socket kpoint type'''
    bl_idname = 'ScinodeSocketKpoint'
    bl_label = "Scinode Socket Kpoint"


    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.4, 1, 0.5)


class ScinodeSocketCommand(NodeSocket):
    '''Scinode socket command type'''
    bl_idname = 'ScinodeSocketCommand'
    bl_label = "Scinode Socket Command"

    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (1.0, 0.4, 0.4, 0.5)


class ScinodeSocketPseudo(NodeSocket):
    '''Scinode socket pseudo type'''
    bl_idname = 'ScinodeSocketPseudo'
    bl_label = "Scinode Socket Pseudo"


    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 1, 0.4, 0.5)


class ScinodeSocketParameter(NodeSocket):
    '''Scinode socket parameter type'''
    bl_idname = 'ScinodeSocketParameter'
    bl_label = "Scinode Socket Parameter"

    default_value: bpy.props.StringProperty(
        name="Value",
        description="string value",
        default='',
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 1, 0.5)


class ScinodeSocketEnergy(NodeSocket):
    '''Scinode socket energy type'''
    bl_idname = 'ScinodeSocketEnergy'
    bl_label = "Scinode Socket Energy"

    default_value: bpy.props.FloatProperty(
        name="Value",
        description="Float value",
        default=0.0,
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 1, 0.5)


class ScinodeSocketForce(NodeSocket):
    '''Scinode socket force type'''
    bl_idname = 'ScinodeSocketForce'
    bl_label = "Scinode Socket Force"

    default_value: bpy.props.FloatProperty(
        name="Value",
        description="Float value",
        default=0.0,
    )

    argument_type = 'kwargs'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 1, 0.5)


class ScinodeSocketDos(NodeSocket):
    '''Scinode socket dos type'''
    bl_idname = 'ScinodeSocketDos'
    bl_label = "Scinode Socket Dos"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 1, 0.5)


class ScinodeSocketBand(NodeSocket):
    '''Scinode socket Band type'''
    bl_idname = 'ScinodeSocketBand'
    bl_label = "Scinode Socket Band"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 1, 0.5)
