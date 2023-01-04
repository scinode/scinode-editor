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
    platform: bpy.props.StringProperty(name="platform", default="Blender")
    description: bpy.props.StringProperty(name="uuid", default="")
    log: bpy.props.StringProperty(name="uuid", default="")
    #
    auto_udpate_state: bpy.props.BoolProperty(default = False, name = "auto_udpate_state",
        description = "Enable auto update state for this node tree")

    def launch(self, daemon_name=None):
        """Launch the nodetree."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.info("Launch NodeTree: {}".format(self.name))
        if daemon_name is not None:
            self.daemon_name = daemon_name
        self.state = "CREATED"
        self.action = "LAUNCH"
        ntdata = self.to_dict()
        lnt = LaunchNodeTree(ntdata)
        lnt.launch()
        self.update_state()

    def save_to_db(self):
        """Save nodetree to database."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.debug("save_to_db: {}".format(self.name))
        self.state = "CREATED"
        ntdata = self.to_dict()
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

        if self.uuid == '':
            self.uuid = str(uuid1())
        meta = self.meta_to_dict()
        nodes = self.nodes_to_dict(short=short)
        links = self.links_to_dict()
        data = {
            "version": "scinode@{}".format(__version__),
            "uuid": self.uuid,
            "name": self.name,
            "state": self.state,
            "action": self.action,
            "error": "",
            "meta": meta,
            "nodes": nodes,
            "links": links,
            "description": self.description,
            "log": self.log
        }
        return data

    def meta_to_dict(self):
        """Export metadata to a dict."""
        meta = {
            "identifier": self.bl_idname,
            "daemon_name": self.daemon_name,
            "parent": self.parent,
            "platform": self.platform,
        }
        return meta


    def __repr__(self) -> str:
        s = ""
        s += 'NodeTree(name="{}, uuid="{}")\n'.format(self.name, self.uuid)
        return s

    def nodes_to_dict(self, short=False):
        """Export nodes to a dict."""
        # save all relations using links
        nodes = {}
        for node in self.nodes:
            if short:
                nodes[node.name] = node.to_dict(short=short)
            else:
                nodes[node.name] = node.to_dict()
        return nodes


    def links_to_dict(self):
        """Export links to a dict."""
        # save all relations using links
        dbdata = []
        for link in self.links:
            dbdata.append({
                "from_socket": link.from_socket.name,
                "from_node_uuid": link.from_node.uuid,
                "from_node": link.from_node.name,
                "to_socket": link.to_socket.name,
                "to_node_uuid": link.to_node.uuid,
                "to_node": link.to_node.name,
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
        data = scinodedb["nodetree"].find_one(query, {"state": 1, "action": 1})
        if data is not None:
            self.state = data["state"]
            self.action = data["action"]
        else:
            self.state = "CREATED"
        self.update_node_state()

    def update_node_state(self):
        """Update node state.
        """
        for node in self.nodes:
            node.update_state()
