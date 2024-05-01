from comtypes import client
from comtypes import automation
import ctypes

def make_safe_array_long(size):
    return automation._midlSAFEARRAY(ctypes.c_long).create([0]*size)
def make_variant_vt_ref(obj, var_type):
    var = automation.VARIANT()
    var._.c_void_p = ctypes.addressof(obj)
    var.vt = var_type | automation.VT_BYREF
    return var

os = client.GetActiveObject("StaadPro.OpenSTAAD")
geometry = os.geometry

GroupName="_COLUMN1"

geometry._FlagAsMethod("GetGroupEntityCount")
GroupEntityCount=geometry.GetGroupEntityCount(GroupName)

group_entity_safe_array = make_safe_array_long(GroupEntityCount)
group_entity = make_variant_vt_ref(group_entity_safe_array, automation.VT_ARRAY | automation.VT_I4)

geometry._FlagAsMethod("GetGroupEntities")
geometry.GetGroupEntities(GroupName,group_entity)
print("Total Entity Count of Group",GroupName, "is",GroupEntityCount)
print("Group Entity IDs are",group_entity[0])
