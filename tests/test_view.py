import bpy
import time
import numpy as np


def test_view():
    from scinode_editor.api.view import BlenderView
    view = BlenderView()
    view.view(1)
