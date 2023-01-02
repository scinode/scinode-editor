import bpy

def test_node_type():
    bpy.data.node_groups.new(name='test_node_type', type='ScinodeTree')
    scatter1 = bpy.data.node_groups['test_node_type'].nodes.new(type="Scatter")
    switch1 = bpy.data.node_groups['test_node_type'].nodes.new(type="Switch")
    update1 = bpy.data.node_groups['test_node_type'].nodes.new(type="Update")
    float1 = bpy.data.node_groups['test_node_type'].nodes.new(type="TestFloat")
    assert scatter1.node_type.upper() == "SCATTER"
    assert switch1.node_type.upper() == "SWITCH"
    assert update1.node_type.upper() == "UPDATE"


def test_switch_update():
    import time
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_switch_update', type='ScinodeTree')
    switch = nt.nodes.new("Switch")
    update = nt.nodes.new("Update")
    math1 = nt.nodes.new("TestAdd")
    float1 = nt.nodes.new("TestFloat")
    float1.Float = 2
    float2 = nt.nodes.new("TestFloat")
    float2.Float = 3
    #
    math2 = nt.nodes.new("TestLess")
    math2.inputs[1].default_value = 10
    #
    nt.links.new(float1.outputs[0], math1.inputs[0])
    nt.links.new(float2.outputs[0], update.inputs[0])
    nt.links.new(update.outputs[0], math1.inputs[1])
    nt.links.new(math1.outputs[0], math2.inputs[0])
    nt.links.new(math1.outputs[0], switch.inputs[0])
    nt.links.new(math2.outputs[0], switch.inputs[1])
    nt.links.new(switch.outputs[0], update.inputs[1])
    #
    nt.launch()
    time.sleep(20)
    nt.update_state()
    results = math1.get_results()
    value = results[0]['value']
    assert np.isclose(value, 11)
    assert update.counter == 4
