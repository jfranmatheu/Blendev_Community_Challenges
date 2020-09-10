from bpy.types import Operator, SpaceView3D
import bpy
import gpu
from gpu_extras.batch import batch_for_shader


indices = ((0, 1, 2), (2, 1, 3))

shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

def get_vertices(pos, size):
    x, y = pos
    w, h = size
    return (
        (x, y),
        (x + w, y),
        (x, y + h),
        (x + w, y + h)
    )

def draw_callback(self, context):
    batch = batch_for_shader(shader, 'TRIS', {"pos": get_vertices(self.pos, self.size)}, indices=indices)
    shader.bind()
    shader.uniform_float("color", self.color)
    batch.draw(shader)


class SCULPT_OT_test_button(Operator):
    bl_idname = "sculpt.test_button"
    bl_label = "Test Button"

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def execute(self, context):
        self.pos = [10, 10]
        self.size = [200, 100]
        self.color = [0, 0, 0, 1]
        self.draw_handler = SpaceView3D.draw_handler_add(draw_callback, (self, context), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        context.area.tag_redraw()
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            if event.value == 'PRESS':
                SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
                return {'FINISHED'}
        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y
        width = context.region.width
        height = context.region.height
        x = mouse_x / width
        y = mouse_y / height
        self.color = [.5, x, y, 1]
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                if self.is_inside_button(mouse_x, mouse_y):
                    bpy.ops.object.voxel_remesh()
                    return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def is_inside_button(self, mx, my):
        x, y = self.pos
        w, h = self.size
        return mx >= x and my >= y and mx <= x + w and my <= y + h
