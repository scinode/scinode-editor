import bpy
import time
import numpy as np


def test_batoms():
    bpy.ops.batoms.molecule_add(label="h2o", formula="H2O")
    nt = bpy.data.node_groups.new(name='test_batoms', type='ScinodeTree')
    btoms1 = nt.nodes.new(type='Batoms')
    btoms1.batoms = "h2o"
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = btoms1.get_results()
    atoms = results[0]["value"]
    print("atoms: {atoms}")
    assert len(atoms) == 3

def test_batoms_viewer():
    bpy.ops.batoms.molecule_add(label="h2o", formula="H2O")
    nt = bpy.data.node_groups.new(name='test_batoms_viewer', type='ScinodeTree')
    btoms1 = nt.nodes.new(type='Batoms')
    viewer1 = nt.nodes.new(type='ViewBatoms')
    btoms1.batoms = "h2o"
    nt.links.new(btoms1.outputs[0], viewer1.inputs[0])
    nt.launch()
    time.sleep(5)
    nt.update_state()


def test_replace():
    """A nodetree for bulk."""
    bpy.ops.batoms.molecule_add(label="h2o", formula="H2O")
    nt = bpy.data.node_groups.new(name='test_batoms_replace', type='ScinodeTree')
    btoms1 = nt.nodes.new(type='Batoms')
    btoms1.batoms = "h2o"
    #
    replace1 = nt.nodes.new("ASEReplaceAtoms")
    replace1.inputs["Index"].default_value = 1
    replace1.inputs["Value"].default_value = "C"
    nt.links.new(btoms1.outputs[0], replace1.inputs[0])
    #
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = replace1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert atoms1[1].symbol == "C"
