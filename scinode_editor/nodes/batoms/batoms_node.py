import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode

class Batoms(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Batoms'
    bl_label = "Batoms"

    def get_batoms(self, context):
        obj_list = [
            obj for obj in bpy.data.objects if obj.batoms.type == 'BATOMS']
        structures = [('None', 'None', '', 0)]
        i = 1
        for obj in obj_list:
            structures.append((obj.name, obj.name, '', i))
            i += 1
        return structures

    batoms: bpy.props.EnumProperty(
        name="batoms",
        items=get_batoms,
        default=0,
        description="",
    )

    properties = ["batoms"]

    def init(self, context):
        self.outputs.new("ScinodeSocketGeneral", "Structure")
        self.outputs.new("ScinodeSocketGeneral", "Elements")
        self.outputs.new("ScinodeSocketGeneral", "Species")
        self.outputs.new("ScinodeSocketGeneral", "Positions")

    def draw_buttons(self, context, layout):
        layout.prop(self, "batoms", text="")

    def get_executor(self):
        return {"path": "scinode.executors.built_in",
                "name": "ResultToSocket",
                "type": "class",
                }

    def init_results(self):
        """Load Batoms into database."""
        from batoms import Batoms
        batoms = Batoms(self.batoms)
        atoms = batoms.as_ase()
        # check species
        species = atoms.arrays['species'] if "species" in atoms.arrays else atoms.get_chemical_symbols()
        results = ({"name": "Structure", "value": atoms},
                    {"name": "Elements", "value": atoms.get_chemical_symbols()},
                    {"name": "Species", "value": species},
                    {"name": "Positions", "value": atoms.positions},
        )
        return results

    def pre_load(self, ndata):
        """Load structure to Blender

        Args:
            ndata (_type_): _description_
        """
        import pickle
        from batoms import Batoms
        results = pickle.loads(ndata["results"])
        properties = pickle.loads(ndata["properties"])
        atoms = results[0]['value']
        if self.batoms not in bpy.data.objects:
            batoms = Batoms(label=properties["batoms"]["value"], from_ase=atoms)


class ViewBatoms(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'ViewBatoms'
    bl_label = "ViewBatoms"

    label: bpy.props.StringProperty(
        name="label",
        description="label.",
        default="scinode",
    )

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketGeneral", "Structure")

    def get_executor(self):
        return {"path": "scinode.executors.built_in",
                "name": "PropertyToSocket",
                "type": 'class',
                }

    def draw_buttons(self, context, layout):
        layout.prop(self, "label", text="label")

    def update_state(self):
        """Update the debug text.
        """
        from batoms import Batoms
        inputs = self.get_input_parameters_from_db()
        print(inputs)
        atoms = inputs['Structure']['value']
        if self.label in bpy.data.collections:
            bpy.ops.batoms.delete(label=self.label)
        batoms = Batoms(label=self.label, from_ase=atoms)



class BatomsScaleCell(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'BatomsScaleCell'
    bl_label = "Set Cell"

    properties = []

    def init(self, context):
        self.inputs.new("ScinodeSocketFloat", "Scale")
        self.inputs.new("ScinodeSocketGeneral", "Structure")
        self.outputs.new("ScinodeSocketGeneral", "Structure")

    def draw_buttons(self, context, layout):
        pass

    def get_executor(self):
        return {"path": "xnodes.executors.batoms.batoms_node",
                "name": "ScaleCell",
                "type": 'class',
                }
