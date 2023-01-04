.. _advance_control_node:

===========================================
Control nodes
===========================================
An ordinary node runs independently, and thus will not affect other nodes. However, some special nodes, called control nodes, will interfere with other nodes. One can think of them as the flow control statements known from Python languages, e.g. ``for``, ``if``, ``break``.

We can use these nodes for a more complicated workflow.



Switch
------------
Run the nodes after Switch node if the input ``Switch`` socket is ``True``, otherwise does not execute the following nodes.


Update
----------
Update node will update the input socket and run the workflow again.


Scatter
--------------
In the following schematic, the ``Result`` socket of node 1 has a list of values: [a, b, c]. We want to run node 2 and the following nodes with input ``a``, ``b`` and ``c`` separately.


The scatter node will generate a series of sub-nodetree. And the input of the first node will be the result at the index.
