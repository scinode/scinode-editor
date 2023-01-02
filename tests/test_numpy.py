import bpy
import time



def test_numpy():
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_numpy', type='ScinodeTree')
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  4
    arange1.inputs["step"].default_value =  2
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = arange1.get_results()
    value = results[0]['value']
    assert len(value) == 2

def test_numpy_add():
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_numpy_add', type='ScinodeTree')
    float1 = nt.nodes.new("Float")
    float1.Float = 2
    float2 = nt.nodes.new("Float")
    float2.Float = 3
    add1 = nt.nodes.new("Numpy")
    add1.function = "add"
    debug1 = nt.nodes.new("Print")
    nt.links.new(float1.outputs[0], add1.inputs[0])
    nt.links.new(float2.outputs[0], add1.inputs[1])
    nt.links.new(add1.outputs[0], debug1.inputs[0])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = add1.get_results()
    value = results[0]['value']
    assert value == 5
