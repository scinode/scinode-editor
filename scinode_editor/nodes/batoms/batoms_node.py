import bpy
from scinode_editor.nodes.base_node import BaseNode

class Batoms(BaseNode):
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
        self.outputs.new("ASEAtoms", "Atoms")
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

    def pre_save(self):
        """Load Batoms into database."""
        from scinode.database.client import scinodedb
        from scinode.utils.db import replace_one
        from scinode.utils.node import get_executor
        from batoms import Batoms
        batoms = Batoms(self.batoms)
        atoms = batoms.as_ase()
        outputs = self.output_sockets_to_dict()
        species = atoms.arrays['species'] if "species" in atoms.arrays else atoms.get_chemical_symbols()
        results = ({"name": "Structure", "value": atoms},
                    {"name": "Elements", "value": atoms.get_chemical_symbols()},
                    {"name": "Species", "value": species},
                    {"name": "Positions", "value": atoms.positions},
        )
        for i in range(len(outputs)):
            Executor, executor_type = get_executor(outputs[i]["serialize"])
            outputs[i]["value"] = Executor(results[i]["value"])
            replace_one(outputs[i], scinodedb["data"])

    def pre_load(self, ndata):
        """Load structure to Blender

        Args:
            ndata (_type_): _description_
        """
        from batoms import Batoms
        from scinode.database.client import scinodedb
        from scinode.utils.node import deserialize_item
        result = scinodedb["data"].find_one({"uuid":ndata["outputs"][0]["uuid"]})
        result = deserialize_item(result)
        atoms = result['value']
        print("result: ", result)
        properties = ndata["properties"]
        if self.batoms not in bpy.data.objects:
            batoms = Batoms(label=properties["batoms"]["value"], from_ase=atoms)


class ViewBatoms(BaseNode):
    bl_idname = 'ViewBatoms'
    bl_label = "ViewBatoms"

    label: bpy.props.StringProperty(
        name="label",
        description="label.",
        default="scinode",
    )

    properties = []

    def init(self, context):
        self.inputs.new("ASEAtoms", "Atoms")

    def get_executor(self):
        return {"path": "scinode.executors.built_in",
                "name": "PropertyToSocket",
                "type": 'class',
                }

    def draw_buttons(self, context, layout):
        layout.prop(self, "label", text="label")

    def update_state(self):
        """Update the batoms in the 3DView.
        """
        from batoms import Batoms
        inputs = self.get_input_parameters_from_db()
        print(inputs)
        atoms = inputs['Atoms']['value']
        if self.label in bpy.data.collections:
            bpy.ops.batoms.delete(label=self.label)
        Batoms(label=self.label, from_ase=atoms)



class BatomsScaleCell(BaseNode):
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
