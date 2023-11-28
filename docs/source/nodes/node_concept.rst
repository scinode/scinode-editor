.. _node_concept:

===========================================
Node
===========================================


.. figure:: /_static/images/node.png
   :width: 10cm
   :align: right

Here we only introduce the general features of `Node`.

A node can have the following features:

- metadata, e.g. name, state, type
- properties (optional)
- input sockets (optional)
- output sockets (optional)
- executor: a function (class) to process node data.
- belong to a `Nodetree`


Metadata
====================
- `identifier`: identifier of this node class.
- `name`: name of this node.

.. code-block:: python

   # inditifier: TestFloat
   node1 = nt.nodes.new("TestFloat")
   node1.name = "float1"

- State
   A node can has following states:
   ``CREATED``, ``RUNNING``, ``FINISHED``, ``FAILED``, ``CANCELLED``, ``PAUSED``, ``WAITING``, ``SKIPPED``, ``UNKNOWN``.

- Action
   Actions applied to a node:
   ``NONE``,  ``LAUNCH``,  ``WAIT_RESULT``,  ``PAUSE``,  ``PLAY``,  ``GATHER``,  ``CANCEL``,  ``SKIP``.

Executor
===========================================
Finally, the main entry point is the executor. An executor is a Python class/function for processing node data. It uses the node properties, inputs, outputs and context information as arguments (positional and keyword).

- function
- class

Classification
==================
According to the state of the node:

- Normal
- Control (Scatter, Update, Switch)
- Reference
- Copy

According to the execution:

- Passive
- Active. An active node has a control loop that runs in its own process or thread.



List of all Methods
===================

.. autoclass:: scinode_editor.nodes.base_node.ScinodeTreeNode
   :members:
