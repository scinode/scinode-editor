import bpy
from uuid import uuid1
import logging
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class ScinodeTreeNode():
    """
    Mix-in class for all nodes in this ScinodeTree type.

    Returns:
        _type_: _description_
    """

    db_name: bpy.props.StringProperty(name="db_name", default="node")
    node_type: bpy.props.StringProperty(name="node_type", default="Normal")
    uuid: bpy.props.StringProperty(name="uuid", default="")
    state: bpy.props.StringProperty(name="state", default="CREATED")
    action: bpy.props.StringProperty(name="action", default="")
    daemon_name: bpy.props.StringProperty(name="daemon_name", default="")
    counter: bpy.props.IntProperty(name="counter",
                                   description="Number of time this node has been executed.",
                                   default=0)
    nodetree_uuid: bpy.props.StringProperty(name="nodetree_uuid", default="")
    platform: bpy.props.StringProperty(name="platform", default="Blender")
    scatter_node: bpy.props.StringProperty(name="scatter_node",
                                             description="uuid of the scatter node",
                                             default="")
    scattered_from: bpy.props.StringProperty(name="scattered_from",
                                             description="uuid of the node this node copied from",
                                             default="")
    scattered_label: bpy.props.StringProperty(name="scattered_label",
                                              default="")
    description: bpy.props.StringProperty(name="description",
                                              default="")
    log: bpy.props.StringProperty(name="uuid", default="")

    args: bpy.props.StringProperty(
        name="args",
        description="args.",
        default='',
    )
    kwargs: bpy.props.StringProperty(
        name="kwargs",
        description="kwargs.",
        default='',
    )

    properties = []


    @classmethod
    def poll(cls, ntree):
        """A poll function to enable instantiation.
        """
        return ntree.bl_name == 'ScinodeTree'

    def reset(self):
        """Set the state of this node and all its child nodes to "CREATED".
        Note, due to the principle that each node run independently, this action
        will not affect its child nodes. One has to use reset node in the nodetree
        to reset its child nodes.
        """
        from scinode.core.db_nodetree import DBNodeTree
        nt = DBNodeTree(uuid=self.id_data.uuid)
        nt.reset_node(self.name)
        self.update_state()

    def pre_save(self):
        """Pre action before save to database."""
        if self.node_type.upper() == "GROUP":
            self.init_nodetree_group()
            self.ntg.daemon_name = self.daemon_name
            self.ntg.save_to_db()

    def expose(self):
        """Expose group input and output sockets.
        """
        pass

    def to_dict(self, short=False, daemon_name="localhost"):
        """Save all datas, include properties, input and output sockets.

        This will be called when execute nodetree
        """
        from scinode.version import __version__

        logger.debug(f"save_to_db: {self.name}")
        if not self.daemon_name:
            self.daemon_name = daemon_name
        self.pre_save()

        if self.uuid == '':
            self.uuid = str(uuid1())
        if short:
            data = {
                "name": self.name,
                "identifier": self.bl_idname,
                "node_type": self.node_type,
                "uuid": self.uuid,
            }
        else:
            metadata = self.get_metadata()
            properties = self.properties_to_dict()
            input_sockets = self.input_sockets_to_dict()
            output_sockets = self.output_sockets_to_dict()
            executor = self.executor_to_dict()

            data = {
                "version": "scinode@{}".format(__version__),
                "uuid": self.uuid,
                "id": self.id_data.nodes.find(self.name),
                "name": self.name,
                "state": self.state,
                "action": self.action,
                "error": "",
                "metadata": metadata,
                "properties": properties,
                "inputs": input_sockets,
                "outputs": output_sockets,
                "executor": executor,
                "position": [0, 0],
                "description": self.description,
                "log": self.log,
            }

        return data

    def get_metadata(self):
        """save metadata data"""
        metadata = {
            "node_type": self.node_type,
            "identifier": self.bl_idname,
            "nodetree_uuid": self.id_data.uuid,
            "platform": self.platform,
            "scatter_node": self.scatter_node,
            "scattered_from": self.scattered_from,
            "scattered_label": self.scattered_label,
            "counter": self.counter,
            "args": [x for x in self.args.replace(' ', '').split(",") if x != ''],
            "kwargs": [x for x in self.kwargs.replace(' ', '').split(",") if x!= ''],
            "group_inputs": self.group_inputs,
            "group_outputs": self.group_outputs,
        }
        if self.daemon_name == "":
            metadata.update({"daemon_name": self.id_data.daemon_name})
        else:
            metadata.update({"daemon_name": self.daemon_name})
        return metadata

    def properties_to_dict(self):
        """save data used for calculation."""
        from scinode_editor.utils import type_bl_to_python
        properties = {}
        for p in self.properties:
            properties[p] = {
                "value": type_bl_to_python(getattr(self, p)),
                "name": p,
                # "type": p.data_type,
                "serialize": {
                    "path": "scinode.serialization.built_in",
                    "name": "serialize_pickle",
                },
                "deserialize": {
                    "path": "scinode.serialization.built_in",
                    "name": "deserialize_pickle",
                },
            }
        # default value of sockets
        for input in self.inputs:
            properties[input.name] = {
                "value": input.get_default_value(),
                "name": input.name,
                # "type": p.data_type,
                "serialize": input.get_serialize(),
                "deserialize": input.get_deserialize(),
            }
        return properties


    def input_sockets_to_dict(self):
        """Save input sockets
        """
        dbdata = sockets_as_dbdata(self.inputs)
        return dbdata

    def output_sockets_to_dict(self):
        """Save output sockets
        """
        dbdata = sockets_as_dbdata(self.outputs)
        return dbdata

    def executor_to_dict(self):
        """Save run executor"""
        executor = self.get_executor()
        if "name" not in executor:
            executor["name"] = executor["path"].split(".")[-1]
            executor["path"] = executor["path"][0 : -(len(executor["name"]) + 1)]
        if "type" not in executor:
            executor["type"] = "function"
        return executor

    def get_dbdata(self, query, fliter={}):
        from scinode.database.db import scinodedb
        data = scinodedb["node"].find_one(
            query, fliter
        )
        return data

    def update_state(self):
        # print("update node: {}".format(self.name))
        query = {"uuid": self.uuid}
        fliter = {"state": 1, "action": 1, "metadata.counter": 1}
        data = self.get_dbdata(query, fliter)
        if data is not None:
            self.counter = data["metadata"]["counter"]
        else:
            self.state = "CREATED"
        self.update_item_color()

    def update_item_color(self):
        """Set item's color based on the state."""
        self.use_custom_color = True
        state = self.state
        if state.upper() == "CREATED":
            self.color = [0.2, 0.2, 0]
        elif state.upper() == "RUNNING":
            self.color = [0, 0, 0.5]
        elif state.upper() == "FINISHED":
            self.color = [0, 0.5, 0]
        elif state.upper() == "PAUSED":
            self.color = [0, 0.5, 0.5]
        elif state.upper() == "KILLED":
            self.color = [0.5, 0, 0]

    def get_results(self):
        """Item data from database.

        Returns:
            dict: _description_
        """
        from scinode.database.db import scinodedb
        from scinode.utils.node import deserialize_item
        results = []
        for output in self.outputs:
            query = {"uuid": output.uuid}
            data = scinodedb["data"].find_one(query, {"_id": 0})
            if data:
                results += [deserialize_item(data)]
            else:
                results += [data]
        return results

    def pre_load(self, ndata):
        """Pre load.

        Args:
            ndata (_type_): _description_
        """
        pass

    def pause(self):
        from scinode.core.db_nodetree import DBNodeTree
        nt = DBNodeTree(uuid=self.id_data.uuid)
        nt.pause_node(self.name)
        self.update_state()

    def play(self):
        from scinode.core.db_nodetree import DBNodeTree
        nt = DBNodeTree(uuid=self.id_data.uuid)
        nt.play_node(self.name)
        self.update_state()

    @property
    def parent_nodes(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        from scinode.utils.node import find_input_nodes
        from scinode.database.db import scinodedb

        nodes = find_input_nodes(self.input_sockets_to_dict(), scinodedb["node"])
        # print("Total: {} parent nodes.".format(len(nodes)))
        return nodes

    def get_input_parameters_from_db(self):
        """get inputs from database

        The inputs are the outputs of parent nodes and
        the properties of the node itself.

        Returns:
            _type_: _description_
        """
        from scinode.utils.node import get_input_parameters_from_db
        from scinode.database.db import scinodedb
        query = {"uuid": self.uuid}
        dbdata = scinodedb["node"].find_one(
            query, {"_id": 0}
        )
        paramters = get_input_parameters_from_db(dbdata)
        return paramters

    @classmethod
    def load_from_db(cls, nodetree, uuid):
        """Load Node data from database.
        """
        from scinode.database.db import scinodedb
        ndata = scinodedb["node"].find_one({"uuid": uuid})
        node = cls.build_node(nodetree, ndata)
        return node

    def update_from_dict(self, ndata):
        """update node from dict.
        """
        from scinode_editor.utils import type_python_to_bl
        for key in ['identifier',  'node_type', 'nodetree_uuid', 'scattered_from',
                    'scattered_label', 'counter',
                    'platform']:
            if ndata.get(key):
                setattr(self, key, ndata["metadata"][key])
        properties = ndata['properties']
        # set properties
        for name, p in properties.items():
            value = type_python_to_bl(p['value'])
            setattr(self, name, value)
        # set input sockets if the no link
        for input in self.inputs:
            if input.name in properties:
                input.set_default_value(type_python_to_bl(properties[input.name]['value']))

    @classmethod
    def build_node(cls, nodetree, ndata, name=""):
        """Build Scinode

        Args:
            nodetree (_type_): _description_
            ndata (_type_): _description_
            db (_type_): _description_

        Returns:
            _type_: _description_
        """
        node = nodetree.nodes.new(type=ndata["metadata"]["identifier"])
        # assgin name and uuid from database
        node.name = name
        for key in ["uuid", "state", "action", "description"]:
            if ndata.get(key):
                setattr(node, key, ndata.get(key))
        # nodes[node.uuid] = node
        # get node data from database
        node.update_from_dict(ndata)
        return node

    def get_executor(self):
        """"""
        executor = None
        if self.node_type.upper() == "GROUP":
            executor = {
                "path": "scinode.executors.built_in",
                "name": "NodeGroup",
                "type": "class",
            }
        return executor

    def init_nodetree_group(self):
        """init the nodetree group (ntg)"""
        from scinode_editor.node_tree import ScinodeTree

        ntdata = self.node_group()
        ntdata["name"] = self.name
        logger.debug(f"node uuid: {self.uuid}")
        ntdata["uuid"] = self.uuid
        ntdata["metadata"]["daemon_name"] = self.daemon_name
        ntdata["metadata"]["parent_node"] = self.uuid
        self.ntg = ScinodeTree.from_dict(ntdata)

    def create_sockets(self):
        """Create input and output sockets"""
        self.inputs.clear()
        self.outputs.clear()
        if self.node_type.upper() == "GROUP":
            self.create_group_sockets()

    def create_group_sockets(self):
        """Create input and output sockets based on group inputs
        and outputs.

        group_inputs = [
            ["add1", "x", "x"],
            ["add1", "y", "y"],
        ]
        """
        for input in self.group_inputs:
            node, socket, name = input
            logger.debug(f"create input: {name}")
            identifier = self.ntg.nodes[node].inputs[socket].bl_idname
            self.inputs.new(identifier, name)
        for output in self.group_outputs:
            node, socket, name = output
            logger.debug(f"create output: {name}")
            identifier = self.ntg.nodes[node].outputs[socket].bl_idname
            self.outputs.new(identifier, name)

    @property
    def group_inputs(self):
        return self.get_group_inputs()

    def get_group_inputs(self):
        return []

    @property
    def group_outputs(self):
        return self.get_group_outputs()

    def get_group_outputs(self):
        return []

class BaseNode(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'BaseNode'
    bl_label = "ScinodeTree Base Node"


    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        for key in self.properties:
            layout.prop(self, key, text="")

    def copy(self, node):
        print("Copying from node: ", node.name)
        newnode = self.id_data.nodes[-1]
        newnode.uuid = ""


def update_sockets(self, context):
    self.inputs.clear()
    self.outputs.clear()
    self.init(context)


def sockets_as_dbdata(sockets):
    """Save sockets to dbdata
    """
    # save all relations using links
    dbdata = []
    for socket in sockets:
        if socket.uuid == '':
            socket.uuid = str(uuid1())
        data = {
            'name': socket.name,
            'link_limit': socket.link_limit,
            # 'value': socket.get_default_value(),
            "uuid": socket.uuid,
            "node_uuid": socket.node.uuid,
            "identifier": socket.bl_idname,
            "links": [],
            "serialize": socket.get_serialize(),
            "deserialize": socket.get_deserialize(),
        }
        logger.debug("Save socket to db: {}".format(socket.name))
        for link in socket.links:
            # we only handle one sockek one link yet.
            # for output socket, this is not a problem.
            data["links"].append({
                'from_node': link.from_node.name,
                'from_socket': link.from_socket.name,
                'from_socket_uuid': link.from_socket.uuid,
                'to_node': link.to_node.name,
                'to_socket': link.to_socket.name,
                'to_socket_uuid': link.to_socket.uuid,
                'value': None,
                'index': link.from_node.outputs.find(link.from_socket.name),
            }
            )
        dbdata.append(data)
    return dbdata
