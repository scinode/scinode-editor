.. _first_nodetree:

===========================================
Build your first node-based workflow
===========================================

Here is a video tutorial: https://youtu.be/I7AgGz0WkhY

New nodetree
===================
#. Open Blender, and go to ``Scinode`` Editor.
#. Create a new Nodetree, and change it name to ``my_first_nodetree``


Add node
===================
#. Add two ``Float`` nodes, a ``Numpy`` node, and a ``Debug`` node.
#. Set the value of Float nodes to be 2 and 3 respectively.
#. Set the `function` in ``Numpy`` node to be `add`.


Connect your ndoes
====================
#. Connect the output socket of ``Float`` nodes to the input sockes of ``Numpy`` node.
#. Connect the output socket of ``Numpy`` nodes to the input sockes of ``Debug`` node.



Launch nodetree
===================

#. Now we can submit the nodetree by clicking ``Launch`` button.
#. Wait few seconds, and click "update_state" button.

One should see the following output of ``Numpy`` node on the ``Debug`` node.



Check nodetree status
===========================================

Open a terminal, one can show all nodetree by:

.. code-block:: console

    $ xnodes nodetree show
       index               name     state action daemon_name
    0      1  my_first_nodetree  FINISHED   NONE   localhost

Since this a simple calculation, you will see that the job is finished.

One can show the detail of the nodetree by adding the ``index`` option:

.. code-block:: console

    $ xnodes nodetree show --index 1

One can show the detail of a ``Node`` by:

.. code-block:: console

    $ xnodes node show --index 1

One can check the ``error`` key, if node failed.
