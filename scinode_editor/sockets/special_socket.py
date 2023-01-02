import bpy
from bpy.types import NodeSocket


class ScinodeSocketJoin(NodeSocket):
    '''Scinode socket Join type'''
    bl_idname = 'ScinodeSocketJoin'
    bl_label = "Scinode Socket Join"

    default_value: bpy.props.BoolProperty(
        name="Value",
        description="float value",
        default=False,
    )

    argument_type = 'kwargs'

    # is_multi_input = True

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.4, 0.4, 1, 0.5)
