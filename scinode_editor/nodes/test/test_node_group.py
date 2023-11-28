

import bpy
from scinode_editor.nodes.base_node import BaseNode


class TestSqrtAdd(BaseNode):
    bl_idname = 'TestSqrtAdd'
    bl_label = "Sqrt Add Node"
    bl_icon = "OUTLINER_OB_POINTCLOUD"


    def init(self, context):
        from uuid import uuid1
        if self.uuid == '':
            self.uuid = str(uuid1())
        self.node_type = "GROUP"
        self.init_nodetree_group()
        self.create_properties()
        self.create_sockets()

    def get_group_properties(self):
        group_properties = [
            ["sqrt1", "t", "t1"],
            ["add1", "t", "t2"],
        ]
        return group_properties

    def get_group_inputs(self):
        group_inputs = [
            ["sqrt1", "x", "x"],
            ["sqrt2", "x", "y"],
        ]
        return group_inputs

    def get_group_outputs(self):
        group_outputs = [["add1", "Result", "Result"]]
        return group_outputs


    def get_node_group(self):
        ntdata = {
            "metadata": {
                "platform": "scinode",
            },
            "nodes": {
                "sqrt1": {
                    "metadata": {
                        "identifier": "TestSqrt",
                    },
                    "properties": {},
                },
                "sqrt2": {
                    "metadata": {
                        "identifier": "TestSqrt",
                    },
                    "properties": {},
                },
                "add1": {
                    "metadata": {
                        "identifier": "TestAdd",
                    },
                    "properties": {},
                },
            },
            "links": [
                {
                    "from_node": "sqrt1",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "x",
                },
                {
                    "from_node": "sqrt2",
                    "from_socket": "Result",
                    "to_node": "add1",
                    "to_socket": "y",
                },
            ],
        }
        return ntdata
