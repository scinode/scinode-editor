
import bpy
from batoms import Batoms
from ase.atoms import Atoms
import numpy as np
import time
import pickle
# build structure
bpy.ops.batoms.delete()
bpy.ops.surface.fcc111_add(label='fcc111', symbol='Pt', size=(2, 2, 2))
bpy.ops.batoms.molecule_add(label='h2o', formula="H2O")
bpy.ops.batoms.molecule_add(label='h2', formula="H2")
h2o = Batoms("h2o")
h2o.cell = [10, 10, 10]
h2 = Batoms("h2")
h2.cell = [10, 10, 10]
OH = Atoms("OH", [[0, 0, 0], [0, 0, 1.0]])
O = Atoms("O", [[0, 0, 0]])
OOH = Atoms("OOH", [[0, 0, 0], [0, 0, 1.2], [0, 0, 2.2]])
OH = Batoms("OH", from_ase=OH)
O = Batoms("O", from_ase=O)
OOH = Batoms("OOH", from_ase=OOH)
# build workflow
nt = bpy.data.node_groups.new(name='oer_pt111', type='BnodesTree')
# surface
surface = nt.nodes.new(type='BnodesStructure')
surface.name = 'FCC111'
surface.structure = 'fcc111'
# fix atoms constraint
constraint = nt.nodes.new(type='AtomicConstraint')
constraint.method = 'distance'
constraint.distance=1.0
# parameter
parameter = nt.nodes.new(type='QEPWParameter')
parameter.calculation = 'relax'
pseudo = nt.nodes.new(type='QEPseudo')
kpoint = nt.nodes.new(type='DFTKpoint')
kpoint.size = (4, 4, 4)
# add queue
scheduler = nt.nodes.new(type='BnodesScheduler')
scheduler.time = '1:59:00'
scheduler.ntasks_per_node = 8
# scheduler.qos = 'job_epyc2_debug'
scheduler.config = '.xespresso-intel-2020b'
#
pw0 = nt.nodes.new(type='QEPW')
pw0.directory = 'bnodes/oer/pt111'
nt.links.new(surface.outputs['Structure'], constraint.inputs['Structure'])
nt.links.new(constraint.outputs['Structure'], pw0.inputs['Structure'])
nt.links.new(parameter.outputs['Parameter'], pw0.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw0.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw0.inputs['Kpoint'])
nt.links.new(scheduler.outputs['Scheduler'], pw0.inputs['Scheduler'])
#
analysis = nt.nodes.new(type='SurfaceAnalysis')
nt.links.new(pw0.outputs['Structure'], analysis.inputs['Surface'])
#
# structure
for species in ['OH', 'O', 'OOH']:
    intermediate = nt.nodes.new(type='BnodesStructure')
    intermediate.name = species
    intermediate.structure = species
    debug = nt.nodes.new(type='BnodesDebug')
    select = nt.nodes.new(type='BnodesSelect')
    argmin = nt.nodes.new(type='BnodesNumpy')
    argmin.function = 'argmin'
    subtract = nt.nodes.new(type='BnodesNumpy')
    subtract.function = 'subtract'
    adsorption = nt.nodes.new(type='BuildAdsorption')
    pw = nt.nodes.new(type='QEPW')
    pw.directory = 'bnodes/oer/{}'.format(species)
    #
    nt.links.new(intermediate.outputs['Structure'], adsorption.inputs['Adsorbate'])
    nt.links.new(pw0.outputs['Structure'], adsorption.inputs['Surface'])
    nt.links.new(analysis.outputs['Ontop'], adsorption.inputs['Sites'])
    nt.links.new(analysis.outputs['Bridge'], adsorption.inputs['Sites'])
    nt.links.new(adsorption.outputs['Structure'], pw.inputs['Structure'])
    nt.links.new(parameter.outputs['Parameter'], pw.inputs['Parameter'])
    nt.links.new(pseudo.outputs['Pseudo'], pw.inputs['Pseudo'])
    nt.links.new(kpoint.outputs['Kpoint'], pw.inputs['Kpoint'])
    nt.links.new(scheduler.outputs['Scheduler'], pw.inputs['Scheduler'])
    nt.links.new(pw.outputs['Energy'], argmin.inputs['Input'])
    nt.links.new(pw.outputs['Energy'], select.inputs['Input'])
    nt.links.new(argmin.outputs['Result'], select.inputs['Index'])
    nt.links.new(select.outputs['Result'], subtract.inputs[0])
    nt.links.new(pw0.outputs['Energy'], subtract.inputs[1])
    nt.links.new(subtract.outputs['Result'], debug.inputs['Input'])
nt.launch(daemon_name='ubelix')
# time.sleep(240)
# outputs = pickle.loads(debug.dbdata.get('outputs'))
# energy = outputs[1]['value']
# print("energy: ", energy)
