import bpy


def test_nodetree():
    bpy.data.node_groups.new(name='test_nodetree', type='ScinodeTree')
    assert 'test_nodetree' in bpy.data.node_groups

def test_save():
    nt = bpy.data.node_groups.new(name='test_save', type='ScinodeTree')
    float1 = nt.nodes.new(type='TestFloat')
    add1 = nt.nodes.new(type='TestAdd')
    nt.save_to_db()
    nt.update_state()
    assert float1.uuid != ""
    assert float1.state == "CREATED"

def test_launch():
    nt = bpy.data.node_groups.new(name='test_launch', type='ScinodeTree')
    nt.nodes.new(type='TestFloat')
    nt.launch()
