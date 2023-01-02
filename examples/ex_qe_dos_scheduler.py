import bpy
import numpy as np
import time
import pickle
import os
from pathlib import Path
home = "/storage/homefs/xw20n572"
bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
nt = bpy.data.node_groups.new(name='pw_remote', type='BnodesTree')
pw = nt.nodes.new(type='QEPW')
pw.directory = os.path.join(home, 'batoms/bnodes/al')
structure = nt.nodes.new(type='BnodesStructure')
structure.structure = 'Al'
parameter = nt.nodes.new(type='QEPWParameter')
pseudo = nt.nodes.new(type='QEPseudo')
kpoint = nt.nodes.new(type='DFTKpoint')
scheduler = nt.nodes.new(type='BnodesScheduler')
scheduler.time = '0:09:00'
scheduler.ntasks_per_node = 1
scheduler.qos = 'job_epyc2_debug'
scheduler.config = '.xespresso-intel-2020b'
debug = nt.nodes.new(type='BnodesDebug')
nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
nt.links.new(scheduler.outputs['Scheduler'], pw.inputs['Scheduler'])
nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
nt.links.new(pw.outputs['Energy'], debug.inputs['Input'])
# dos
dos = nt.nodes.new('QEDos')
dos.directory = os.path.join(home, 'batoms/bnodes/al')
dos.prefix = 'al'
parameter_dos = nt.nodes.new('QEDosParameter')
debug_dos = nt.nodes.new("BnodesDebug")
nt.links.new(pw.outputs['Calculator'], dos.inputs['Calculator'])
nt.links.new(parameter_dos.outputs['Parameter'], dos.inputs['Parameter'])
nt.links.new(scheduler.outputs['Scheduler'], dos.inputs['Scheduler'])
nt.links.new(dos.outputs['Dos'], debug_dos.inputs['Input'])
# projwfc
projwfc = nt.nodes.new('QEProjwfc')
projwfc.directory = os.path.join(home, 'batoms/bnodes/al')
projwfc.prefix = 'al'
parameter_projwfc = nt.nodes.new('QEProjwfcParameter')
debug_projwfc = nt.nodes.new("BnodesDebug")
nt.links.new(pw.outputs['Calculator'], projwfc.inputs['Calculator'])
nt.links.new(parameter_projwfc.outputs['Parameter'], projwfc.inputs['Parameter'])
nt.links.new(scheduler.outputs['Scheduler'], projwfc.inputs['Scheduler'])
nt.links.new(projwfc.outputs['Pdos'], debug_projwfc.inputs['Input'])
#
nt.launch()
# nt.launch(computer='ubelix')
time.sleep(120)
outputs = pickle.loads(pw.dbdata.get('outputs'))
energy = outputs[1]['value']
# assert np.isclose(energy, -534.1679643486145)
outputs = pickle.loads(dos.dbdata.get('outputs'))
dos = outputs[1]['value']
print(dos)
outputs = pickle.loads(projwfc.dbdata.get('outputs'))
projwfc = outputs[1]['value']
print(projwfc)
