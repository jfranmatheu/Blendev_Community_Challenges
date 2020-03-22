from bpy.types import Panel

class MD_PT_metric_display(Panel):
    bl_label = "Metric Display"
    bl_category = 'View'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.operator('md.draw_metric', text="Draw Metric")