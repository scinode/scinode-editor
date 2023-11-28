import bpy


def test_pause_node():
    import time
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_pause_node', type='ScinodeTree')
    float1 = nt.nodes.new(type='TestFloat')
    float1.Float = 2
    float2 = nt.nodes.new(type='TestFloat')
    float2.Float = 5
    math1 = nt.nodes.new(type='TestAdd')
    math1.t = 3
    math1.x = 2
    math2 = nt.nodes.new(type='TestAdd')
    math2.t = 3
    math2.x = 2
    math3 = nt.nodes.new(type='TestAdd')
    math3.t = 3
    math3.x = 2
    nt.links.new(float1.outputs[0], math1.inputs[0])
    nt.links.new(float2.outputs[0], math2.inputs[0])
    nt.links.new(math1.outputs[0], math3.inputs[0])
    nt.links.new(math2.outputs[0], math3.inputs[1])
    nt.launch()
    math2.pause()
    time.sleep(10)
    nt.update_state()
    assert math2.state == 'PAUSED'
    assert math3.state == 'CREATED'
    time.sleep(10)
    math2.play()
    time.sleep(10)
    nt.update_state()
    results = math3.get_results()
    value = results[0]['value']
    assert np.isclose(value, 7.0)
