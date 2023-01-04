.. _qe:

===================
Quantum Espresso
===================
Quantum ESPRESSO (QE) is an Open-Source package for electronic-structure calculations and materials modeling. It is based on density-functional theory, plane waves, and pseudopotentials.


PW
----------
Perform a regular pw calculation:

.. image:: /_static/images/qe-pw.png
   :width: 10cm

Here is the python code:

.. code-block:: python

   nt = bpy.data.node_groups.new(name='test_pw', type='ScinodeTree')
   # build a structure
   bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
   structure = nt.nodes.new(type='Batoms')
   structure.batoms = 'Al'
   # Add PW node, set its work directory
   pw = nt.nodes.new(type='QEPW')
   pw.Directory = 'scinode/al'
   # Add parameters, pseudo and kpoints nodes
   parameter = nt.nodes.new(type='QEPWParameter')
   pseudo = nt.nodes.new(type='QEPseudo_SSSP')
   kpoint = nt.nodes.new(type='DFTKpoints')
   kpoint.size = [5, 5, 5]
   debug = nt.nodes.new(type='Print')
   # link all sockets
   nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
   nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
   nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
   nt.links.new(kpoint.outputs['Kpoints'], pw.inputs['Kpoints'])
   nt.links.new(pw.outputs['Energy'], debug.inputs['Input'])
   #
   nt.launch()

Get the results:

.. code-block:: python

   results = pw.get_results()
   energy = results[1]['value']

DOS and PDOS
------------------------------------

.. image:: /_static/images/qe-pw-dos-pdos.png
   :width: 15cm


Here is the python code:

.. code-block:: python

   nt = bpy.data.node_groups.new(name='test_dos_pdos', type='ScinodeTree')
   # build a structure
   bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
   structure = nt.nodes.new(type='Batoms')
   structure.batoms = 'Al'
   # Add PW node, set its work directory
   pw = nt.nodes.new(type='QEPW')
   pw.Directory = 'scinode/al'
   # Add parameters, pseudo and kpoints nodes
   parameter = nt.nodes.new(type='QEPWParameter')
   pseudo = nt.nodes.new(type='QEPseudo_SSSP')
   kpoint = nt.nodes.new(type='DFTKpoints')
   kpoint.size = [5, 5, 5]
   # Add dos and dos parameters nodes
   dos = nt.nodes.new(type='QEDos')
   dosparameter = nt.nodes.new(type='QEDosParameter')
   # Add projwfc and projwfc parameters nodes
   projwfc = nt.nodes.new(type='QEProjwfc')
   projwfcparameter = nt.nodes.new(type='QEProjwfcParameter')
   #
   debug1 = nt.nodes.new(type='Print')
   debug2 = nt.nodes.new(type='Print')
   nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
   nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
   nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
   nt.links.new(kpoint.outputs['Kpoints'], pw.inputs['Kpoints'])
   nt.links.new(pw.outputs['Calculator'], dos.inputs['Calculator'])
   nt.links.new(dosparameter.outputs[0], dos.inputs['Parameter'])
   nt.links.new(pw.outputs['Calculator'], projwfc.inputs['Calculator'])
   nt.links.new(projwfcparameter.outputs[0], projwfc.inputs['Parameter'])
   nt.links.new(dos.outputs['Energies'], debug1.inputs['Input'])
   nt.links.new(projwfc.outputs['Energies'], debug2.inputs['Input'])
   nt.launch()
