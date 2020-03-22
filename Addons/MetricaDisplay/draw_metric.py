from gpu.shader import from_builtin
from gpu_extras.batch import batch_for_shader
import bgl
import blf

shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR')


def rectangle_points(x, y, w, h):
    return (
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    )

# 2         # 3


# 0         # 1
rectangle_indices = (
        (0, 1, 2),
        (2, 1, 3)
    )

def Draw_2D_Rectangle(_posX, _posY, _width, _height, _color=(0, 0, 0, 0.3), _shader=shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'TRIS', {"pos": rectangle_points(_posX, _posY, _width, _height)}, indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND)

def Draw_Text(_posX, _posY, _text, _size, _r=1, _g=1, _b=1, _a=0.8):
    blf.color(0, _r, _g, _b, _a)
    blf.position(0, _posX, _posY, 0)
    blf.size(0, _size, 72)
    blf.draw(0, _text)

def draw(self, context):
    Draw_2D_Rectangle(0, 0, context.region.width, 80)
    Draw_Text(int(context.region.width/2), 30, self.metric, 16)