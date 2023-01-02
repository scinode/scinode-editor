import bpy
import time



def test_debug_math():
    import numpy as np
    nt = bpy.data.node_groups.new(name='test_debug_math', type='ScinodeTree')
    math1 = nt.nodes.new(type='TestAdd')
    float1 = nt.nodes.new(type='TestFloat')
    float1.Float = 2
    floag2 = nt.nodes.new(type='TestFloat')
    floag2.Float = 3
    nt.links.new(float1.outputs[0],
                                math1.inputs['x'])
    nt.links.new(floag2.outputs[0],
                                math1.inputs['y'])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = math1.get_results()
    value = results[0]['value']
    assert np.isclose(value, 5.0)
