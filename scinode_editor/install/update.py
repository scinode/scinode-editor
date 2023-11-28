"""
update scinode_editor
"""

import bpy
import subprocess
import os
import logging
# logger = logging.getLogger('scinode_editor')
logger = logging.getLogger(__name__)

account_name = "scinode"
repo_name = "scinode-editor"
DEFAULT_PLUGIN_NAME = "scinode-editor"

repo_git = f"https://github.com/{account_name}/{repo_name}.git"

def subprocess_run(cmds):
    try:
        p = subprocess.Popen(cmds,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
            return True
        else:
            logger.critical(stdout, stderr)
    except (OSError, Exception) as exception:
        logger.critical(exception)
        return False
    return False

def has_git():
    return subprocess_run(['git','--version'])

def gitclone(workdir=".", version="main", url=repo_git):
    """Make a git clone to the directory
    version can be a branch name or tag name
    """
    import shutil
    import pathlib
    scinode_editor_dir = os.path.dirname(pathlib.Path(__file__).parent.resolve())
    addon_dir = os.path.dirname(scinode_editor_dir)
    clone_into = os.path.join(addon_dir, repo_name)
    if os.path.exists(clone_into) and os.path.isdir(clone_into):
        shutil.rmtree(clone_into)
    commands = [
        "git",
        "clone",
        "--depth",
        "1",
        "-b",
        f"{version}",
        f"{url}",
        clone_into,
    ]
    flag = subprocess_run(commands)
    flag = True
    if flag:
        logger.info(f"Cloned repo into directory {clone_into}")
    else:
        logger.warning("Faild to clone")
    #
    src = os.path.join(clone_into, "scinode_editor")
    if os.path.exists(scinode_editor_dir) and os.path.isdir(scinode_editor_dir):
        logger.info("Remove old Scinode Editor folder {}".format(scinode_editor_dir))
        shutil.rmtree(scinode_editor_dir)
    logger.info("Move {} to {}".format(src, scinode_editor_dir))
    shutil.move(src, scinode_editor_dir)

class ScinodeEditorUpdateButton(bpy.types.Operator):
    """Update Scinode Editor"""
    bl_idname = "scinode.update"
    bl_label = "Update Scinode Editor"
    bl_description = "Update to the latest development version."

    def execute(self, context):
        if not has_git():
            self.report({"ERROR"}, "Please install Git first.")
            logger.warning("Please install Git first.")
            return {"CANCELLED"}
        gitclone()
        self.report({"INFO"}, "Update to the latest version successfully!")
        return {"FINISHED"}
