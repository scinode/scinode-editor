import bpy


def test_node():
    bpy.data.node_groups.new(name='test_node', type='ScinodeTree')
    float1 = bpy.data.node_groups['test_node'].nodes.new(type="TestFloat")
    assert float1.name in bpy.data.node_groups['test_node'].nodes

def test_copy():
    """Test copy."""
    bpy.data.node_groups.new(name='test_copy', type='ScinodeTree')
    float1 = bpy.data.node_groups['test_copy'].nodes.new(type="TestFloat")
