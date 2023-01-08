import bpy, math
from bpy.types import PropertyGroup

from .EasyFX_op import *

class MySettings(PropertyGroup):

    # Nodes
    use_auto_update: BoolProperty(
        name="Auto Update",
        description="Automatically update when a value is altered",
        default=True, update=Auto_Update)
    # Filters
    use_vignette: BoolProperty(
        name="Vignette",
        description="Gradual decrease in light intensity towards the image borders",
        default=False, update=Auto_Update)
    vignette_v: FloatProperty(name="Viggnette Amount", description="Amount",
                              default=70, min=0, max=100, subtype="PERCENTAGE", update=Auto_Update)
    use_glow: BoolProperty(
        name="Glow",
        description="Glow",
        default=False, update=Auto_Update)
        
    glow_em: BoolProperty(
        name="Only Emission",
        description="Only materials with an emission value will glow",
        default=False, update=Auto_Update)
    glow_v: FloatProperty(name="Viggnette Amount",
                          description="Amount", default=1, min=0, update=Auto_Update)
    use_streaks: BoolProperty(
        name="Streaks",
        description="Streaks",
        default=False, update=Auto_Update)
    streaks_em: BoolProperty(
        name="Only Emission",
        description="Only materials with an emission value will generate streaks",
        default=False, update=Auto_Update)
    streaks_v: FloatProperty(
        name="Viggnette Amount", description="Amount", default=1, min=0, update=Auto_Update)
    streaks_n: IntProperty(name="Number of streaks", description="Number of streaks",
                           default=4, min=2, max=16, update=Auto_Update)
    streaks_d: FloatProperty(name="Angle Offset", description="Streak angle offset",
                             default=0, min=0, max=math.pi, unit='ROTATION', update=Auto_Update)
    sharpen_v: FloatProperty(
        name="Sharpen", description="Sharpen image", default=0, min=0, update=Auto_Update)
    soften_v: FloatProperty(
        name="Soften", description="Soften image", default=0, min=0, update=Auto_Update)

    # Blurs
    use_speedb: BoolProperty(
        name="Motion Blur",
        description="Blurs out fast motions",
        default=False, update=Auto_Update)
    motionb_v: FloatProperty(name="Motion blur amount",
                             description="Amount of motion blur", default=1.0, min=0, update=Auto_Update)
    use_dof: BoolProperty(
        name="Depth of field",
        description="Range of distance that appears acceptably sharp",
        default=False, update=Auto_Update)
    dof_v: FloatProperty(name="Defocus amount", description="Amount of blur",
                         default=50.0, min=0, max=128, update=Auto_Update)

    # Color
    bw_v: FloatProperty(name="Saturation", description="Saturation",
                        default=1, min=0, max=4, subtype="FACTOR", update=Auto_Update)
    contrast_v: FloatProperty(
        name="Contrast", description="The difference in color and light between parts of an image", default=0, update=Auto_Update)
    brightness_v: FloatProperty(
        name="Brightness", description="Brightness", default=0, update=Auto_Update)
    shadows_v: bpy.props.FloatVectorProperty(
        name="Shadows", description="Shadows", subtype="COLOR_GAMMA", default=(1, 1, 1), min=0, max=2, update=Auto_Update)
    midtones_v: bpy.props.FloatVectorProperty(
        name="Midtones", description="Midtones", subtype="COLOR_GAMMA", default=(1, 1, 1), min=0, max=2, update=Auto_Update)
    highlights_v: bpy.props.FloatVectorProperty(
        name="Highlights", description="Highlights", subtype="COLOR_GAMMA", default=(1, 1, 1), min=0, max=2, update=Auto_Update)
    check_v: bpy.props.FloatVectorProperty(
        default=(1, 1, 1), subtype="COLOR_GAMMA", update=Auto_Update)

    # Distort / Lens
    use_flip: BoolProperty(
        name="Flip image",
        description="Flip image on the X axis",
        default=False, update=Auto_Update)
    lens_distort_v: FloatProperty(
        name="Distort", description="Distort the lens", default=0, min=-0.999, max=1, update=Auto_Update)
    dispersion_v: FloatProperty(
        name="Dispersion", description="A type of distortion in which there is a failure of a lens to focus all colors to the same convergence point", default=0, min=0, max=1, update=Auto_Update)
    use_flare: BoolProperty(
        name="Lens Flare",
        description="Lens Flare",
        default=False, update=Auto_Update)
    flare_type: EnumProperty(items=[('Fixed', 'Fixed', 'Fixed position'), ('Tracked', 'Tracked',
                             'Select if you want object to place in the viewport to act like the flare')], update=Auto_Update)
    flare_c: bpy.props.FloatVectorProperty(name="Highlights", description="Flare Color", subtype="COLOR_GAMMA", size=4, default=(
        1, 0.3, 0.084, 1), min=0, max=1, update=Auto_Update)
    flare_x: FloatProperty(
        name="Flare X Pos", description="Flare X offset", default=0, update=Auto_Update)
    flare_y: FloatProperty(
        name="Flare Y Pos", description="Flare Y offset", default=0, update=Auto_Update)
    # flare_size = FloatProperty(name="Size",description="Flare Y offset", default=0, update=Auto_Update)
    flare_streak_intensity: FloatProperty(
        name="Size", description="Streak Intensity", default=0.002, min=0, max=1, subtype='FACTOR', update=Auto_Update)
    flare_streak_lenght: FloatProperty(name="Size", description="Streak Lenght",
                                       default=1, max=3, min=0.001, subtype='FACTOR', update=Auto_Update)
    flare_streak_angle: FloatProperty(name="Size", description="Streak Rotatiom",
                                      default=0, max=math.pi, min=0, subtype='ANGLE', update=Auto_Update)
    flare_streak_streaks: IntProperty(
        name="Size", description="Streak Streaks", default=12, max=16, min=2, update=Auto_Update)
    flare_glow: FloatProperty(name="Size", description="Glow Intensity",
                              default=0.03, min=0, max=1, subtype='FACTOR', update=Auto_Update)
    flare_ghost: FloatProperty(
        name="Size", description="Ghost Intensity", default=1, min=0, update=Auto_Update)
    flare_layer: bpy.props.BoolVectorProperty(name="test", subtype="LAYER", size=20, update=Auto_Update, default=(
        False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False))
    # Tracked
    flaret_streak_intensity: FloatProperty(
        name="Size", description="Streak Intensity", default=0.03, min=0, max=1, subtype='FACTOR', update=Auto_Update)
    flaret_streak_lenght: FloatProperty(name="Size", description="Streak Lenght",
                                        default=1.5, max=3, min=0.001, subtype='FACTOR', update=Auto_Update)
    flaret_streak_angle: FloatProperty(name="Size", description="Streak Rotatiom",
                                       default=0, max=math.pi, min=0, subtype='ANGLE', update=Auto_Update)
    flaret_streak_streaks: IntProperty(
        name="Size", description="Streak Streaks", default=12, max=16, min=2, update=Auto_Update)
    flaret_glow: FloatProperty(name="Size", description="Glow Intensity",
                               default=0.1, min=0, max=1, subtype='FACTOR', update=Auto_Update)
    flaret_ghost: FloatProperty(
        name="Size", description="Ghost Intensity", default=1.5, min=0, update=Auto_Update)
    flare_center_size: FloatProperty(
        name="Size", description="Size of the flare source", default=20, min=1, update=Auto_Update)

    # World
    use_mist: BoolProperty(
        name="Use Mist",
        description="Mist",
        default=False, update=Auto_Update)
    mist_sky: BoolProperty(
        name="Use Mist",
        description="The mist will affect the sky",
        default=True, update=Auto_Update)
    mist_offset: FloatProperty(
        name="Size", description="Offset", default=0, update=Auto_Update)
    mist_size: FloatProperty(
        name="Size", description="Amount", default=0.01, update=Auto_Update)
    mist_min: FloatProperty(name="Size", description="Minimum",
                            default=0, min=0, max=1, update=Auto_Update, subtype="FACTOR")
    mist_max: FloatProperty(name="Size", description="Maximum",
                            default=1, min=0, max=1, update=Auto_Update, subtype="FACTOR")
    mist_color: bpy.props.FloatVectorProperty(name="Mist Color", description="Mist Color",
                                              subtype="COLOR_GAMMA", size=4, default=(1, 1, 1, 1), min=0, max=1, update=Auto_Update)

    # Settings
    use_cinematic_border: BoolProperty(
        name="Cinematic Border",
        description="Add black borders at top and bottom",
        default=False, update=Auto_Update)
    cinematic_border_v: FloatProperty(
        name="Cinematic Border", description="border height", default=0.4, min=0, max=1, update=Auto_Update)
    use_transparent_sky: BoolProperty(
        name="Transparent Sky",
        description="Render the sky as transparent",
        default=False, update=Auto_Update)
    use_cel_shading: BoolProperty(
        name="Cell Shading",
        description="Adds a black outline, mimic the style of a comic book or cartoon",
        default=False, update=Auto_Update)
    cel_thickness: FloatProperty(name="Cel shading thickness", description="Line thickness",
                                 default=1, min=0, subtype='PIXEL', update=Auto_Update)
    split_image: BoolProperty(
        name="Split Original",
        description="Split the image with the original render",
        default=False, update=Auto_Update)
    split_v: IntProperty(name="Split Value", description="Where to split the image",
                         default=50, min=0, max=100, subtype='PERCENTAGE', update=Auto_Update)
    use_image_sky: BoolProperty(
        name="Image Sky",
        description="Use external image as sky",
        default=False, update=Auto_Update)
    image_sky_img: StringProperty(
        name="Sky Image", description="Image", default="", subtype='FILE_PATH', update=Auto_Update)
    image_sky_x: FloatProperty(
        name="Image Sky X", description="Image offset on the X axis", default=0, update=Auto_Update)
    image_sky_y: FloatProperty(
        name="Image Sky Y", description="Image offset on the Y axis", default=0, update=Auto_Update)
    image_sky_angle: FloatProperty(
        name="Image Sky Angle", description="Image Rotation", default=0, update=Auto_Update)
    image_sky_scale: FloatProperty(
        name="Image sky Scale", description="Image Scale", default=1, update=Auto_Update)
    layer_index: IntProperty(
        name="Layer Index", description="Render Layer to use as main", default=0, min=0, update=Auto_Update)
