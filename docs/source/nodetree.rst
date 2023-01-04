.. _nodetree:

.. module:: nodetree


===========================================
Nodetree
===========================================
The :class:`~scinode_editor.node_tree.ScinodeTree` object is a collection of nodes and links.

.. figure:: /_static/images/scinode-example.png
   :width: 10cm


Create and launch nodetree
============================
- Create a nodetree:

.. code-block:: python

    nt = bpy.data.node_groups.new(name='my_first_nodetree', type='ScinodeTree')

- Add nodes:

.. code-block:: python

    float1 = nt.nodes.new("TestFloat")
    add1 = nt.nodes.new("TestAdd")

- Add link between nodes:

.. code-block:: python

    nt.links.new(float1.outputs[0], add1.inputs[0])

- Launch the nodetree:

.. code-block:: python

    nt.launch()


Execute order
===============
The nodes will be executed when:

- No input node
- All input nodes finish.

.. figure:: /_static/images/nodetree-execute.gif
   :width: 20cm

Working mode
===============
SciNode supports the following working modes:


- Normal launch.
- Reset, and launch a new workflow.
- Add new nodes, and continue the workflow.
- Add new nodes, and start a new workflow.
- modify nodes, and restart workflow after the node
- modify nodes, and start a new workflow
- pause the node and the following nodes, when a job fails.
- modify the failed node, continue the workflow
- pause the node manually, and play it again.


Reset node
------------
Resetting a node will also reset all its child nodes.

.. figure:: /_static/images/nodetree-reset.gif
   :width: 20cm

Add new nodes
--------------
Add new nodes, and continue the workflow:

.. figure:: /_static/images/nodetree-add-continue.gif
   :width: 20cm

The above modes can be achieved by the Python script, the GUI, or the command line.

List of all Methods
====================

.. autoclass:: scinode_editor.node_tree.ScinodeTree
   :members:
