from comtypes import automation
from comtypes import client
import ctypes
from comtypes import npsupport
import numpy as np
npsupport.enable()
os = client.GetActiveObject("StaadPro.OpenSTAAD")

def make_safe_array_double(size): 
    return automation._midlSAFEARRAY(ctypes.c_double).create([0]*size)
def make_safe_array_int(size): 
    return automation._midlSAFEARRAY(ctypes.c_int).create([0]*size)
def make_safe_array_long(size): 
    return automation._midlSAFEARRAY(ctypes.c_long).create([0]*size)
def make_variant_vt_ref(obj, var_type):
    var = automation.VARIANT()
    var._.c_void_p = ctypes.addressof(obj)
    var.vt = var_type | automation.VT_BYREF
    return var

geometry=os.Geometry
output = os.Output

groupname = "_MEMBER1"

geometry._FlagAsMethod("GetGroupEntityCount")
membcount=geometry.GetGroupEntityCount(groupname)

safe_array_beam_list = make_safe_array_long(membcount)
beams = make_variant_vt_ref(safe_array_beam_list, automation.VT_ARRAY | automation.VT_I4)

geometry._FlagAsMethod("GetGroupEntities")
geometry.GetGroupEntities(groupname,beams)

#For specific Member Group
print("For specific Member Group")
output._FlagAsMethod("GetMemberEndForces")
nEnd=0 #Start Node
LCase=1 #Load Case
LoctoGlb=0 #Local

safe_array_force= make_safe_array_double(6)
force = make_variant_vt_ref(safe_array_force, automation.VT_ARRAY | automation.VT_R8)
for i in range(4):
    output.GetMemberEndForces(beams[0][i], nEnd, LCase, force, LoctoGlb)
    print("Member End Force at Start node of Member ",beams[0][i], "is ",force[0])

nEnd=0 #End Node

safe_array_force = make_safe_array_double(6)
force = make_variant_vt_ref(safe_array_force, automation.VT_ARRAY | automation.VT_R8)
for i in range(4):
    output.GetMemberEndForces(beams[0][i], nEnd, LCase, force, LoctoGlb)
    print("Member End Force at End node of Member ",beams[0][i], "is ",force[0])

#For specific Member 
print("For Specific Member")
output._FlagAsMethod("GetMemberEndForces")
nEnd=0 #Start Node
LCase=1 #Load Case
LoctoGlb=0 #Local
beam=[21,22,23]

safe_array_force = make_safe_array_double(6)
force = make_variant_vt_ref(safe_array_force, automation.VT_ARRAY | automation.VT_R8)
for i in range(3):
    output.GetMemberEndForces(beam[i], nEnd, LCase, force, LoctoGlb)
    print("Member End Force at Start node of Member ",beam[i], "is ",force[0])

nEnd=1 #End Node
beam=[21,22,23]

safe_array_force = make_safe_array_double(6)
force = make_variant_vt_ref(safe_array_force, automation.VT_ARRAY | automation.VT_R8)
for i in range(3):
    output.GetMemberEndForces(beam[i], nEnd, LCase, force, LoctoGlb)
    print("Member End Force at End node of Member ",beam[i], "is ",force[0])