
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
# single atoms
ir = Atoms('Ir')
iro = Atoms('IrO', positions = [[0, 0, 0], [1.9, 00, -0.1]])
iro2 = Atoms('IrO2', positions = [[0, 0, 0], [-1.9, 0, -0.1], [1.9, 0, -0.1]])
ir = Batoms("ir", from_ase=ir)
iro = Batoms("iro", from_ase=iro)
iro2 = Batoms("iro2", from_ase=iro2)
# intermediate
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
nt.links.new(surface.outputs['Structure'], constraint.inputs['Structure'])
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
nt.links.new(constraint.outputs['Structure'], pw0.inputs['Structure'])
nt.links.new(parameter.outputs['Parameter'], pw0.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw0.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw0.inputs['Kpoint'])
nt.links.new(scheduler.outputs['Scheduler'], pw0.inputs['Scheduler'])
#
analysis = nt.nodes.new(type='SurfaceAnalysis')
nt.links.new(pw0.outputs['Structure'], analysis.inputs['Surface'])
#
scatter1 = nt.nodes.new(type='BnodesScatter')
# structure
for species in ['Ir', 'IrO', 'IrO2']:
    sa = nt.nodes.new(type='BnodesStructure')
    sa.name = species
    sa.structure = species
    adsorption = nt.nodes.new(type='BuildAdsorption')
    nt.links.new(sa.outputs['Structure'], adsorption.inputs['Adsorbate'])
    nt.links.new(pw0.outputs['Structure'], adsorption.inputs['Surface'])
    nt.links.new(analysis.outputs['Ontop'], adsorption.inputs['Sites'])
    nt.links.new(analysis.outputs['Bridge'], adsorption.inputs['Sites'])
    nt.links.new(adsorption.outputs['Structure'], scatter1.inputs['Input'])
    #
pw1 = nt.nodes.new(type='QEPW')
pw1.directory = 'bnodes/oer/pt111-sa'
nt.links.new(scatter1.outputs['Result'], pw1.inputs['Structure'])
nt.links.new(parameter.outputs['Parameter'], pw1.inputs['Parameter'])
nt.links.new(pseudo.outputs['Pseudo'], pw1.inputs['Pseudo'])
nt.links.new(kpoint.outputs['Kpoint'], pw1.inputs['Kpoint'])
nt.links.new(scheduler.outputs['Scheduler'], pw1.inputs['Scheduler'])
#
# dos
# add queue
scheduler1 = nt.nodes.new(type='BnodesScheduler')
scheduler1.time = '23:59:00'
scheduler1.ntasks_per_node = 20
# scheduler1.qos = 'job_epyc2_debug'
scheduler1.config = '.xespresso-intel-2020b'
dos = nt.nodes.new('QEDos')
dos.directory = 'bnodes/oer/pt111-sa'
parameter_dos = nt.nodes.new('QEDosParameter')
debug_dos = nt.nodes.new("BnodesDebug")
nt.links.new(pw1.outputs['Calculator'], dos.inputs['Calculator'])
nt.links.new(parameter_dos.outputs['Parameter'], dos.inputs['Parameter'])
nt.links.new(scheduler1.outputs['Scheduler'], dos.inputs['Scheduler'])
nt.links.new(dos.outputs['Dos'], debug_dos.inputs['Input'])
# projwfc
projwfc = nt.nodes.new('QEProjwfc')
projwfc.directory = 'bnodes/oer/pt111-sa'
parameter_projwfc = nt.nodes.new('QEProjwfcParameter')
debug_projwfc = nt.nodes.new("BnodesDebug")
nt.links.new(pw1.outputs['Calculator'], projwfc.inputs['Calculator'])
nt.links.new(parameter_projwfc.outputs['Parameter'], projwfc.inputs['Parameter'])
nt.links.new(scheduler1.outputs['Scheduler'], projwfc.inputs['Scheduler'])
nt.links.new(projwfc.outputs['Pdos'], debug_projwfc.inputs['Input'])

# analysis1 = nt.nodes.new(type='SurfaceAnalysis')
# nt.links.new(pw1.outputs['Structure'], analysis1.inputs['Surface'])
# structure
# scatter2 = nt.nodes.new(type='BnodesScatter')
# for species in ['OH', 'O', 'OOH']:
#     intermediate = nt.nodes.new(type='BnodesStructure')
#     intermediate.name = species
#     intermediate.structure = species
#     debug = nt.nodes.new(type='BnodesDebug')
#     select = nt.nodes.new(type='BnodesSelect')
#     argmin = nt.nodes.new(type='BnodesNumpy')
#     argmin.function = 'argmin'
#     subtract = nt.nodes.new(type='BnodesNumpy')
#     subtract.function = 'subtract'
#     adsorption = nt.nodes.new(type='BuildAdsorption')
#     pw2 = nt.nodes.new(type='QEPW')
#     pw2.directory = 'bnodes/oer/{}'.format(species)
#     #
#     nt.links.new(intermediate.outputs['Structure'], adsorption.inputs['Adsorbate'])
#     nt.links.new(pw1.outputs['Structure'], adsorption.inputs['Surface'])
#     nt.links.new(analysis1.outputs['Ontop'], adsorption.inputs['Sites'])
#     nt.links.new(analysis1.outputs['Bridge'], adsorption.inputs['Sites'])
#     nt.links.new(adsorption.outputs['Structure'], pw2.inputs['Structure'])
#     nt.links.new(parameter.outputs['Parameter'], pw2.inputs['Parameter'])
#     nt.links.new(pseudo.outputs['Pseudo'], pw2.inputs['Pseudo'])
#     nt.links.new(kpoint.outputs['Kpoint'], pw2.inputs['Kpoint'])
#     nt.links.new(scheduler.outputs['Scheduler'], pw2.inputs['Scheduler'])
#     nt.links.new(pw2.outputs['Energy'], argmin.inputs['Input'])
#     nt.links.new(pw2.outputs['Energy'], select.inputs['Input'])
#     nt.links.new(argmin.outputs['Result'], select.inputs['Index'])
#     nt.links.new(select.outputs['Result'], subtract.inputs[0])
#     nt.links.new(pw0.outputs['Energy'], subtract.inputs[1])
#     nt.links.new(subtract.outputs['Result'], debug.inputs['Input'])
# nt.launch()
# nt.launch(daemon_name='ubelix')
# time.sleep(240)
# outputs = pickle.loads(debug.dbdata.get('outputs'))
# energy = outputs[1]['value']
# print("energy: ", energy)
