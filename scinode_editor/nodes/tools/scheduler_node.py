

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class BnodesScheduler(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'BnodesScheduler'
    bl_label = "Scheduler"


    system: bpy.props.EnumProperty(
        name="system",
        items=[
                ('SLURM', 'SLURM', '', 0),
                ('PBS', 'PBS', '', 0)
            ],
        description="",
        default=0,
    )

    time: bpy.props.StringProperty(name="time", default="23:59:59")
    partition: bpy.props.StringProperty(name="partition", default="")
    qos: bpy.props.StringProperty(name="qos", default="")
    nodes: bpy.props.IntProperty(name="nodes", default=1)
    ntasks_per_node: bpy.props.IntProperty(name="ntasks_per_node", default=20)
    config: bpy.props.StringProperty(name="config", default="")

    properties = {
        'system': 'kwargs',
        'time': 'kwargs',
        'nodes': 'kwargs',
        'ntasks_per_node': 'kwargs',
        'partition': 'kwargs',
        'qos': 'kwargs',
        'config': 'kwargs',
    }

    def init(self, context):
        self.outputs.new("ScinodeSocketGeneral", "Scheduler")

    def draw_buttons(self, context, layout):
        if getattr(self, 'system') == 'SLURM':
            layout.prop(self, "time", text="time")
            layout.prop(self, "partition", text="partition")
            layout.prop(self, "qos", text="qos")
            layout.prop(self, "config", text="config")
            layout.prop(self, "nodes", text="Nodes")
            layout.prop(self, "ntasks_per_node", text="ntasks_per_node")

    def get_executor(self):
        return {"path": "xnodes.executors.tools.scheduler_node",
                "name": "Scheduler",
                "has_run": True,
                }
