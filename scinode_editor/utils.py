import logging
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def type_bl_to_python(data):
    if 'bpy_prop_array' in str(type(data)):
        data =list(data)
    return data

def type_python_to_bl(data):
    import numpy as np

    if "numpy.int" in str(type(data)):
        data = int(data)
    if "numpy.float" in str(type(data)):
        data = float(data)
    if "numpy.ndarray" in str(type(data)):
        data = data.tolist()

    return data


def generate_enum(items):
    i = 0
    for item in items:
        print("""  "{}", "{}", "", {} """.format(item, item, i))
        i += 1
