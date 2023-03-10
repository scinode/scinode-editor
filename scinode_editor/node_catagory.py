from nodeitems_utils import NodeCategory, NodeItem


class ScinodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ScinodeTree'


node_categories = [
    # identifier, label, items list
    ScinodeCategory('Input', "Input", items=[
        NodeItem("Integer", label="Integer", settings={}),
        NodeItem("Float", label="Float", settings={}),
        NodeItem("String", label="String", settings={}),
        NodeItem("Bool", label="Bool", settings={}),
        NodeItem("Batoms", label="Batoms", settings={}),
    ]),
    ScinodeCategory('ASE', "ASE", items=[
        NodeItem("ASEAtoms", label="Atoms", settings={}),
        NodeItem("ASEBulk", label="Bulk", settings={}),
        NodeItem("ASEMolecule", label="Molecule", settings={}),
        NodeItem("ASESurface", label="Surface", settings={}),
        NodeItem("ASEAdsorption", label="Adsorption", settings={}),
        NodeItem("ASECellTransformatoin", label="Transform", settings={}),
        NodeItem("ASEReplaceAtoms", label="Replace", settings={}),
        NodeItem("ASEDeleteAtoms", label="Delete", settings={}),
        NodeItem("ASEFixAtoms", label="FixAtoms", settings={}),
        NodeItem("ASEAtomsAttribute", label="AtomsAttribute", settings={}),
        NodeItem("ASEEOS", label="EOS", settings={}),
    ]),
    ScinodeCategory('DFT', "DFT", items=[
        NodeItem("DFTKpoints", label="Kpoints", settings={}),
    ]),
    ScinodeCategory('Test', "Test", items=[
        NodeItem("TestAdd", label="Add", settings={}),
        NodeItem("TestFloat", label="Float", settings={}),
        NodeItem("TestLess", label="Less", settings={}),
        NodeItem("TestGreater", label="Greater", settings={}),
        NodeItem("TestRange", label="Range", settings={}),
    ]),
    ScinodeCategory("QE", "QE", items=[
        NodeItem("QEPWParameter", label="PWParameter", settings={}),
        NodeItem("QEDosParameter", label="DosParameter", settings={}),
        NodeItem("QEProjwfcParameter", label="ProjwfcParameter", settings={}),
        NodeItem("QEPseudo_SSSP", label="Pseudo_SSSP", settings={}),
        NodeItem("QEPW", label="PW", settings={}),
        NodeItem("QEDos", label="Dos", settings={}),
        NodeItem("QEProjwfc", label="Projwfc", settings={}),
    ]),
    ScinodeCategory('Utils', "Utils", items=[
        NodeItem("Getattr", label="Getattr", settings={}),
        NodeItem("Setattr", label="Setattr", settings={}),
        NodeItem("Getitem", label="Getitem", settings={}),
        NodeItem("Setitem", label="Setitem", settings={}),
        NodeItem("Input_to_Output", label="Input to Output", settings={}),
        NodeItem("ViewBatoms", label="ViewBatoms", settings={}),
        NodeItem("Print", label="Print", settings={}),
    ]),
    ScinodeCategory('Math', "Math", items=[
        NodeItem("ScinodePythonMath", label="Math", settings={}),
        NodeItem("ScinodeNumpy", label="Numpy", settings={}),
    ]),
    ScinodeCategory('Vector', "Vector", items=[
        NodeItem("ScinodeVector3DMath", label="Vector3D", settings={}),
    ]),
    ScinodeCategory('Control', "Control", items=[
        NodeItem("ScinodeScatter", label="Scatter", settings={}),
        NodeItem("ScinodeSwitch", label="Switch", settings={}),
        NodeItem("ScinodeUpdate", label="Update", settings={}),
    ]),
]
