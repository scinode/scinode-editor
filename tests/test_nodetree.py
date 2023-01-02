import bpy


def test_nodetree():
    bpy.data.node_groups.new(name='test_nodetree', type='ScinodeTree')
    assert 'test_nodetree' in bpy.data.node_groups

def test_launch():
    nt = bpy.data.node_groups.new(name='test_launch', type='ScinodeTree')
    nt.nodes.new(type='TestFloat')
    nt.launch()
