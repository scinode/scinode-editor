import bpy


def build_nodetree(ntdata, db):
    """Recreate the nodetree from database
    Args:
        ntdata (dict): data of the nodetree
    """
    # new nodetree with type ScinodeTree
    nt = bpy.data.node_groups.new(name=ntdata["name"], type="ScinodeTree")
    # asgin the uuid from database
    nt.uuid = ntdata["uuid"]
    nt.daemon_name = ntdata["meta"]["daemon_name"]
    nodes = {}
    for name, ndata in ntdata["nodes"].items():
        print(
            "Node name: {}, identifier: {}".format(ndata["name"], ndata["identifier"])
        )
        # new node with nodetype
        node = build_node(nt, ndata, db)
        nodes[name] = node
    # re-build links
    for link in ntdata["links"]:
        print("link: ", link)
        # check if link exist
        if link["from_node"] in nodes and link["to_node"] in nodes:
            nt.links.new(
                nodes[link["from_node"]].outputs[link["from_socket"]],
                nodes[link["to_node"]].inputs[link["to_socket"]],
            )
    return nt


def build_node(nodetree, ndata, db):
    """Build Scinode

    Args:
        nodetree (_type_): _description_
        ndata (_type_): _description_
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    node = nodetree.nodes.new(type=ndata["identifier"])
    # assgin name and uuid from database
    print("Re-build node: {}".format(ndata["name"]))
    node.name = ndata["name"]
    node.uuid = ndata["uuid"]
    # nodes[node.uuid] = node
    # get node data from database
    node.load_data_from_db()
    return node
