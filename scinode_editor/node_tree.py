import bpy
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class ScinodeTree(bpy.types.NodeTree):
    """Nodetree is a collection of nodes and links.

    Attributes:

    Examples:

    >>> nt = bpy.data.node_groups.new(name='test', type='ScinodeTree')

    add nodes:

    >>> float1 = nt.nodes.new("TestFloat")
    >>> add1 = nt.nodes.new("TestAdd")

    add links:

    >>> nt.links.new(float1.outputs[0], add1.inputs[0])

    Launch the nodetree:

    >>> nt.launch()

    """

    bl_idname = 'ScinodeTree'
    bl_label = "Scinode Editor"
    bl_icon = 'KEYTYPE_EXTREME_VEC'

    db_name: bpy.props.StringProperty(name="db_name", default="nodetree")
    uuid: bpy.props.StringProperty(name="uuid", default="")
    state: bpy.props.StringProperty(name="state", default="")
    action: bpy.props.StringProperty(name="uuid", default="")
    daemon_name: bpy.props.StringProperty(name="daemon_name", default="localhost")
    parent: bpy.props.StringProperty(name="parent", default="")
    parent_node: bpy.props.StringProperty(name="parent_node", default="")
    platform: bpy.props.StringProperty(name="platform", default="Blender")
    description: bpy.props.StringProperty(name="uuid", default="")
    log: bpy.props.StringProperty(name="uuid", default="")
    scatter_node: bpy.props.StringProperty(name="scatter_node",
                                             description="uuid of the scatter node",
                                             default="")
    #
    auto_udpate_state: bpy.props.BoolProperty(default = False, name = "auto_udpate_state",
        description = "Enable auto update state for this node tree")

    def launch(self, daemon_name=None):
        """Launch the nodetree."""
        from scinode.engine.send_to_queue import launch_nodetree
        logger.info("Launch NodeTree: {}".format(self.name))
        if daemon_name is not None:
            self.daemon_name = daemon_name
        self.save_to_db()
        launch_nodetree(self.daemon_name, self.uuid)
        self.update_state()

    def save_to_db(self):
        """Save nodetree to database."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.debug("save_to_db: {}".format(self.name))
        self.state = "CREATED"
        ntdata = self.to_dict()
        # print("links: ", ntdata["links"])
        # print("nodes: ", ntdata["nodes"])
        lnt = LaunchNodeTree(ntdata)
        lnt.save()
        self.update_state()

    def to_dict(self, short=False):
        """Export nodetree to a dict.

        Returns:
            dict: nodetree data
        """
        from scinode.version import __version__
        from uuid import uuid1

        # update uuid for nodetree, nodes, sockets
        if self.uuid == '':
            self.uuid = str(uuid1())
        metadata = self.get_metadata()
        nodes = self.nodes_to_dict(short=short)
        links = self.links_to_dict()
        data = {
            "version": "scinode@{}".format(__version__),
            "uuid": self.uuid,
            "name": self.name,
            "state": self.state,
            "action": self.action,
            "error": "",
            "metadata": metadata,
            "nodes": nodes,
            "links": links,
            "description": self.description,
            "log": self.log
        }
        return data

    def get_metadata(self):
        """Export metadata to a dict."""
        metadata = {
            "identifier": self.bl_idname,
            "daemon_name": self.daemon_name,
            "parent_node": self.parent_node,
            "parent": self.parent,
            "platform": self.platform,
            "scatter_node": self.scatter_node,
        }
        return metadata


    def __repr__(self) -> str:
        s = ""
        s += 'NodeTree(name="{}, uuid="{}")\n'.format(self.name, self.uuid)
        return s

    def nodes_to_dict(self, short=False):
        """Export nodes to a dict."""
        # save all relations using links
        from uuid import uuid1
        nodes = {}
        for node in self.nodes:
            node.name = node.name.replace(".", "_")
            if node.uuid == '':
                node.uuid = str(uuid1())
            # add uuid for socket
            for output in node.outputs:
                if output.uuid == '':
                    output.uuid = str(uuid1())
        for node in self.nodes:
            node.name = node.name.replace(".", "_")
            if short:
                nodes[node.name] = node.to_dict(short=short)
            else:
                nodes[node.name] = node.to_dict(daemon_name=self.daemon_name)
        return nodes


    def links_to_dict(self):
        """Export links to a dict."""
        # save all relations using links
        dbdata = []
        for link in self.links:
            dbdata.append({
                "from_socket": link.from_socket.name,
                "from_node": link.from_node.name.replace(".", "_"),
                "to_socket": link.to_socket.name,
                "to_node": link.to_node.name.replace(".", "_"),
            }
            )
        return dbdata

    def reset(self):
        """Reset all nodes."""
        from scinode.core.db_nodetree import DBNodeTree
        nt = DBNodeTree(uuid=self.uuid)
        nt.reset()
        self.update_state()

    def update_state(self):
        """Update state of nodetree and its nodes.
        """
        from scinode.database.db import scinodedb

        query = {"uuid": self.uuid}
        data = scinodedb["nodetree"].find_one(query, {"state": 1, "action": 1, "nodes": 1})
        if data is not None:
            self.state = data["state"]
            self.action = data["action"]
            for node in self.nodes:
                node.state = data["nodes"][node.name]["state"]
                node.update_item_color()
        else:
            self.state = "CREATED"

    def update_node_state(self):
        """Update node state.
        """
        for node in self.nodes:
            node.update_state()

    @classmethod
    def load_from_db(cls, uuid):
        """Load Node data from database.
        """
        from scinode.utils.nodetree import get_nt_full_data
        ntdata = get_nt_full_data({"uuid": uuid})
        nt = cls.from_dict(ntdata)
        return nt

    @classmethod
    def from_dict(cls, ntdata):
        """Rebuild nodetree from dict ntdata.

        Args:
            ntdata (dict): data of the nodetree.

        Returns:
            Nodedtree: a nodetree
        """
        from scinode_editor.nodes.base_node import BaseNode
        # new nodetree with type ScinodeTree
        nt = bpy.data.node_groups.new(name=ntdata["name"], type="ScinodeTree")
        # asgin the uuid from database
        nt.uuid = ntdata["uuid"]
        nt.daemon_name = ntdata["metadata"]["daemon_name"]
        nodes = {}
        for name, ndata in ntdata["nodes"].items():
            print(
                f"Node name: {name}, identifier: {ndata['metadata']['identifier']}"
            )
            # new node with nodetype
            node = BaseNode.build_node(nt, ndata, name=name)
            nodes[name] = node
        # re-build links
        for link in ntdata["links"]:
            # check if link exist
            if link["from_node"] in nodes and link["to_node"] in nodes:
                nt.links.new(
                    nodes[link["from_node"]].outputs[link["from_socket"]],
                    nodes[link["to_node"]].inputs[link["to_socket"]],
                )
        return nt
