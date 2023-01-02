.. _advance_socket:

===========================================
Socket
===========================================

Link limit
===================

For output socket, there is no limit on the number of links connected with them. In the following schematic, node 1 has two output links for the ``Result`` socket.


.. image:: /_static/images/scinode-output-sockets.png
   :width: 10cm

For inputs sockets, there is a link_limit. The default ``link_limit`` = 1, which means the input socket can only have one input link. This is how we define a function, whose arguments should be unique.


However, if you want to create a input socket allowing more than one link, you can set ``link_limit`` to a large number when creating the socket.

.. code:: python

   def init(self, context):
        socket = self.inputs.new("BnodesSocketGeneral", "Input")
         # Set the link_limit to 100 for "Input" socket
        socket.link_limit = 100
        self.outputs.new("BnodesSocketGeneral", "Result")


In the following schematic, node 3 has two output links for the ``Input`` socket. In this case, you have to tell the node how to handle multiple input links. One possible solution is to merge the inputs as one.



.. image:: /_static/images/scinode-input-sockets.png
   :width: 10cm


Dynamic sockets
===================

Add a callback function (here is ``update_sockets``) when update a property.


.. code:: python

   import bpy
   from bnodes.node.base_node import BnodesTreeNode, update_sockets


   class BnodesDebugMath(bpy.types.Node, BnodesTreeNode):
      bl_idname = 'BnodesDebugMath'
      bl_label = "Math Node"
      bl_icon = "VIEW_ORTHO"

      # we add update_sockets callback for "function" property.
      function: bpy.props.EnumProperty(
         name="function",
         description="function.",
         items=(
               ('add', "add", "add", 0),
               ('minus', "minus", "minus", 1),
               ('multiply_add', "multiply_add", "multiply_add", 2),
         ),
         default='add',
         update=update_sockets,
      )

      x: bpy.props.FloatProperty(name="x", default=0.0)

      properties = ["x", "function"]

      def init(self, context):
         if self.function == 'multiply_add':
               self.inputs.new("BnodesSocketFloat", "y")
               self.inputs.new("BnodesSocketFloat", "z")
         else:
               self.inputs.new("BnodesSocketFloat", "y")
         self.outputs.new("BnodesSocketFloat", "Result")

      def draw_buttons(self, context, layout):
         layout.prop(self, "function", text="")
         layout.prop(self, "x", text="")

      def get_executor(self):
         return {"path": "scinode.executors.debug.math",
                  "name": self.function,
                  "type": "function",
                  "has_run": True,
                  }
