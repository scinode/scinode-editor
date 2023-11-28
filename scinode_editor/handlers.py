import bpy


def auto_update_nodetree_state():
    area = [area for area in bpy.context.screen.areas if area.type == "NODE_EDITOR"][0]
    with bpy.context.temp_override(area=area):
        bpy.ops.scinode.nodetree_update_state()
    return 1.0


def register():
    bpy.app.timers.register(auto_update_nodetree_state, persistent = True)

def unregister():
    if bpy.app.timers.is_registered(auto_update_nodetree_state):
        bpy.app.timers.unregister(auto_update_nodetree_state)
