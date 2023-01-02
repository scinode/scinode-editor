

import bpy
from scinode_editor.nodes.base_node import ScinodeTreeNode, update_sockets

func_items = [
    ("acos", "acos", "", 0),
    ("acosh", "acosh", "", 1),
    ("asin", "asin", "", 2),
    ("asinh", "asinh", "", 3),
    ("atan", "atan", "", 4),
    ("atan2", "atan2", "", 5),
    ("atanh", "atanh", "", 6),
    ("ceil", "ceil", "", 7),
    ("comb", "comb", "", 8),
    ("copysign", "copysign", "", 9),
    ("cos", "cos", "", 10),
    ("cosh", "cosh", "", 11),
    ("degrees", "degrees", "", 12),
    ("dist", "dist", "", 13),
    ("e", "e", "", 14),
    ("erf", "erf", "", 15),
    ("erfc", "erfc", "", 16),
    ("exp", "exp", "", 17),
    ("expm1", "expm1", "", 18),
    ("fabs", "fabs", "", 19),
    ("factorial", "factorial", "", 20),
    ("floor", "floor", "", 21),
    ("fmod", "fmod", "", 22),
    ("frexp", "frexp", "", 23),
    ("fsum", "fsum", "", 24),
    ("gamma", "gamma", "", 25),
    ("gcd", "gcd", "", 26),
    ("hypot", "hypot", "", 27),
    ("inf", "inf", "", 28),
    ("isclose", "isclose", "", 29),
    ("isfinite", "isfinite", "", 30),
    ("isinf", "isinf", "", 31),
    ("isnan", "isnan", "", 32),
    ("isqrt", "isqrt", "", 33),
    ("ldexp", "ldexp", "", 34),
    ("lgamma", "lgamma", "", 35),
    ("log", "log", "", 36),
    ("log10", "log10", "", 37),
    ("log1p", "log1p", "", 38),
    ("log2", "log2", "", 39),
    ("modf", "modf", "", 40),
    ("nan", "nan", "", 41),
    ("perm", "perm", "", 42),
    ("pi", "pi", "", 43),
    ("pow", "pow", "", 44),
    ("prod", "prod", "", 45),
    ("radians", "radians", "", 46),
    ("remainder", "remainder", "", 47),
    ("sin", "sin", "", 48),
    ("sinh", "sinh", "", 49),
    ("sqrt", "sqrt", "", 50),
    ("tan", "tan", "", 51),
    ("tanh", "tanh", "", 52),
    ("tau", "tau", "", 53),
    ("trunc", "trunc", "", 54),
]


class Math(bpy.types.Node, ScinodeTreeNode):
    bl_idname = 'Math'
    dtype = 'Math'
    bl_label = "Math"

    function: bpy.props.EnumProperty(
        name="function",
        description="function.",
        items=func_items,
        default='cos',
        update=update_sockets,
    )

    properties = ["function"]

    def init(self, context):
        if self.function in ['atan2', 'fmod', 'gcd', 'pow', 'remainder']:
            self.inputs.new("ScinodeSocketFloat", "x")
            self.inputs.new("ScinodeSocketFloat", "y")
            self.args = "x, y"
        elif self.function in ['comb', 'perm']:
            self.inputs.new("NodeSocketInt", "n")
            self.inputs.new("NodeSocketInt", "k")
            self.args = "n, k"
        elif self.function in ['dist']:
            self.inputs.new("ScinodeSocketFloat", "p")
            self.inputs.new("ScinodeSocketFloat", "q")
            self.args = "p, q"
        elif self.function in ['fsum']:
            self.inputs.new("ScinodeSocketFloat", "seq")
            self.args = "seq"
        elif self.function in ['isclose']:
            self.inputs.new("ScinodeSocketFloat", "a")
            self.inputs.new("ScinodeSocketFloat", "n")
            self.args = "a, n"
        elif self.function in ['isqrt']:
            self.inputs.new("NodeSocketInt", "n")
            self.args = "n"
        elif self.function in ['ldexp']:
            self.inputs.new("ScinodeSocketFloat", "x")
            self.inputs.new("NodeSocketInt", "i")
            self.args = "x, i"
        else:
            self.inputs.new("ScinodeSocketFloat", "x")
            self.args = "x"
        self.outputs.new("ScinodeSocketFloat", "Result")

    def draw_buttons(self, context, layout):
        layout.prop(self, "function", text="")

    def get_executor(self):
        return {"path": "math",
                "name": self.function,
                "type": "function",
                }
