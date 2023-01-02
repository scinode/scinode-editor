import bpy
import time
import numpy as np

def test_getattr():
    """Test getattr."""
    nt = bpy.data.node_groups.new(name='test_getattr', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    att = nt.nodes.new("Getattr")
    att.inputs["Name"].default_value = "pbc"
    nt.links.new(bulk1.outputs[0], att.inputs["Source"])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = att.get_results()
    print("results: ", results)
    value = results[0]["value"]
    assert value[0] == True


def test_setattr():
    """Test setattr."""
    nt = bpy.data.node_groups.new(name='test_setattr', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    att = nt.nodes.new("Setattr")
    att.inputs["Name"].default_value = "pbc"
    #
    bool1 = nt.nodes.new("Bool")
    bool1.Bool = False
    nt.links.new(bulk1.outputs[0], att.inputs["Source"])
    nt.links.new(bool1.outputs[0], att.inputs["Value"])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = att.get_results()
    print("results: ", results)
    value = results[0]["value"]
    assert value.pbc[0] == False


def test_getitem():
    nt = bpy.data.node_groups.new(name='test_getitem', type='ScinodeTree')
    getitem1 = nt.nodes.new("Getitem")
    #
    linspace1 = nt.nodes.new("Numpy")
    linspace1.function = "linspace"
    linspace1.inputs["start"].default_value =  1
    linspace1.inputs["stop"].default_value =  5
    linspace1.inputs["num"].default_value =  5
    #
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  4
    arange1.inputs["step"].default_value =  2
    #
    nt.links.new(linspace1.outputs[0], getitem1.inputs["Source"])
    nt.links.new(arange1.outputs[0], getitem1.inputs["Index"])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = getitem1.get_results()
    print("results: ", results)
    value = results[0]["value"]
    assert value[1] == 4


def test_setitem():
    nt = bpy.data.node_groups.new(name='test_setitem', type='ScinodeTree')
    setitem1 = nt.nodes.new("Setitem")
    #
    linspace1 = nt.nodes.new("Numpy")
    linspace1.function = "linspace"
    linspace1.inputs["start"].default_value =  1
    linspace1.inputs["stop"].default_value =  5
    linspace1.inputs["num"].default_value =  5
    #
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  4
    arange1.inputs["step"].default_value =  2
    #
    linspace2 = nt.nodes.new("Numpy")
    linspace2.function = "linspace"
    linspace2.inputs["start"].default_value =  11
    linspace2.inputs["stop"].default_value =  12
    linspace2.inputs["num"].default_value =  2
    #
    nt.links.new(linspace1.outputs[0], setitem1.inputs["Source"])
    nt.links.new(arange1.outputs[0], setitem1.inputs["Index"])
    nt.links.new(linspace2.outputs[0], setitem1.inputs["Value"])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = setitem1.get_results()
    print("results: ", results)
    value = results[0]["value"]
    assert value[1] == 11
