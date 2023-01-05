import bpy
import time
import numpy as np

def test_scatter():
    nt = bpy.data.node_groups.new(name='test_scatter', type='ScinodeTree')
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  5
    arange1.inputs["step"].default_value =  1
    scatter = nt.nodes.new(type='Scatter')
    float1 = nt.nodes.new(type='TestFloat')
    float1.Float = 2
    add1 = nt.nodes.new(type='TestAdd')
    add2 = nt.nodes.new(type='TestAdd')
    add2.y = 2
    debug = nt.nodes.new(type='Print')
    nt.links.new(arange1.outputs['Result'], scatter.inputs['Input'])
    nt.links.new(scatter.outputs['Result'], add1.inputs[0])
    nt.links.new(float1.outputs['Float'], add1.inputs[1])
    nt.links.new(add1.outputs['Result'], add2.inputs[0])
    nt.links.new(add2.outputs['Result'], debug.inputs[0])
    nt.launch()
    time.sleep(20)
    nt.update_state()
    results = add2.get_results()
    value = results[0]['value']
    print("value: ", value)
    assert len(value) == 4
    assert value[0] == 3.0

def test_scatter_stop():
    nt = bpy.data.node_groups.new(name='test_scatter_stop', type='ScinodeTree')
    arange1 = nt.nodes.new("Numpy")
    arange1.function = "arange"
    arange1.inputs["start"].default_value =  1
    arange1.inputs["stop"].default_value =  4
    arange1.inputs["step"].default_value =  2
    scatter = nt.nodes.new(type='Scatter')
    float1 = nt.nodes.new(type='TestFloat')
    float1.Float = 2
    add1 = nt.nodes.new(type='TestAdd')
    add1.function = 'add'
    greater1 = nt.nodes.new(type='TestGreater')
    greater1.function = 'greater'
    greater1.inputs[1].default_value = 4
    #
    npnode4 = nt.nodes.new(type='TestAdd')
    npnode4.function = 'add'
    npnode4.inputs[1].default_value = 4
    npnode5 = nt.nodes.new(type='TestAdd')
    npnode5.function = 'add'
    npnode5.inputs[1].default_value = 5
    debug1 = nt.nodes.new(type='Print')
    debug2 = nt.nodes.new(type='Print')
    nt.links.new(arange1.outputs['Result'], scatter.inputs['Input'])
    nt.links.new(scatter.outputs['Result'], add1.inputs[0])
    nt.links.new(scatter.outputs['Result'], npnode4.inputs[0])
    nt.links.new(float1.outputs['Float'], add1.inputs[1])
    nt.links.new(add1.outputs['Result'], greater1.inputs[0])
    nt.links.new(greater1.outputs['Result'], debug1.inputs[0])
    nt.links.new(npnode4.outputs['Result'], npnode5.inputs[0])
    nt.links.new(npnode5.outputs['Result'], debug2.inputs[0])
    nt.links.new(npnode5.outputs['Result'], scatter.inputs[1])
    nt.launch()
    results = scatter.get_results()
    value = results[0]['value']
    print("value: ", value)
