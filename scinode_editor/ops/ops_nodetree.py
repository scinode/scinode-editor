import bpy
from bpy.props import *
from bpy_extras.io_utils import ImportHelper, ExportHelper

class NodeTreeOperatorBase(bpy.types.Operator):

    @classmethod
    def poll(cls, context):
        if context.space_data.node_tree is not None:
            nodetree = context.space_data.node_tree
            return nodetree.bl_idname == "ScinodeTree"
        return False


class NodeTreeLaunch(NodeTreeOperatorBase):
    bl_idname = "scinode.nodetree_launch"
    bl_label = "Launch Scinode Tree"
    bl_description = "Launch all nodes in the tree"

    def execute(self, context):
        nodetree = context.space_data.node_tree
        nodetree.launch()
        self.report({"INFO"}, "Launch nodetree: {}".format(
            repr(nodetree.name)))
        return {"FINISHED"}


class NodeTreeUpdateState(NodeTreeOperatorBase):
    bl_idname = "scinode.nodetree_update_state"
    bl_label = "Update state of Scinode Tree"
    bl_description = "Update state of all nodes in the tree"

    def execute(self, context):
        nodetree = context.space_data.node_tree
        nodetree.update_state()
        self.report({"INFO"}, "Update state of nodetree: {}".format(
            repr(nodetree.name)))
        return {"FINISHED"}


class NodeTreeResetState(NodeTreeOperatorBase):
    bl_idname = "scinode.nodetree_reset"
    bl_label = "Reset state of Scinode Tree"
    bl_description = "Reset state of all nodes in the tree"

    def execute(self, context):
        nodetree = context.space_data.node_tree
        nodetree.reset()
        self.report({"INFO"}, "Reset state of nodetree: {}".format(
            repr(nodetree.name)))
        return {"FINISHED"}


class NodeTreeLoad(NodeTreeOperatorBase):
    bl_idname = "scinode.nodetree_load"
    bl_label = "Load NodeTree from database"
    bl_description = "Load a Scinode Tree from database"

    def execute(self, context):
        nodetree = context.space_data.node_tree
        nodetree.reset_state()
        self.report({"INFO"}, "Reset state of nodetree: {}".format(
            repr(nodetree.name)))
        return {"FINISHED"}


class EXPORT_OT_Nodetree(NodeTreeOperatorBase, ExportHelper):
    bl_idname = "scinode.nodetree_export"
    bl_label = "Export"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".py"

    def draw(self, context):

        layout = self.layout
        layout.label(text="Export to Python")

    def execute(self, context):
        from scinode.api.export_python_script import export_python_script
        nt = context.space_data.node_tree
        export_python_script(nt, filename=self.filepath)
        return {'FINISHED'}


def menu_func_export_batoms(self, context):
    lay = self.layout
    lay.operator(EXPORT_OT_Nodetree.bl_idname,
                 text="Python script file (.py)")
