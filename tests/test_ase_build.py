import bpy
import time
import numpy as np


def test_atoms():
    nt = bpy.data.node_groups.new(name='test_atoms', type='ScinodeTree')
    atoms1 = nt.nodes.new(type='ASEAtoms')
    atoms1.inputs["symbols"].default_value = "H2"
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = atoms1.get_results()
    assert len(results[0]["value"]) == 2
    assert results[1]["value"] == ["H"]*2


def test_bulk():
    """A nodetree for bulk."""
    nt = bpy.data.node_groups.new(name='test_bulk', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = bulk1.get_results()
    assert len(results[0]["value"]) == 4
    assert results[1]["value"] == ["Al"]*4

def test_ch4():
    """A nodetree for molecule."""
    nt = bpy.data.node_groups.new(name='test_ch4', type='ScinodeTree')
    mol1 = nt.nodes.new(type='ASEMolecule')
    mol1.inputs["formula"].default_value = "CH4"
    mol1.inputs["vacuum"].default_value = 5.0
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = mol1.get_results()
    assert len(results[0]["value"]) == 5
    assert results[0]["value"].cell[2][2] > 10


def test_fcc111():
    """A nodetree for molecule."""
    nt = bpy.data.node_groups.new(name='test_fcc111', type='ScinodeTree')
    surf1 = nt.nodes.new(type='ASESurface')
    surf1.function = "fcc111"
    surf1.inputs["symbol"].default_value = "Pt"
    surf1.inputs["size"].default_value = [1, 1, 4]
    surf1.inputs["vacuum"].default_value = 5.0
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = surf1.get_results()
    assert len(results[0]["value"]) == 4
    assert results[0]["value"].cell[2][2] > 10
    #
    nt.reset()
    surf1.function = "hcp0001"
    surf1.inputs["symbol"].default_value = "Ti"
    surf1.inputs["size"].default_value = [2, 2, 4]
    surf1.inputs["vacuum"].default_value = 10.0
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = surf1.get_results()
    assert len(results[0]["value"]) == 16
    assert results[0]["value"].cell[2][2] > 20
