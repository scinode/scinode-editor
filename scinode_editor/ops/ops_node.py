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


class NodeReset(NodeOperatorBase):
    bl_idname = "scinode.node_reset"
    bl_label = "Reset node"
    bl_description = "Reset node"

    def execute(self, context):
        node = context.space_data.node_tree.nodes.active
        from scinode.engine.nodetree_engine import EngineNodeTree
        ent = EngineNodeTree(uuid=node.id_data.uuid)
        ent.reset_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Reset node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodePause(NodeOperatorBase):
    bl_idname = "scinode.node_pause"
    bl_label = "Pause node"
    bl_description = "Pause node"

    def execute(self, context):
        node = context.space_data.node_tree.nodes.active
        from scinode.engine.nodetree_engine import EngineNodeTree
        ent = EngineNodeTree(uuid=node.id_data.uuid)
        ent.pause_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Pause node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodePlay(NodeOperatorBase):
    bl_idname = "scinode.node_play"
    bl_label = "Play node"
    bl_description = "Play node"

    def execute(self, context):
        node = context.space_data.node_tree.nodes.active
        from scinode.engine.nodetree_engine import EngineNodeTree
        ent = EngineNodeTree(uuid=node.id_data.uuid)
        ent.play_node(node.name)
        bpy.ops.scinode.nodetree_update_state()
        self.report({"INFO"}, "Play node: {}".format(repr(node.name)))
        return {"FINISHED"}


class NodeCancel(NodeOperatorBase):
    bl_idname = "scinode.node_cancel"
    bl_label = "Cancel node"
    bl_description = "Cancel node"

    def execute(self, context):
        node = context.space_data.node_tree.nodes.active
        from scinode.engine.nodetree_engine import EngineNodeTree
        ent = EngineNodeTree(uuid=node.id_data.uuid)
        ent.cancel_node(node.name)
        self.report({"INFO"}, "Cancel node: {}".format(repr(node.name)))
        return {"FINISHED"}
