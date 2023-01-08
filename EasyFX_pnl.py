import bpy

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


class EASYFX_PT_UpdatePanel(bpy.types.Panel):
    bl_category = "EasyFX"
    bl_label = "Update"
    bl_idname = "EASYFX_PT_Update"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator('object.update_render_operator',
                     text="Update & re-Render", icon="RENDER_STILL")
        row = col.row(align=True)
        row.operator('object.update_operator',
                     text="Update", icon="SEQ_CHROMA_SCOPE")
# COLOR IMAGE_COL PARTICLES RENDERLAYERS CAMERA_STEREO MOD_PARTICLES SEQ_CHROMA_SCOPE
        scn = context.scene
        mytool = scn.easyfx
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "use_auto_update", text="Auto Update")
        row.prop(mytool, "use_flip", text="Flip image")
        layout.prop(mytool, "split_image", text="Split with original")
        if mytool.split_image == True:
            layout.prop(mytool, "split_v", text="Split at")


class EASYFX_PT_FilterPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Filter"
    bl_idname = "EASYFX_PT_Filter"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        # get the scene
        scn = context.scene
        mytool = scn.easyfx

        # display the property
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "use_glow", text="Glow")
        if mytool.use_glow == True:
            row = col.row(align=True)
            row.prop(mytool, "glow_em", text="Emission only (Cycles only)")
            row = col.row(align=True)
            row.prop(mytool, "glow_v", text="Threshold")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "use_streaks", text="Streaks")
        if mytool.use_streaks == True:
            row = col.row(align=True)
            row.prop(mytool, "streaks_em", text="Emission only (Cycles only)")
            row = col.row(align=True)
            row.prop(mytool, "streaks_v", text="Threshold")
            row = col.row(align=True)
            row.prop(mytool, "streaks_n", text="Streaks")
            row = col.row(align=True)
            row.prop(mytool, "streaks_d", text="Angle offset")
        layout.prop(mytool, "use_vignette", text="Vignette")
        if mytool.use_vignette == True:
            layout.prop(mytool, "vignette_v", text="Amount")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "sharpen_v", text="Sharpen")
        row = col.row(align=True)
        row.prop(mytool, "soften_v", text="Soften")


class EASYFX_PT_BlurPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Blur"
    bl_idname = "EASYFX_PT_Blur"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        mytool = scn.easyfx
        layout = self.layout
        layout.prop(mytool, "use_dof", text="Depth of field")
        if mytool.use_dof == True:
            layout.prop(mytool, "dof_v", text="F-stop")
            layout.label(text="Focal point can be set in Camera Properties")
        layout.prop(mytool, "use_speedb", text="Motion blur (Cycles only)")
        if mytool.use_speedb == True:
            layout.prop(mytool, "motionb_v", text="Amount")


class EASYFX_PT_ColorPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Color"
    bl_idname = "EASYFX_PT_Color"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        mytool = scn.easyfx
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "brightness_v", text="Brightness")
        row = col.row(align=True)
        row.prop(mytool, "contrast_v", text="Contrast")
        row = col.row(align=True)
        row.prop(mytool, "bw_v", text="Saturation")
        layout.prop(mytool, "shadows_v", text="Shadows")
        layout.prop(mytool, "midtones_v", text="Midtones")
        layout.prop(mytool, "highlights_v", text="Hightlights")


class EASYFX_PT_LensPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Lens"
    bl_idname = "EASYFX_PT_Lens"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        mytool = scn.easyfx
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "lens_distort_v", text="Lens distortion")
        row = col.row(align=True)
        row.prop(mytool, "dispersion_v", text="Chromatic aberration")
        layout.prop(mytool, "use_flare", text="Lens Flare")
        if mytool.use_flare == True:
            layout.prop(mytool, "flare_type", text="Position")
            if mytool.flare_type == 'Fixed':
                col = layout.column(align=True)
                row = col.row(align=True)
                row.prop(mytool, "flare_x", text="X")
                row.prop(mytool, "flare_y", text="Y")
                row = col.row(align=True)
                row.prop(mytool, "flare_center_size", text="Source Size")
                row = col.row(align=True)
                row.prop(mytool, "flare_c", text="")
                col = layout.column(align=True)
                row = col.row(align=True)
                row.prop(mytool, "flare_streak_intensity",
                         text='Streak Intensity')
                row = col.row(align=True)
                row.prop(mytool, "flare_streak_lenght", text="Streak Lenght")
                row = col.row(align=True)
                row.prop(mytool, "flare_streak_angle", text="Rotation")
                row.prop(mytool, "flare_streak_streaks", text="Streaks")
                row = col.row(align=True)
                row.prop(mytool, "flare_glow", text="Glow")
                row = col.row(align=True)
                row.prop(mytool, "flare_ghost", text="Ghost")
            else:
                layout.prop(mytool, "flare_layer", text="")
                col = layout.column(align=True)
                row = col.row(align=True)
                row.prop(mytool, "flaret_streak_intensity",
                         text='Streak Intensity')
                row = col.row(align=True)
                row.prop(mytool, "flaret_streak_lenght", text="Streak Lenght")
                row = col.row(align=True)
                row.prop(mytool, "flaret_streak_angle", text="Rotation")
                row.prop(mytool, "flaret_streak_streaks", text="Streaks")
                row = col.row(align=True)
                row.prop(mytool, "flaret_glow", text="Glow")
                row = col.row(align=True)
                row.prop(mytool, "flaret_ghost", text="Ghost")
            # if mytool.flare_type == 'Tracked':
            #    layout.prop(mytool, "flare_layer", text="")


class EASYFX_PT_WorldPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "World"
    bl_idname = "EASYFX_PT_World"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        mytool = scn.easyfx
        layout = self.layout
        layout.prop(mytool, "use_mist", text="Mist")
        if mytool.use_mist == True:
            col = layout.column(align=True)
            if bpy.context.scene.render.engine != 'CYCLES':
                row = col.row(align=True)
                row.prop(mytool, "mist_sky", text="Affect sky")
            row = col.row(align=True)
            row.prop(mytool, "mist_offset", text="Offset")
            row = col.row(align=True)
            row.prop(mytool, "mist_size", text="Size")
            row = col.row(align=True)
            row.prop(mytool, "mist_min", text="Min")
            # row = col.row(align = True)
            row.prop(mytool, "mist_max", text="Max")
            row = col.row(align=True)
            row.prop(mytool, "mist_color", text="")
        layout.prop(mytool, "use_transparent_sky", text="Transparent sky")
        layout.prop(mytool, "use_image_sky", text="Image sky")
        if mytool.use_image_sky == True:
            layout.prop(mytool, "image_sky_img", text="")
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(mytool, "image_sky_x", text="X")
            row.prop(mytool, "image_sky_y", text="Y")
            row = col.row(align=True)
            row.prop(mytool, "image_sky_angle", text="Rotation")
            row = col.row(align=True)
            row.prop(mytool, "image_sky_scale", text="Scale")


class EASYFX_PT_StylePanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Style"
    bl_idname = "EASYFX_PT_Style"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        mytool = scn.easyfx
        layout = self.layout
        layout.prop(mytool, "use_cel_shading", text="Cel shading")
        if mytool.use_cel_shading == True:
            layout.prop(mytool, "cel_thickness", text="Line thickness")
        layout.prop(mytool, "use_cinematic_border", text="Cinematic borders")
        if mytool.use_cinematic_border == True:
            layout.prop(mytool, "cinematic_border_v", text="Border height")


class EASYFX_PT_SettingPanel(Panel):
    bl_category = "EasyFX"
    bl_label = "Settings"
    bl_idname = "EASYFX_PT_Settings"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        scn = context.scene
        # mytool = scn.easyfx
        layout = self.layout
        # layout.prop(mytool, "layer_index", text="Layer index")
        layout.operator('object.reset_settings_operator',
                        text="Reset all values", icon="RECOVER_LAST")
        # ERROR RECOVER_LAST FILE_REFRESH RECOVER_AUTO
        
