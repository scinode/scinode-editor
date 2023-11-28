"""
View the nodetree by Blender
"""
from scinode.database.db import scinodedb


class BlenderView:
    """Class used to view nodetree by Blender"""

    def __init__(self) -> None:
        self.db = scinodedb

    def view(self, index):
        """View the nodetree with index

        Args:
            index (int): index of the nodetree to be viewed.
        """
        import bpy

        query = {"index": index}
        # build nodetree
        self.build_nodetree_from_db(query)
        # change view to node editor
        area = bpy.context.screen.areas[0]
        area.type = "NODE_EDITOR"
        area.ui_type = "ScinodeTree"
        area.spaces[0].node_tree = self.nt
        # self.arrange_node(area)
        self.full_screen(area)

    def full_screen(self, area):
        """Make the Node Editor full screen.

        Args:
            area (_type_): _description_
        """
        import bpy

        with bpy.context.temp_override(area=area):
            bpy.ops.screen.screen_full_area(use_hide_panels=False)

    def arrange_node(self, area):
        """Arrange nodes

        Args:
            area (_type_): _description_
        """
        import bpy

        with bpy.context.temp_override(area=area):
            bpy.ops.node.button()

    def query_node(self, uuid):
        """Query node by uuid

        Args:
            uuid (str): uuid of the node

        Returns:
            dict: data of the node
        """
        query = {"uuid": uuid}
        ndata = self.db["node"].find_one(query)
        return ndata

    def build_nodetree_from_db(self, query):
        """Recreate the nodetree from database
        """
        from scinode_editor.node_tree import ScinodeTree
        ntdata = self.db["nodetree"].find_one(query, {"uuid": 1, "metadata.platform":1})
        if ntdata["metadata"]["platform"].upper() == "BLENDER":
            nt = ScinodeTree.load_from_db(ntdata["uuid"])
            self.nt = nt
        else:
            raise Exception("This nodetree is not created by Blender")
