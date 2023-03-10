import bpy
import time



def test_node_group():
    import bpy
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_node_group', type='ScinodeTree')
    float1 = nt.nodes.new(type='TestFloat')
    float1.Float = 4
    floag2 = nt.nodes.new(type='TestFloat')
    floag2.Float = 9
    sqrt_add1 = nt.nodes.new(type='TestSqrtAdd')
    assert len(sqrt_add1.inputs) == 2
    assert len(sqrt_add1.outputs) == 1
    nt.links.new(float1.outputs[0],
                                sqrt_add1.inputs['x'])
    nt.links.new(floag2.outputs[0],
                                sqrt_add1.inputs['y'])
    nt.launch()
    time.sleep(10)
    nt.update_state()
    results = sqrt_add1.get_results()
    value = results[0]['value']
    assert np.isclose(value, 5.0)
