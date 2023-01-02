
==================
Design your Node
==================

These tutorials expect you to have a basic knowledge in Python. It will consist of multiple parts. Each part will go a bit more into detail so that you will be able to write more complex nodes in the end.


In the previous example, we used the built-in nodes ``float`` and ``numpy``. In this example, we will create a custom node, thus, we can reuse the node later.

In order to create a new node, we need to do the following steps:

1. UI node file: This file defines how the node looks like in the Node Editor, e.g. Name of the node; How many input sockets and outputs sockets.
2. Register the node into a catagory
3. Register the classes into Blender
4. Create a executor file: This file defines a function the node will execute.


Here, we want to build a ``MySumDifference`` node, which will calculate the sum and the difference between two number. The node has two inputs ``input1`` and ``input2``. It will return two results: ``sum`` and the ``difference``. Here is the schematic of the node:

.. image:: /_static/images/sum_difference_node.png
   :width: 5cm

Here is a video tutorial: https://youtu.be/6ibDfMeabas

Step 1: Add UI Node
=====================

First create a UI node file (``my_sum_difference.py``).

.. code:: Python

    import bpy
    from bnodes.nodes.base_node import BnodesTreeNode

    class BnodesSumDifference(bpy.types.Node, BnodesTreeNode):
        bl_idname = 'BnodesSumDifference'
        bl_label = "SumDifference"

        def init(self, context):
            # Here we define the inputs and ouputs sockets.
            self.inputs.new("BnodesSocketFloat", "input1")
            self.inputs.new("BnodesSocketFloat", "input2")
            self.outputs.new("BnodesSocketGeneral", "Sum")
            self.outputs.new("BnodesSocketGeneral", "Difference")
            #
            self.kwargs = "input1, input2"


        def get_executor(self):
            # where can we import the execute node.
            return {"path": "mypackage.my_sum_difference",
                    "name": "sum_difference"}



Step 2: Add Node Catagory
==============================

.. code:: Python

    from nodeitems_utils import NodeCategory, NodeItem
    from bnodes.node_catagory import BnodesCategory
    node_categories = [
        # identifier, label, items list
        BnodesCategory('Mynodes', "My Nodes", items=[
            NodeItem("BnodesSumDifference", label="SumDifference", settings={}),
        ]),
    ]


Step 3: Register Classes and Catagory
========================================

.. code:: Python

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


Copy the above code into Blender's text Editor, and run. Then in the ``Bnodes`` Editor, you can find a new Catagory for the new node.

.. image:: /_static/images/bnodes_custom_node_1.png
   :width: 10cm


Step 4: Add executor node
================================

Now let's build a custom executor (function) ``SumDifference`` for our node. Let's create a file called ``sum_difference.py``, and the following code into it.

.. code:: Python

        def sum_difference(input1=0, input2=0):
            """This is the main function to execute the node.
            """
            import numpy as np
            sum = input1 + input2
            difference = input1 - input2
            return sum, difference

It is important that we add this executor to a python package (or into a Python path), thus we could import it in our node. We can create own Python package, e.g. ``mynode``. Add the above executor file into this package, e.g. add into ``mynode.executors.sum_difference``.
