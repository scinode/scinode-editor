import bpy
from bpy.props import *


class NodeOperatorBase(bpy.types.Operator):

    @classmethod
    def poll(cls, context):
        if context.space_data.node_tree:
            nodetree = context.space_data.node_tree
            if nodetree.bl_idname == "ScinodeTree":
                return context.space_data.node_tree.nodes.active
        return False

class NodeUpdateState(NodeOperatorBase):
    bl_idname = "scinode.node_update_state"
    bl_label = "Update state of Scinode Tree"
    bl_description = "Update state of all nodes in the tree"

    def execute(self, context):
        node = context.space_data.node_tree.nodes.active
        node.update_state()
        self.report({"INFO"}, "Update state of node: {}".format(
            repr(node.name)))
        return {"FINISHED"}

class NodeReset(NodeOperatorBase):
    bl_idname = "scinode.node_reset"
    bl_label = "Reset node"
    bl_description = "Reset node"

    def execute(self, context):
        from scinode.orm.db_nodetree import DBNodeTree
        node = context.space_data.node_tree.nodes.active
        nt = DBNodeTree(uuid=node.id_data.uuid)
        nt.reset_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Reset node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodePause(NodeOperatorBase):
    bl_idname = "scinode.node_pause"
    bl_label = "Pause node"
    bl_description = "Pause node"

    def execute(self, context):
        from scinode.orm.db_nodetree import DBNodeTree
        node = context.space_data.node_tree.nodes.active
        nt = DBNodeTree(uuid=node.id_data.uuid)
        nt.pause_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Pause node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodePlay(NodeOperatorBase):
    bl_idname = "scinode.node_play"
    bl_label = "Play node"
    bl_description = "Play node"

    def execute(self, context):
        from scinode.orm.db_nodetree import DBNodeTree
        node = context.space_data.node_tree.nodes.active
        nt = DBNodeTree(uuid=node.id_data.uuid)
        nt.play_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Play node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodeCancel(NodeOperatorBase):
    bl_idname = "scinode.node_cancel"
    bl_label = "Cancel node"
    bl_description = "Cancel node"

    def execute(self, context):
        from scinode.orm.db_nodetree import DBNodeTree
        node = context.space_data.node_tree.nodes.active
        nt = DBNodeTree(uuid=node.id_data.uuid)
        nt.cancel_node(node.name)
        self.report({"INFO"}, "Cancel node: {}".format(repr(node.name)))
        return {"FINISHED"}
