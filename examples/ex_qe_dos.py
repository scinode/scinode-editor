import bpy
import numpy as np
import time
import pickle
import os
from pathlib import Path
home = str(Path.home())
bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
nt = bpy.data.node_groups.new(name='pw_dos', type='ScinodeTree')
pw = nt.nodes.new(type='QEPW')
pw.directory = os.path.join(home, 'batoms/scinode/al')
structure = nt.nodes.new(type='Structure')
structure.structure = 'Al'
parameter = nt.nodes.new(type='QEPWParameter')
pseudo = nt.nodes.new(type='QEPseudo')
kpoint = nt.nodes.new(type='DFTKpoint')
# plot
plt = nt.nodes.new(type='MatplotlibPyplot')
plt.marker = 'o'
debug = nt.nodes.new(type='Print')
nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
nt.links.new(structure.outputs['Structure'], pw.inputs['Structure'])
nt.links.new(pw.outputs['Energy'], debug.inputs['Input'])
# dos
dos = nt.nodes.new('QEDos')
dos.directory = os.path.join(home, 'batoms/scinode/al')
dos.prefix = 'al'
parameter_dos = nt.nodes.new('QEDosParameter')
debug_dos = nt.nodes.new("Print")
nt.links.new(pw.outputs['Calculator'], dos.inputs['Calculator'])
nt.links.new(parameter_dos.outputs['Parameter'], dos.inputs['Parameter'])
nt.links.new(dos.outputs['Energies'], plt.inputs['x'])
nt.links.new(dos.outputs['Dos'], plt.inputs['y'])
nt.links.new(plt.outputs['Result'], debug_dos.inputs['Input'])
# projwfc
projwfc = nt.nodes.new('QEProjwfc')
projwfc.directory = os.path.join(home, 'batoms/scinode/al')
projwfc.prefix = 'al'
parameter_projwfc = nt.nodes.new('QEProjwfcParameter')
debug_projwfc = nt.nodes.new("Print")
nt.links.new(pw.outputs['Calculator'], projwfc.inputs['Calculator'])
nt.links.new(parameter_projwfc.outputs['Parameter'], projwfc.inputs['Parameter'])
nt.links.new(projwfc.outputs['Pdos'], debug_projwfc.inputs['Input'])
#
nt.launch()
# time.sleep(60)
# outputs = pickle.loads(pw.dbdata.get('outputs'))
# energy = outputs[1]['value']
# # assert np.isclose(energy, -534.1679643486145)
# outputs = pickle.loads(dos.dbdata.get('outputs'))
# dos = outputs[1]['value']
# print(dos)
# outputs = pickle.loads(projwfc.dbdata.get('outputs'))
# projwfc = outputs[1]['value']
# print(projwfc)
