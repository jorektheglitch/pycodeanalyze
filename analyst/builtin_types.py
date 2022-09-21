from .analytics import Class, Module


type_type = Class(None, [])
type_type.type = type_type
bool_type = Class(type_type, [])
int_type = Class(type_type, [])
module_type = Class(type_type, [])

builtins = Module(None, None, [], {
    "bool": bool_type,
    "int": int_type
})
