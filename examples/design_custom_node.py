
import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode


class SumDifference(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'SumDifference'
    bl_label = "SumDifference"

    def init(self, context):
        # Here we define the inputs and ouputs sockets.
        self.inputs.new("ScinodeSocketFloat", "input1")
        self.inputs.new("ScinodeSocketFloat", "input2")
        self.outputs.new("ScinodeSocketGeneral", "Result")

    def get_executor(self):
        # where can we import the execute node.
        return {"path": "mypackage.my_sum_difference",
                "name": "SumDifference",}

from nodeitems_utils import NodeItem
from scinode_editor.node_catagory import ScinodeCategory
node_categories = [
    # identifier, label, items list
    ScinodeCategory('Mynodes', "My Nodes", items=[
        NodeItem("SumDifference", label="SumDifference", settings={}),
    ]),
]

def register_class():
    from bpy.utils import register_class
    import nodeitems_utils
    register_class(SumDifference)
    nodeitems_utils.register_node_categories('MyNodeTree', node_categories)

def unregister_class():
    from bpy.utils import unregister_class
    from bpy.utils import unregister_class
    unregister_class(SumDifference)
    nodeitems_utils.unregister_node_categories('MyNodeTree')

if __name__ == "__main__":
    register_class()
