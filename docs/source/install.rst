.. _download_and_install:

===========================================
Installation
===========================================


Requirements
============

* Blender_ 3.0 or newer, please install Blender first.
* SciNode_



Install and configure SciNode
===========================================
First, install SciNode on your computer. Please visit: https://scinode.readthedocs.io/en/latest/install.html

If you want to use Quantum Espresso,

.. code-block:: console

    pip install scinode-ase




Install Scinode-Editor inside Blender
=======================================

- Download the latest version (`scinode-editor.zip <https://github.com/scinode/scinode-editor/archive/refs/heads/main.zip>`__).

- Extract the file, and move the folder ``scinode_editor`` to Blender addons folder ``$HOME/.config/blender/3.1/scripts/addons/``.

- Enable the addon in the Preferences setting. Please open a Blender Python console, and run the following code to enable the scinode-editor::

    import addon_utils
    import bpy
    addon_utils.enable('Scinode Editor', default_set=True)
    bpy.context.preferences.view.use_translate_new_dataname = False
    bpy.ops.wm.save_userpref()

.. note::
    Or, you can visit here to learn how to enable an addon by hand. https://docs.blender.org/manual/en/latest/editors/preferences/addons.html.



.. _Blender: https://www.blender.org/
.. _SciNode: https://scinode.readthedocs.io/en/latest/index.html
.. _pip: https://pypi.org/project/pip/
