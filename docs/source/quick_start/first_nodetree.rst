.. _first_nodetree:

===========================================
Build your first node-based workflow
===========================================

Here is a video tutorial: https://youtu.be/I7AgGz0WkhY

New nodetree
===================
- Open Blender, and go to ``Scinode`` Editor.
- Create a new Nodetree, and change its name to ``my_first_nodetree``


Add nodes
===================
- Go to ``Test`` catalog, add two ``Float`` nodes, and a ``Add`` node.
- Go to ``Utils`` catalog, add a ``Print`` node.
- Set the value of Float nodes to 2 and 3 respectively.


Connect nodes
====================
- Connect the output socket of ``Float`` nodes to the input sockes of ``Add`` node.
- Connect the output socket of ``Add`` nodes to the input sockes of ``Print`` node.



Launch nodetree
===================

- Enable "auto_update_state" by clicking it.
- Now we can submit the nodetree by clicking ``Launch`` button.
- One will see the color of the node change one by one.
- Green color mean the node is finished.
- When the ``Add`` node finished, the result will be shown on the ``Print`` node.
