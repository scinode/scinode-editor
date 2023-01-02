import bpy
import time



def test_showcase():
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_showcase', type='ScinodeTree')
    n = 10
    adds1 = []
    for i in range(n):
        float1 = nt.nodes.new(type='TestFloat')
        float1.Float = 1
        add1 = nt.nodes.new(type='TestAdd')
        add1.t = 0
        add1.inputs["x"].default_value = 1
        adds1.append(add1)
        nt.links.new(float1.outputs[0], add1.inputs[1])

    adds2 = []
    for i in range(n):
        float1 = nt.nodes.new(type='TestFloat')
        float1.Float = 1
        add1 = nt.nodes.new(type='TestAdd')
        add1.t = 1.5
        add1.inputs["x"].default_value = 1
        adds2.append(add1)
        nt.links.new(float1.outputs[0], add1.inputs[1])

    for i in range(n - 1):
        nt.links.new(adds1[i].outputs[0], adds1[i + 1].inputs[0])
        nt.links.new(adds2[i].outputs[0], adds2[i + 1].inputs[0])

    add1 = nt.nodes.new(type='TestAdd')
    nt.links.new(adds1[-1].outputs[0], add1.inputs[0])
    nt.links.new(adds2[-1].outputs[0], add1.inputs[1])
    debug = nt.nodes.new(type='Print')
    nt.links.new(add1.outputs[0], debug.inputs[0])
    nt.launch()
    time.sleep(30)
    nt.update_state()
    results = add1.get_results()
    value = results[0]['value']
    assert np.isclose(value, 22.0)
