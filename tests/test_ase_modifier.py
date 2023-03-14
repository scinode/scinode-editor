import bpy
import time
import numpy as np


def test_cell_transform():
    """A nodetree for bulk."""
    nt = bpy.data.node_groups.new(name='test_cell_transform', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    #
    t1 = nt.nodes.new("ASECellTransformatoin")
    t1.inputs["P"].i =  [2, 0, 0]
    t1.inputs["P"].j =  [0, 2, 0]
    t1.inputs["P"].k =  [0, 0, 2]
    nt.links.new(bulk1.outputs[0], t1.inputs[0])
    #
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = t1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert np.isclose(atoms1.cell[0][0], 8.1)
    assert len(atoms1) == 32
    #
    t1.inputs["P"].i =  [2, 0, 0]
    t1.inputs["P"].j =  [0, 1, 0]
    t1.inputs["P"].k =  [0, 0, 1]
    nt.save_to_db()
    time.sleep(5)
    nt.update_state()
    assert t1.state == "CREATED"


def test_replace():
    """A nodetree for bulk."""
    nt = bpy.data.node_groups.new(name='test_replace', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    #
    replace1 = nt.nodes.new("ASEReplaceAtoms")
    replace1.inputs["Index"].default_value = 1
    replace1.inputs["Value"].default_value = "Pt"
    nt.links.new(bulk1.outputs[0], replace1.inputs[0])
    #
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = replace1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert atoms1[1].symbol == "Pt"
    # replace a list of atoms
    nt.reset()
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  4
    arange1.inputs["step"].default_value =  2
    nt.links.new(arange1.outputs[0], replace1.inputs[1])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = replace1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert atoms1[1].symbol == "Pt"
    assert atoms1[3].symbol == "Pt"


def test_delete():
    """A nodetree for bulk."""
    nt = bpy.data.node_groups.new(name='test_delete', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    #
    del1 = nt.nodes.new("ASEDeleteAtoms")
    del1.inputs["Index"].default_value = 1
    nt.links.new(bulk1.outputs[0], del1.inputs[0])
    #
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = del1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert len(atoms1) == 3
