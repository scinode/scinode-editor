from scinode.database.db import scinodedb
from pprint import pprint

def export_python_script(nt, filename=None):
    script = build_nodetree_python_script(nt)
    if filename is None:
        filename = "script_{}.py".format(nt.name)
    with open(filename, "w") as f:
        f.write(script)
        
def build_nodetree_python_script(nt):
    """build_nodetree_python_script
    """
    print(nt)
    s = """
import bpy

nt = bpy.data.node_groups.new(name="{}", type='ScinodeTree')
""".format(
        nt.name
    )
    # nodes
    for node in nt.nodes:
        s += """
node = nt.nodes.new("{0}")
node.name = "{1}"
""".format(
            node.bl_idname, node.name
        )
        # set node properties
        for name in node.properties:
            p = getattr(node, name)
            s += """node.{} = {}
""".format(
                    name, p
                )

    # links
    for link in nt.links:
        s += """
nt.links.new(nt.nodes["{}"].outputs["{}"], nt.nodes["{}"].inputs["{}"])""".format(
            link.from_node.name,
            link.from_socket.name,
            link.to_node.name,
            link.to_socket.name,
        )

    # launch
    s += """
nt.launch()
"""
    return s

if __name__ == "__main__":
    # query = {"index": 1}
    # export_python_script_from_db(query)
    import bpy
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
    export_python_script(nt)