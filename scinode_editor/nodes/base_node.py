import bpy
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

    def to_dict(self, short=False):
        """Save all datas, include properties, input and output sockets.

        This will be called when execute nodetree
        """
        from scinode.version import __version__
        from uuid import uuid1

        logger.debug("save_to_db: {}".format(self.name))
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
            meta = self.meta_to_dict()
            properties = self.properties_to_dict()
            input_sockets = self.input_sockets_to_dict()
            output_sockets = self.output_sockets_to_dict()
            executor = self.executor_to_dict()
            results = self.init_results()

            data = {
                "version": "scinode@{}".format(__version__),
                "uuid": self.uuid,
                "id": self.id_data.nodes.find(self.name),
                "name": self.name,
                "state": self.state,
                "action": self.action,
                "error": "",
                "meta": meta,
                "properties": properties,
                "inputs": input_sockets,
                "outputs": output_sockets,
                "executor": executor,
                "results": results,
                "position": [0, 0],
                "description": self.description,
                "log": self.log,
            }

        return data

    def meta_to_dict(self):
        """save meta data"""
        meta = {
            "node_type": self.node_type,
            "identifier": self.bl_idname,
            "nodetree_uuid": self.id_data.uuid,
            "platform": self.platform,
            "scattered_from": self.scattered_from,
            "scattered_label": self.scattered_label,
            "counter": self.counter,
            "args": [x for x in self.args.replace(' ', '').split(",") if x != ''],
            "kwargs": [x for x in self.kwargs.replace(' ', '').split(",") if x!= ''],
        }
        if self.daemon_name == "":
            meta.update({"daemon_name": self.id_data.daemon_name})
        else:
            meta.update({"daemon_name": self.daemon_name})
        return meta

    def properties_to_dict(self):
        """save data used for calculation."""
        from scinode_editor.utils import type_bl_to_python
        properties = {}
        for p in self.properties:
            properties[p] = {
                "value": type_bl_to_python(getattr(self, p)),
                "name": p,
                # "type": p.data_type,
            }
        # default value of sockets
        for input in self.inputs:
            properties[input.name] = {
                "value": input.get_default_value(),
                "name": input.name,
                # "type": p.data_type,
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
        executor = self.get_executor() or self.executor
        if "name" not in executor:
            executor["name"] = executor["path"].split(".")[-1]
            executor["path"] = executor["path"][0 : -(len(executor["name"]) + 1)]
        if "type" not in executor:
            executor["type"] = "function"
        return executor

    def init_results(self):
        #
        if not hasattr(self, "results") or len(self.results) != len(self.outputs):
            results = ()
            for output in self.outputs:
                results += ({"name": output.name, "value": output.default_value},)
            return results
        else:
            return getattr(self, "results")


    def get_dbdata(self, query, fliter={}):
        from scinode.database.db import scinodedb
        data = scinodedb["node"].find_one(
            query, fliter
        )
        return data

    def update_state(self):
        # print("update node: {}".format(self.name))
        query = {"uuid": self.uuid}
        fliter = {"state": 1, "action": 1, "results": 1, "meta.counter": 1}
        data = self.get_dbdata(query, fliter)
        if data is not None:
            self.state = data["state"]
            self.action = data["action"]
            self.counter = data["meta"]["counter"]
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
        import pickle

        query = {"uuid": self.uuid}
        data = scinodedb["node"].find_one(query, {"results": 1})
        results = pickle.loads(data["results"])
        return results

    def pre_load(self, ndata):
        """Pre load.

        Args:
            ndata (_type_): _description_
        """
        pass

    def load_data_from_db(self, uuid=None):
        """Load Node data from database.
        """
        from scinode.database.db import scinodedb
        import pickle
        from scinode_editor.utils import type_python_to_bl
        if uuid is None:
            uuid = self.uuid
        ndata = scinodedb["node"].find_one({"uuid": uuid})
        self.pre_load(ndata)
        self.name = ndata["name"]
        for key in ['identifier',  'node_type', 'nodetree_uuid', 'scattered_from',
                    'scattered_label', 'counter',
                    'platform']:
            setattr(self, key, ndata["meta"][key])
        properties = pickle.loads(ndata['properties'])
        # set properties
        print("properties: ", properties)
        print("Set properties: ")
        for name, p in properties.items():
            value = type_python_to_bl(p['value'])
            print(name, value, type(value))
            setattr(self, name, value)
        # set input sockets if the no link
        print("Set input: ")
        for input in self.inputs:
            if input.name in properties:
                input.set_default_value(type_python_to_bl(properties[input.name]['value']))

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
            query, {"_id": 0, "results": 0}
        )
        paramters = get_input_parameters_from_db(dbdata)
        return paramters

class ScinodeTreeBaseNode(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'ScinodeTreeBaseNode'
    bl_label = "ScinodeTree Base Node"

    x: bpy.props.BoolProperty(
        name="x",
        description="Is integer.",
        default=False,
    )

    properties = ["x"]

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        for key, value in self.properties.items():
            layout.prop(self, key, text="")

    def get_executor(self):
        return None


def update_sockets(self, context):
    self.inputs.clear()
    self.outputs.clear()
    self.init(context)


def sockets_as_dbdata(sockets):
    """Save sockets to dbdata
    """
    # save all relations using links
    from scinode_editor.utils import type_bl_to_python
    dbdata = []
    for socket in sockets:
        data = {
            'name': socket.name,
            'link_limit': socket.link_limit,
            # 'value': socket.get_default_value(),
            "links": [],
        }
        logger.debug("Save socket to db: {}".format(socket.name))
        for link in socket.links:
            # we only handle one sockek one link yet.
            # for output socket, this is not a problem.
            data["links"].append({
                'from_node_uuid': link.from_node.uuid,
                'from_node': link.from_node.name,
                'from_socket': link.from_socket.name,
                'to_node_uuid': link.to_node.uuid,
                'to_node': link.to_node.name,
                'to_socket': link.to_socket.name,
                'value': None,
                'index': link.from_node.outputs.find(link.from_socket.name),
            }
            )
        dbdata.append(data)
    return dbdata
