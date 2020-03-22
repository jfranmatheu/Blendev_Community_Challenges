from bpy.types import Operator, SpaceView3D
from . draw_metric import draw
handlers = []

base = '1'
metric_list = {
    "0.001" :   'Milímetros',
    "0.01" :   'Centímetros',
    "0.1" :   'Decímetros',
    "1" :   'Metros',
    "10" :   'Decámetros',
    "100" :   'Hectámetros',
    "1000" :   'Kilómetros',
}

class MD_OT_draw_metric(Operator):
    bl_idname = "md.draw_metric"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def modal(self, context, event):
        if event.type == 'ESC':
            if hasattr(self, "_handle"):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            return {'FINISHED'}
        dim = self.obj.dimensions
        dim = max(dim[0], max(dim[1], dim[2]))
        if self.obj == context.active_object and self.dim == dim or context.active_object.type != 'MESH':
            return {'PASS_THROUGH'}
        self.obj = context.active_object
        self.objName = self.obj.name
        self.dim = dim
        for key, item in metric_list.items():
            div = float(key) / self.dim
            if div > 0.1 and div < 1: # 0.1
                print(key + " -> " + str(div) " -> " + str(self.dim))
                self.metric = metric_list[key]
                break
        return {'PASS_THROUGH'}

    def execute(self, context):
        
        self.obj = context.active_object
        self.metric = 'Metros'
        self.objName = self.obj.name
        self.dim = 0
        context.window_manager.modal_handler_add(self)
        args = (self, context)
        self._handle = SpaceView3D.draw_handler_add(draw, args, 'WINDOW', 'POST_PIXEL')
        #handlers.append(self._handle)
        return {'RUNNING_MODAL'}