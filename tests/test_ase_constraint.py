import bpy
import time

def test_fix_atoms():
    nt = bpy.data.node_groups.new(name='test_fix_atoms', type='ScinodeTree')
    bulk1 = nt.nodes.new(type='ASEBulk')
    bulk1.inputs["name"].default_value = "Al"
    bulk1.inputs["cubic"].default_value = True
    #
    fix1 = nt.nodes.new("ASEFixAtoms")
    fix1.inputs["Index"].default_value = 1
    nt.links.new(bulk1.outputs[0], fix1.inputs[0])
    nt.launch()
    time.sleep(5)
    nt.update_state()
    results = fix1.get_results()
    print(results)
    atoms1 = results[0]["value"]
    assert len(atoms1.constraints) == 1
