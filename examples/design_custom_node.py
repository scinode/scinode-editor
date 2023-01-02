
import bpy
from bnodes.node.base_node import BnodesTreeNode


class BnodesSumDifference(bpy.types.Node, BnodesTreeNode):
    bl_idname = 'BnodesSumDifference'
    bl_label = "SumDifference"

    def init(self, context):
        # Here we define the inputs and ouputs sockets.
        self.inputs.new("BnodesSocketFloat", "input1")
        self.inputs.new("BnodesSocketFloat", "input2")
        self.outputs.new("BnodesSocketGeneral", "Result")

    def get_executor(self):
        # where can we import the execute node.
        return {"path": "mypackage.my_sum_difference",
                "name": "SumDifference",}

from nodeitems_utils import NodeCategory, NodeItem
from bnodes.node_catagory import BnodesCategory
node_categories = [
    # identifier, label, items list
    BnodesCategory('Mynodes', "My Nodes", items=[
        NodeItem("BnodesSumDifference", label="SumDifference", settings={}),
    ]),
]

def register_class():
    from bpy.utils import register_class
    import nodeitems_utils
    register_class(BnodesSumDifference)
    nodeitems_utils.register_node_categories('MyNodeTree', node_categories)

def unregister_class():
    from bpy.utils import unregister_class
    from bpy.utils import unregister_class
    unregister_class(BnodesSumDifference)
    nodeitems_utils.unregister_node_categories('MyNodeTree')

if __name__ == "__main__":
    register_class()
