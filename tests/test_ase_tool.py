import bpy
import time
import numpy as np

def test_adsorption():
    """
    """
    nt = bpy.data.node_groups.new(name='test_adsorption', type='ScinodeTree')
    # add Pt fcc111 surface
    surf1 = nt.nodes.new(type='ASESurface')
    surf1.function = "fcc111"
    surf1.inputs["symbol"].default_value = "Pt"
    surf1.inputs["size"].default_value = [1, 1, 4]
    surf1.inputs["vacuum"].default_value = 5.0
    # add H2O molecule
    mol1 = nt.nodes.new(type='ASEMolecule')
    mol1.inputs["formula"].default_value = "H2O"
    # add adsorption node
    ads1 = nt.nodes.new(type='ASEAdsorption')
    ads1.inputs["Attach_atom"].default_value = 1
    ads1.inputs["Index"].default_value = 3
    debug = nt.nodes.new(type='Print')
    nt.links.new(surf1.outputs[0], ads1.inputs[0])
    nt.links.new(mol1.outputs[0], ads1.inputs[1])
    nt.links.new(ads1.outputs[0], debug.inputs[0])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    atoms = ads1.get_results()[0]["value"]
    print(atoms.positions)
    assert len(atoms) == 7
    assert np.isclose(atoms[-1].z, 15.036)
