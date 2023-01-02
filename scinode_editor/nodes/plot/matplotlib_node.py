

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode, update_sockets


func_items = [
    ("plot", "plot", "", 0),
    ("bar", "bar", "", 1),
]

color_items = [
    ("red", "red", "", 1),
    ("green", "green", "", 1),
    ("blue", "blue", "", 0),
]


linestyle_items = [
    ("solid", "solid", "", 0),
    ("dashed", "dashed", "", 1),
]

marker_items = [
    ("None", "None", "", 0),
    ("o", "o", "", 1),
    ("s", "s", "", 2),
]


class MatplotlibPyplot(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'MatplotlibPyplot'
    bl_label = "Pyplot"

    function: bpy.props.EnumProperty(
        name="function",
        description="function.",
        items=func_items,
        default='plot',
        update=update_sockets,
    )

    color: bpy.props.EnumProperty(
        name="color",
        description="color.",
        items=color_items,
        default='blue',
    )

    linestyle: bpy.props.EnumProperty(
        name="linestyle",
        description="linestyle.",
        items=linestyle_items,
        default='solid',
    )

    marker: bpy.props.EnumProperty(
        name="marker",
        description="marker.",
        items=marker_items,
        default='None',
    )

    properties = {
        "color": "kwargs",
        "linestyle": "kwargs",
        "marker": "kwargs",
    }

    def init(self, context):
        if self.function in ['plot', 'bar']:
            self.inputs.new("ScinodeSocketFloatArgs", "x")
            self.inputs.new("ScinodeSocketFloatArgs", "y")
        else:
            self.inputs.new("ScinodeSocketFloatArgs", "x")
        self.outputs.new("ScinodeSocketFloatArgs", "Result")

    def draw_buttons(self, context, layout):
        layout.prop(self, "function", text="")
        layout.prop(self, "color", text="color")
        layout.prop(self, "linestyle", text="style")
        layout.prop(self, "marker", text="marker")

    def get_executor(self):
        return {"path": "matplotlib.pyplot",
                "name": self.function,
                "type": "function",
                "has_run": False,
                }

    def update_state(self):
        """Update the debug text.
        """
        import importlib
        from xnodes.utils.node import inspect_executor_arguments
        import matplotlib.pyplot as plt
        parameters = self.get_input_parameters_from_db()
        if parameters is None:
            return
        args, kwargs = inspect_executor_arguments(parameters)
        data = self.get_executor()
        module = importlib.import_module("{}".format(data['path']))
        Ececutor = getattr(module, data['name'])
        print("  Ececutor: ", Ececutor)
        print("  args, kwargs ", args, kwargs)
        kwargs.update({"linestyle": self.linestyle,
                       "color": self.color})
        if self.marker != 'None':
            kwargs['marker'] = self.marker
        if data['has_run']:
            Ececutor = Ececutor(*args, **kwargs, dbdata=self.dbdata)
            Ececutor.run()
        else:
            Ececutor(*args, **kwargs)
        plt.show()
