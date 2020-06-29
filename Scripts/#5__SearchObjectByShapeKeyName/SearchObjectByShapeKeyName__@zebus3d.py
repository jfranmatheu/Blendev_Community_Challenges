import bpy

def get_object_with_shapekey(sk_target):
    for ob in bpy.data.objects:
        if hasattr(ob.data, 'shape_keys'):
            sk = ob.data.shape_keys
            if sk_target in sk.key_blocks:
                return ob
        
sk_target = 'target' # nombre del shapekey
obj_with_sk = get_object_with_shapekey(sk_target)
print(obj_with_sk.name)