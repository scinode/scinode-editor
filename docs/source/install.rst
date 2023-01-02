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






Install SciNode inside Blender
===============================

On Linux and MacOS, go to your Blender python directory, e.g. ``blender-3.1.0-linux-x64/3.1/python/bin``, install pip_::

    $ ./python3.10 -m ensurepip
    $ ./python3.10 -m pip install --upgrade pip

Install SciNode_ inside Blender::

    $ ./pip3 install --upgrade scinode


Install Scinode-Editor inside Blender
===============================

- Download the latest version (`beautiful-nodes.zip <https://github.com/beautiful-atoms/beautiful-nodes/archive/refs/heads/main.zip>`__).

- Extract the file, move the folder ``scinode_editor`` to Blender addons folder ``$HOME/.config/blender/3.1/scripts/addons/``.

- Enable the addon in the Preferences setting. Please open a Blender Python console, and run the following code to enable the scinode-editor::

    import addon_utils
    import bpy
    addon_utils.enable('scinode-editor', default_set=True)
    bpy.context.preferences.view.use_translate_new_dataname = False
    bpy.ops.wm.save_userpref()

.. note::
    Or, you can visit here to learn how to enable an addon by hand. https://docs.blender.org/manual/en/latest/editors/preferences/addons.html.



.. _Blender: https://www.blender.org/
.. _SciNode: https://scinode.readthedocs.io/en/latest/index.html
.. _pip: https://pypi.org/project/pip/
