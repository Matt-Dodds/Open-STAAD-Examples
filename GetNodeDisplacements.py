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
load = os.load

#Node Count
geometry._FlagAsMethod("GetNodeCount")
nodeCount = geometry.GetNodeCount()

#Node List
print("Node List")
print("-------------------")
geometry._FlagAsMethod("GetNodeList")
safe_array_node_list = make_safe_array_long(nodeCount)
node = make_variant_vt_ref(safe_array_node_list, automation.VT_ARRAY | automation.VT_I4)
geometry.GetNodeList(node)
print(f"Node count: {nodeCount}")
print(node[0])

#LoadComb Case Count
geometry._FlagAsMethod("GetLoadCombinationCaseCount")
nLoadCombinationCase = load.GetLoadCombinationCaseCount

#LoadComb Case List
print("Load Combination List")
print("-------------------")
load._FlagAsMethod("GetLoadCombinationCaseNumbers")
safe_array_LCComb_list = make_safe_array_long(nLoadCombinationCase)
LCCases = make_variant_vt_ref(safe_array_LCComb_list, automation.VT_ARRAY | automation.VT_I4)
load.GetLoadCombinationCaseNumbers (LCCases)
print(f"Load Combination count: {nLoadCombinationCase}")
print(LCCases[0])

#Get Node Displacement
output._FlagAsMethod("GetNodeDisplacements")
safe_array_Disp= make_safe_array_double(6)
Disp = make_variant_vt_ref(safe_array_Disp, automation.VT_ARRAY | automation.VT_R8)

for i in range(nodeCount):
    for j in range(nLoadCombinationCase):
        output.GetNodeDisplacements (node[0][i], LCCases[0][j], Disp)
        print("For Node:", node[0][i]," For Load Case Combination:", LCCases[0][j], " Displacement is",Disp[0])