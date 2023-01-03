"""
Example: EOS of bulk Al

"""
import bpy
import numpy as np
import time
import pickle
import os
from pathlib import Path
home = str(Path.home())
# Create node tree
nt = bpy.data.node_groups.new(name='dft_qe_eos', type='ScinodeTree')
# Node pw and work directory
pw = nt.nodes.new(type='QEPW')
pw.directory = os.path.join(home, 'batoms/scinode/al')
# numpy node
np_node = nt.nodes.new(type='Numpy')
np_node.inputs['start'].default_value = 0.97
np_node.inputs['stop'].default_value = 1.03
np_node.inputs['num'].default_value = 7
# scale cell
scale_cell = nt.nodes.new(type='BatomsScaleCell')
# structure
bpy.ops.batoms.bulk_add(label = 'Al', formula = 'Al')
structure = nt.nodes.new(type='Structure')
structure.structure = 'Al'
#
parameter = nt.nodes.new(type='QEPWParameter')
pseudo = nt.nodes.new(type='QEPseudo')
kpoint = nt.nodes.new(type='DFTKpoint')
# plot
plt = nt.nodes.new(type='MatplotlibPyplot')
plt.marker = 'o'
debug = nt.nodes.new(type='Print')
# scale structure
nt.links.new(np_node.outputs['Result'], scale_cell.inputs['Scale'])
nt.links.new(structure.outputs['Structure'], scale_cell.inputs['Structure'])
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
