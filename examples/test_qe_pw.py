import bpy
import pytest
import time


def test_pw_local():
    import numpy as np
    import time
    import pickle
    bpy.ops.batoms.delete()
    bpy.ops.batoms.bulk_add(label='Al', formula='Al')
    nt = bpy.data.node_groups.new(name='pw_local', type='ScinodeTree')
    pw = nt.nodes.new(type='QEPW')
    pw.directory = 'scinode/al'
    structure = nt.nodes.new(type='Structure')
    structure.structure = 'Al'
    parameter = nt.nodes.new(type='QEPWParameter')
    pseudo = nt.nodes.new(type='QEPseudo')
    kpoint = nt.nodes.new(type='DFTKpoint')
    debug = nt.nodes.new(type='Print')
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
    nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
    nt.links.new(pw.outputs['Energy'], debug.inputs['Input'])
    nt.launch()
    time.sleep(60)
    outputs = pickle.loads(pw.dbdata.get('outputs'))
    energy = outputs[1]['value']
    assert np.isclose(energy, -534.16, atol = 1e-1)


def test_pw_remote():
    import numpy as np
    import time
    import pickle
    bpy.ops.batoms.delete()
    bpy.ops.batoms.bulk_add(label='Al', formula='Al')
    nt = bpy.data.node_groups.new(name='pw_remote', type='ScinodeTree')
    pw = nt.nodes.new(type='QEPW')
    pw.directory = 'scinode/al'
    structure = nt.nodes.new(type='Structure')
    structure.structure = 'Al'
    parameter = nt.nodes.new(type='QEPWParameter')
    pseudo = nt.nodes.new(type='QEPseudo')
    kpoint = nt.nodes.new(type='DFTKpoint')
    kpoint.size = (4, 4, 4)
    scheduler = nt.nodes.new(type='Scheduler')
    scheduler.time = '0:09:00'
    scheduler.ntasks_per_node = 1
    scheduler.qos = 'job_epyc2_debug'
    scheduler.config = '.xespresso-intel-2020b'
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
    nt.links.new(scheduler.outputs['Scheduler'], pw.inputs['Scheduler'])
    nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
    nt.launch(daemon_name='ubelix')
    time.sleep(90)
    outputs = pickle.loads(pw.dbdata.get('outputs'))
    energy = outputs[1]['value']
    # assert np.isclose(energy, -534.1679643486145)


def test_pw_vector():
    import numpy as np
    import time
    import pickle
    import os
    bpy.ops.batoms.delete()
    bpy.ops.batoms.bulk_add(label='Al', formula='Al')
    nt = bpy.data.node_groups.new(name='pw_vector', type='ScinodeTree')
    pw = nt.nodes.new(type='QEPW')
    pw.directory = 'scinode/al'
    # numpy node
    np_node = nt.nodes.new(type='Numpy')
    np_node.inputs['start'].default_value = 0.97
    np_node.inputs['stop'].default_value = 1.03
    np_node.inputs['num'].default_value = 7
    # scale cell
    scale_cell = nt.nodes.new(type='BatomsScaleCell')
    structure = nt.nodes.new(type='Structure')
    structure.structure = 'Al'
    parameter = nt.nodes.new(type='QEPWParameter')
    pseudo = nt.nodes.new(type='QEPseudo')
    kpoint = nt.nodes.new(type='DFTKpoint')
    # plot
    plt = nt.nodes.new(type='MatplotlibPyplot')
    plt.marker = 'o'
    debug = nt.nodes.new(type='Print')
    # scale structure
    nt.links.new(np_node.outputs['Result'], scale_cell.inputs['Scale'])
    nt.links.new(structure.outputs['Structure'],
                 scale_cell.inputs['Structure'])
    nt.links.new(scale_cell.outputs['Structure'], pw.inputs['Structure'])
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
    nt.links.new(np_node.outputs['Result'], plt.inputs['x'])
    nt.links.new(pw.outputs['Energy'], plt.inputs['y'])
    nt.links.new(plt.outputs['Result'], debug.inputs['Input'])
    nt.launch()
    time.sleep(60)
    outputs = pickle.loads(pw.dbdata.get('outputs'))
    energy = outputs[1]['value']
    assert len(energy) == 7
