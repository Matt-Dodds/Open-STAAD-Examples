from comtypes import client
from comtypes import automation
import ctypes

# Helper functions to create safe array
def make_safe_array_double(size):
    return automation._midlSAFEARRAY(ctypes.c_double).create([0]*size)
def make_safe_array_int(size):
    return automation._midlSAFEARRAY(ctypes.c_int).create([0]*size)
def make_safe_array_long(size):
    return automation._midlSAFEARRAY(ctypes.c_long).create([0]*size)
def make_safe_array_string(size):
    return automation._midlSAFEARRAY(automation.BSTR).create([""]*size)
def make_variant_vt_ref(obj, var_type):
    var = automation.VARIANT()
    var._.c_void_p = ctypes.addressof(obj)
    var.vt = var_type | automation.VT_BYREF
    return var

# OpenSTAAD COM object
os = client.GetActiveObject("StaadPro.OpenSTAAD")
# Geometry class instance
geometry = os.geometry
# Group count
geometry._FlagAsMethod("GetGroupCount")
grouptype=2 #Member Type
group_count = geometry.GetGroupCount(grouptype)

group_names_safe_array = make_safe_array_string(group_count)
group_names = make_variant_vt_ref(group_names_safe_array, automation.VT_ARRAY | automation.VT_BSTR)

geometry._FlagAsMethod("GetGroupNames")
geometry.GetGroupNames(grouptype, group_names)

print("Member Group Count:",group_count)
print(group_names[0])
