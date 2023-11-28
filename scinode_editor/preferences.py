"""
"""

import bpy
from bpy.types import AddonPreferences
from bpy.props import (
    BoolProperty,
    StringProperty,
    EnumProperty,
)
from scinode_editor.install.pip_dependencies import has_module
from scinode_editor.install import update
from scinode_editor.logger import update_logging_level
import logging

# logger = logging.getLogger('scinode_editor')
logger = logging.getLogger(__name__)


# Enum property.
# Note: the getter/setter callback must use integer identifiers!
logging_level_items = [
    ("DEBUG", "DEBUG", "", 0),
    ("INFO", "INFO", "", 1),
    ("WARNING", "WARNING", "", 2),
    ("ERROR", "ERROR", "", 3),
    ("CRITICAL", "CRITICAL", "", 4),
]

dependencies = {"scinode": "scinode",
                }


DEFAULT_GITHUB_ACCOUNT = "scinode"
DEFAULT_REPO_NAME = "scinode-editor"
DEFAULT_PLUGIN_NAME = "scinode-editor"


class ScinodeEditorDefaultPreference(bpy.types.Operator):
    """Update Scinode"""
    bl_idname = "scinode.use_scinode_editor_preference"
    bl_label = "Use defatul preference of Scinode"
    bl_description = "Use defatul preference of Scinode"

    def execute(self, context):
        import pathlib
        import os
        # theme
        bpy.context.preferences.themes[0].view_3d.space.gradients.background_type = "LINEAR"
        bpy.context.preferences.themes[0].view_3d.space.gradients.high_gradient = (0.9, 0.9, 0.9)
        bpy.context.preferences.themes[0].view_3d.space.gradients.gradient = (0.5, 0.5, 0.5)
        bpy.ops.wm.save_userpref()
        # logger
        bpy.context.preferences.addons['scinode_editor'].preferences.logging_level = "WARNING"
        self.report({"INFO"}, "Set default preferences successfully!")
        return {'FINISHED'}

class ScinodeEditorAddonPreferences(AddonPreferences):
    bl_idname = __package__

    def get_logging_level(self):
        items = self.bl_rna.properties["logging_level"].enum_items
        # self.get: returns the value of the custom property assigned to
        # key or default when not found
        return items[self.get("logging_level", 2)].value

    def set_logging_level(self, value):
        items = self.bl_rna.properties["logging_level"].enum_items
        item = items[value]
        level = item.identifier
        # we need to update both the preference and the logger
        self["logging_level"] = level
        # Set the logging level for all child loggers of "scinode-editor"
        update_logging_level()
        # Note the following logging info might not emit
        # if global level is higher than INFO
        logger.info("Set logging level to: {}".format(level))


    def scinode_editor_setting_path_update(self, context):
        import os
        if os.name == 'posix':  # Linux
            cmds = ["export", "SCINODE_EDITOR_SETTING_PATH={}".format(
                self.scinode_editor_setting_path)]
        if os.name == 'nt':  # Windows
            cmds = ["setx", "SCINODE_EDITOR_SETTING_PATH {}".format(
                self.scinode_editor_setting_path)]
        logger.debug(update.subprocess_run(cmds))

    scinode: BoolProperty(
        name="SciNode installed",
        description="SciNode package installed",
        default=False,
    )


    scinode_editor_setting_path: StringProperty(name="Custom Setting Path", description="Custom Setting Path",
                                            default="", subtype="FILE_PATH", update=scinode_editor_setting_path_update)

    logging_level: EnumProperty(
        name="Logging Level",
        items=logging_level_items,
        get=get_logging_level,
        set=set_logging_level,
        default=2,
        )

    def draw(self, context):

        layout = self.layout

        layout.label(text="Welcome to Scinode Editor!")
        # Check Blender version
        if bpy.app.version_string < '3.0.0':
            box = layout.box().column()
            box.label(text="Warning: Scinode Editor need Blender version > 3.0.0.")

        box = layout.box().column()
        row = box.row(align=True)
        row.operator("scinode_editor.update", icon="FILE_REFRESH")
        layout.label(text="Use default setting.")
        box = layout.box().column()
        row = box.row(align=True)
        row.operator("scinode_editor.use_scinode_editor_preference", text = "Use Preferences", icon="FILE_REFRESH")
        layout.separator()

        box = layout.box().column()
        box.label(text="Dependencies:")
        #
        for package, modname in dependencies.items():
            if not has_module(modname):
                op = box.operator("scinode_editor.pip_install_package",
                                     icon='IMPORT', text="Install {}".format(package))
                op.package = package
                op.modname = modname
            else:
                setattr(self, modname, True)
                box.prop(self, modname, text=package)
        # custom folder
        layout.separator()
        box = layout.box().column()
        box.label(text="Custom Settings")
        box.prop(self, "logging_level")
        box.prop(self, "scinode_editor_setting_path")


classes = [ScinodeEditorDefaultPreference,
           ScinodeEditorAddonPreferences,
           update.ScinodeEditorUpdateButton,
           ]


def register_class():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_class():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
