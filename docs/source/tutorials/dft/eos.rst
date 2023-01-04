.. _eos:

Equation of state (EOS)
===========================

Calculate the equation of state for bulk FCC Al.


.. image:: /_static/images/eos.png
   :width: 20cm

Here is the python code:

.. code-block:: python

    bpy.ops.batoms.delete()
    nt = bpy.data.node_groups.new(name='test_qe_eos', type='ScinodeTree')
    # add a FCC Al structure
    bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
    structure = nt.nodes.new(type='Batoms')
    structure.batoms = 'Al'
    # add PW node and set its work directory
    pw = nt.nodes.new(type='QEPW')
    pw.directory = 'scinode/al'
    # scale cell
    # numpy.linspace node to set five scale for lattice constants
    linspace1 = nt.nodes.new(type='Numpy')
    linspace1.inputs['start'].default_value = 0.98
    linspace1.inputs['stop'].default_value = 1.02
    linspace1.inputs['num'].default_value = 5
    # get and set cell
    getattr1 = nt.nodes.new(type='Getattr')
    getattr1.inputs["Name"].default_value = "cell"
    setattr1 = nt.nodes.new(type='Setattr')
    setattr1.inputs["Name"].default_value = "cell"
    mul1 = nt.nodes.new(type='Numpy')
    mul1.function = "multiply"
    scatter1 = nt.nodes.new(type='Scatter')
    # Add parameters, pseudo and kpoints nodes
    parameter = nt.nodes.new(type='QEPWParameter')
    pseudo = nt.nodes.new(type='QEPseudo_SSSP')
    kpoint = nt.nodes.new(type='DFTKpoints')
    kpoint.size = [5, 5, 5]
    eos = nt.nodes.new(type='ASEEOS')
    debug = nt.nodes.new(type='Print')
    nt.links.new(structure.outputs[0], getattr1.inputs[0])
    nt.links.new(getattr1.outputs['Result'], mul1.inputs[0])
    nt.links.new(linspace1.outputs[0], scatter1.inputs[0])
    nt.links.new(scatter1.outputs[0], mul1.inputs[1])
    nt.links.new(structure.outputs[0], setattr1.inputs[0])
    nt.links.new(mul1.outputs['Result'], setattr1.inputs['Value'])
    nt.links.new(setattr1.outputs[0], pw.inputs['Structure'])
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoints'], pw.inputs['Kpoints'])
    nt.links.new(pw.outputs['Structure'], scatter1.inputs[1])
    nt.links.new(pw.outputs['Structure'], eos.inputs['Structures'])
    nt.links.new(pw.outputs['Energy'], eos.inputs['Energies'])
    nt.links.new(eos.outputs['B'], debug.inputs['Input'])
    nt.launch()
