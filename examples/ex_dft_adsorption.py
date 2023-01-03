import bpy
import numpy as np
import time
import pickle
bpy.ops.batoms.delete()
bpy.ops.surface.fcc111_add(label='fcc111', symbol='Pt', size=(2, 2, 1))
bpy.ops.batoms.molecule_add(label='co', formula='CO')
nt = bpy.data.node_groups.new(name='adsorption', type='ScinodeTree')
surface = nt.nodes.new(type='Structure')
surface.structure = 'fcc111'
adsorbate = nt.nodes.new(type='Structure')
adsorbate.structure = 'co'
adsorption = nt.nodes.new(type='BuildAdsorption')
analysis = nt.nodes.new(type='SurfaceAnalysis')
pw = nt.nodes.new(type='QEPW')
pw.directory = 'scinode/adsorption'
parameter = nt.nodes.new(type='QEPWParameter')
parameter.calculation = 'relax'
pseudo = nt.nodes.new(type='QEPseudo')
kpoint = nt.nodes.new(type='DFTKpoint')
debug = nt.nodes.new(type='Print')
select = nt.nodes.new(type='Select')
numpy_node = nt.nodes.new(type='Numpy')
numpy_node.function = 'argmin'
#
nt.links.new(surface.outputs['Structure'], analysis.inputs['Surface'])
nt.links.new(adsorbate.outputs['Structure'], adsorption.inputs['Adsorbate'])
nt.links.new(surface.outputs['Structure'], adsorption.inputs['Surface'])
nt.links.new(analysis.outputs['Ontop'], adsorption.inputs['Sites'])
nt.links.new(analysis.outputs['Bridge'], adsorption.inputs['Sites'])
nt.links.new(adsorption.outputs['Structure'], pw.inputs['Structure'])
nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
nt.links.new(pw.outputs['Energy'], numpy_node.inputs['Input'])
nt.links.new(pw.outputs['Energy'], select.inputs['Input'])
nt.links.new(numpy_node.outputs['Result'], select.inputs['Index'])
nt.links.new(select.outputs['Result'], debug.inputs['Input'])
# add queue
scheduler = nt.nodes.new(type='Scheduler')
scheduler.time = '0:20:00'
scheduler.ntasks_per_node = 8
scheduler.qos = 'job_epyc2_debug'
scheduler.config = '.xespresso-intel-2020b'
nt.links.new(scheduler.outputs['Scheduler'], pw.inputs['Scheduler'])
nt.launch(daemon_name='ubelix')
time.sleep(240)
outputs = pickle.loads(debug.dbdata.get('outputs'))
energy = outputs[1]['value']
print("energy: ", energy)
