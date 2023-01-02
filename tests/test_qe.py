import bpy
import time
import numpy as np

def test_pw():
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
    nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoints'], pw.inputs['Kpoints'])
    nt.links.new(pw.outputs['Energy'], debug.inputs['Input'])
    nt.launch()
    time.sleep(20)
    results = pw.get_results()
    energy = results[1]['value']
    assert np.isclose(energy, -537.4240030303778)


def test_dos_pdos():
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
    time.sleep(20)
    results = dos.get_results()
    print(results)
    energy = results[0]['value']
    assert np.isclose(energy[0], -18.1588)


def test_qe_eos():
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
    time.sleep(60)
    results = eos.get_results()
    B = results[2]['value']
    assert np.isclose(B, 76.97911565936764)
