import bpy
import math
from math import pi as PI
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

s_sky = False
s_cell = True
first = True
imgs = ""
skyimg = ""


def Auto_Update(self, context):
    if bpy.context.scene.easyfx.use_auto_update == True:
        bpy.ops.object.update_operator()

def Auto_render():
    bpy.ops.object.update_operator()
    bpy.ops.render.render('INVOKE_DEFAULT')


class EASYFX_OT_UpdateOperator(bpy.types.Operator):
    '''Update'''
    bl_idname = "object.update_operator"
    bl_label = "Update Nodes Operator"

    def execute(self, context):
        editorcheck = False
        ef_use_sky = True
        efFullscreen = False
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                if area.spaces.active.tree_type != 'CompositorNodeTree':
                    area.spaces.active.tree_type = 'CompositorNodeTree'
                editorcheck = True
        if editorcheck == False:
            try:
                bpy.context.area.type = 'NODE_EDITOR'
                bpy.context.area.ui_type = "CompositorNodeTree"
                bpy.ops.screen.area_split(factor=1)
                bpy.context.area.type = 'VIEW_3D'
                bpy.context.area.type = 'IMAGE_EDITOR'
            except:
                bpy.context.area.type = 'IMAGE_EDITOR'
                bpy.ops.screen.back_to_previous()
                self.report({'WARNING'}, "Fullscreen is not supported")
                efFullscreen = True

        scene = bpy.context.scene
        scene.use_nodes = True
        nodes = scene.node_tree.nodes
        links = scene.node_tree.links

        pos_x = 200
        ef = bpy.context.scene.easyfx
        # Layer Index
        layeri = ef.layer_index
        layern = bpy.context.scene.view_layers[layeri].name
        try:
            nodes.remove(nodes['Render Layers'])
            nodes.remove(nodes['Composite'])
        except:
            pass
        # Default Setup
        # Clear Nodes
        # nodes.clear()

        # Input n Output
        try:
            CIn = nodes["Input"]
        except:
            CIn = nodes.new(type='CompositorNodeRLayers')
            CIn.name = "Input"
            CIn.label = "Input"
        try:
            COut = nodes["Output"]
        except:
            COut = nodes.new(type='CompositorNodeComposite')
            COut.name = "Output"
            COut.label = "Output"
        CIn.layer = layern
        latest_node = CIn

    # --------------------------------------------
    #   Other Settings
    # --------------------------------------------
        global s_sky, s_cell

        # Transparent Sky
        if ef.use_transparent_sky == True:
            ef_use_sky = False

        # Cell Shading
        if ef.use_cel_shading == True:
            scene.render.line_thickness = ef.cel_thickness
            if s_cell == True:
                scene.render.use_freestyle = True
                self.report({'INFO'}, "Re-render Required")
                s_cell = False
                Auto_render()
        elif ef.use_cel_shading == False and s_cell == False:
            scene.render.use_freestyle = False
            self.report({'INFO'}, "Re-render Required")
            s_cell = True
            Auto_render()

    # --------------------------------------------
    #   Nodes
    # --------------------------------------------
        # Sharpen
        if ef.sharpen_v != 0:
            try:
                node_sharpen = nodes['Sharpen']
            except:
                node_sharpen = nodes.new(type='CompositorNodeFilter')
                node_sharpen.filter_type = 'SHARPEN'
                node_sharpen.name = 'Sharpen'
            node_sharpen.inputs[0].default_value = ef.sharpen_v
            node_sharpen.location = (pos_x, 0)
            pos_x = pos_x+200
            links.new(latest_node.outputs[0], node_sharpen.inputs[1])
            latest_node = node_sharpen
        else:
            try:
                nodes.remove(nodes['Sharpen'])
            except:
                pass
        # Soften
        if ef.soften_v != 0:
            try:
                node_soften = nodes['Soften']
            except:
                node_soften = nodes.new(type='CompositorNodeFilter')
                node_soften.name = 'Soften'
            node_soften.location = (pos_x, 0)
            node_soften.inputs[0].default_value = ef.soften_v
            pos_x = pos_x+200
            links.new(latest_node.outputs[0], node_soften.inputs[1])
            latest_node = node_soften
        else:
            try:
                nodes.remove(nodes['Soften'])
            except:
                pass

        # Speed Blur
        if ef.use_speedb == True and ef.motionb_v != 0:
            try:
                node_VecBlur = nodes['VecBlur']
            except:
                node_VecBlur = nodes.new(type='CompositorNodeVecBlur')
                links.new(CIn.outputs[0], node_VecBlur.inputs[0])
                node_VecBlur.name = 'VecBlur'
                node_VecBlur.label = 'Motion blur'
                links.new(CIn.outputs[2], node_VecBlur.inputs[1])
                links.new(CIn.outputs[5], node_VecBlur.inputs[2])
            node_VecBlur.location = (pos_x, 0)
            node_VecBlur.factor = ef.motionb_v
            pos_x = pos_x+200
            links.new(latest_node.outputs[0], node_VecBlur.inputs[0])
            latest_node = node_VecBlur
            if scene.view_layers[layeri].use_pass_z == True and scene.view_layers[layeri].use_pass_vector == True:
                pass
            else:
                scene.view_layers[layeri].use_pass_z = True
                scene.view_layers[layeri].use_pass_vector = True
                self.report({'INFO'}, "Re-render Required")
                Auto_render()
        else:
            try:
                nodes.remove(nodes['VecBlur'])
            except:
                pass

        # Defocus
        if ef.use_dof == True:
            try:
                node_dof = nodes['DOF']
            except:
                node_dof = nodes.new(type='CompositorNodeDefocus')
                node_dof.use_zbuffer = True
                node_dof.name = 'DOF'
                node_dof.label = 'Depth of field'
                node_dof.use_preview = False
                links.new(CIn.outputs[2], node_dof.inputs[1])
            node_dof.f_stop = ef.dof_v
            node_dof.location = (pos_x, 0)
            pos_x = pos_x+200
            bpy.data.cameras[0].show_limits = True
            links.new(latest_node.outputs[0], node_dof.inputs[0])
            latest_node = node_dof
            if scene.view_layers[layeri].use_pass_z == True:
                pass
            else:
                scene.view_layers[layeri].use_pass_z = True
                self.report({'INFO'}, "Re-render Required")
                Auto_render()
        else:
            try:
                nodes.remove(nodes['DOF'])
            except:
                pass

        # Color Correction
        if ef.shadows_v != ef.check_v or ef.midtones_v != ef.check_v or ef.highlights_v != ef.check_v:
            try:
                node_color = nodes['CC']
            except:
                node_color = nodes.new(type='CompositorNodeColorBalance')
                node_color.name = 'CC'
            node_color.lift = ef.shadows_v
            node_color.gamma = ef.midtones_v
            node_color.gain = ef.highlights_v
            node_color.location = (pos_x, 0)
            pos_x = pos_x+450
            links.new(latest_node.outputs[0], node_color.inputs[1])
            latest_node = node_color
        else:
            try:
                nodes.remove(nodes['CC'])
            except:
                pass

        # Brightness/Contrast
        if ef.contrast_v != 0 or ef.brightness_v != 0:
            try:
                node_brightcont = nodes['BC']
            except:
                node_brightcont = nodes.new(
                    type='CompositorNodeBrightContrast')
                node_brightcont.name = 'BC'
            node_brightcont.location = (pos_x, 0)
            pos_x = pos_x+200
            node_brightcont.inputs[1].default_value = ef.brightness_v
            node_brightcont.inputs[2].default_value = ef.contrast_v
            links.new(latest_node.outputs[0], node_brightcont.inputs[0])
            latest_node = node_brightcont
        else:
            try:
                nodes.remove(nodes['BC'])
            except:
                pass

        # Mist
        if ef.use_mist == True:
            try:
                node_mist_mapv = nodes['Mist MapV']
                node_mist_mix = nodes['Mist Mix']
                node_mist_cramp = nodes['Mist CRamp']
            except:
                node_mist_mapv = nodes.new(type='CompositorNodeMapValue')
                node_mist_mapv.name = 'Mist MapV'
                node_mist_mapv.label = 'Mist'
                node_mist_cramp = nodes.new(type='CompositorNodeValToRGB')
                node_mist_cramp.name = 'Mist CRamp'
                node_mist_mix = nodes.new(type='CompositorNodeMixRGB')
                node_mist_mix.name = "Mist Mix"
                links.new(CIn.outputs[2], node_mist_mapv.inputs[0])
                links.new(node_mist_mapv.outputs[0], node_mist_cramp.inputs[0])
                links.new(node_mist_cramp.outputs[0], node_mist_mix.inputs[0])
            node_mist_mapv.offset[0] = -1*ef.mist_offset
            node_mist_mapv.size[0] = ef.mist_size
            if ef.mist_min != 0:
                node_mist_mapv.use_min = True
                node_mist_mapv.min[0] = ef.mist_min
            if ef.mist_max != 1:
                node_mist_mapv.use_max = True
                node_mist_mapv.max[0] = ef.mist_max
            node_mist_mix.inputs[2].default_value = ef.mist_color
            node_mist_mapv.location = (pos_x, 250)
            pos_x = pos_x+200
            node_mist_cramp.location = (pos_x, 250)
            pos_x = pos_x+300
            node_mist_mix.location = (pos_x, 0)
            pos_x = pos_x+200
            links.new(latest_node.outputs[0], node_mist_mix.inputs[1])
            latest_node = node_mist_mix
            # Affect Sky
            if ef.mist_sky == False:
                ef_use_sky = False
                try:
                    sky_layer = scene.view_layers['EasyFX - Sky']
                except:
                    sky_layer = bpy.ops.scene.render_layer_add()
                    try:
                        layx = 0
                        while True:
                            sky_layer = bpy.context.scene.view_layers[layx]
                            layx = layx+1
                    except:
                        sky_layer.name = 'EasyFX - Sky'
                        sky_layer.use_solid = False
                        sky_layer.use_halo = False
                        sky_layer.use_ztransp = False
                        sky_layer.use_edge_enhance = False
                        sky_layer.use_strand = False
                        sky_layer.use_freestyle = False
                    layer_active = 0
                    while layer_active < 20:
                        sky_layer.layers[layer_active] = False
                        sky_layer.layers_zmask[layer_active] = True
                        layer_active = layer_active+1

                try:
                    node_mist_sky = nodes['Mist_sky']
                    node_mist_alphov = nodes['Mist_alphov']
                except:
                    node_mist_sky = nodes.new(type='CompositorNodeRLayers')
                    node_mist_sky.name = 'Mist_sky'
                    node_mist_sky.label = 'Sky'
                    node_mist_sky.layer = 'EasyFX - Sky'
                    node_mist_alphov = nodes.new(
                        type='CompositorNodeAlphaOver')
                    node_mist_alphov.name = 'Mist_alphov'
                    links.new(CIn.outputs[1], node_mist_alphov.inputs[0])
                    links.new(
                        node_mist_sky.outputs[0], node_mist_alphov.inputs[1])
                    links.new(
                        node_mist_mix.outputs[0], node_mist_alphov.inputs[2])
                node_mist_sky.location = (pos_x-200, -220)
                node_mist_alphov.location = (pos_x, 0)
                pos_x = pos_x+200
                latest_node = node_mist_alphov
            else:
                try:
                    nodes.remove(nodes['Mist_sky'])
                    nodes.remove(nodes['Mist_alphov'])
                except:
                    pass
        else:
            try:
                nodes.remove(nodes['Mist MapV'])
                nodes.remove(nodes['Mist CRamp'])
                nodes.remove(nodes['Mist Mix'])
                nodes.remove(nodes['Mist_sky'])
                nodes.remove(nodes['Mist_alphov'])
            except:
                pass

        # Streaks
        if ef.use_streaks == True:
            try:
                node_streaks = nodes['Streaks']
            except:
                node_streaks = nodes.new(type='CompositorNodeGlare')
                node_streaks.name = 'Streaks'
                node_streaks.label = 'Streaks'
            node_streaks.threshold = ef.streaks_v
            node_streaks.streaks = ef.streaks_n
            node_streaks.angle_offset = ef.streaks_d

            if ef.streaks_em == True:
                if scene.view_layers[layeri].use_pass_emit == False:
                    scene.view_layers[layeri].use_pass_emit = True
                    self.report({'INFO'}, "Re-render Required")
                    
                links.new(CIn.outputs[17], node_streaks.inputs[0])
                try:
                    node_streaks_mix = nodes['Streaks Mix']
                except:
                    node_streaks_mix = nodes.new(type='CompositorNodeMixRGB')
                    node_streaks_mix.blend_type = 'ADD'
                    node_streaks_mix.name = 'Streaks Mix'
                links.new(latest_node.outputs[0], node_streaks_mix.inputs[1])
                links.new(node_streaks.outputs[0], node_streaks_mix.inputs[2])
                latest_node = node_streaks_mix
                node_streaks.location = (pos_x, -170)
                pos_x = pos_x+200
                node_streaks_mix.location = (pos_x, 0)
                pos_x = pos_x+200
            else:
                links.new(latest_node.outputs[0], node_streaks.inputs[0])
                latest_node = node_streaks
                node_streaks.location = (pos_x, 0)
                pos_x = pos_x+200
                try:
                    nodes.remove(nodes['Streaks Mix'])
                except:
                    pass
        else:
            try:
                nodes.remove(nodes['Streaks'])
                nodes.remove(nodes['Streaks Mix'])
            except:
                pass

        # Glow
        if ef.use_glow == True:
            try:
                node_glow = nodes['Glow']
            except:
                node_glow = nodes.new(type='CompositorNodeGlare')
                node_glow.glare_type = 'FOG_GLOW'
                node_glow.name = 'Glow'
                node_glow.label = 'Glow'
            node_glow.threshold = ef.glow_v
            if ef.glow_em == True:
                if scene.view_layers[layeri].use_pass_emit == False:
                    scene.view_layers[layeri].use_pass_emit = True
                    self.report({'INFO'}, "Re-render Required")
                links.new(CIn.outputs[17], node_glow.inputs[0])
                try:
                    node_glow_mix = nodes['Glow Mix']
                except:
                    node_glow_mix = nodes.new(type='CompositorNodeMixRGB')
                    node_glow_mix.blend_type = 'ADD'
                    node_glow_mix.name = 'Glow Mix'
                    links.new(node_glow.outputs[0], node_glow_mix.inputs[2])
                links.new(latest_node.outputs[0], node_glow_mix.inputs[1])
                latest_node = node_glow_mix
                node_glow.location = (pos_x, -170)
                pos_x = pos_x+200
                node_glow_mix.location = (pos_x, 0)
                pos_x = pos_x+200
            else:
                links.new(latest_node.outputs[0], node_glow.inputs[0])
                latest_node = node_glow
                node_glow.location = (pos_x, 0)
                pos_x = pos_x+200
                try:
                    nodes.remove(nodes['Glow Mix'])
                except:
                    pass
        else:
            try:
                nodes.remove(nodes['Glow'])
                nodes.remove(nodes['Glow Mix'])
            except:
                pass

        # Image Sky
        if ef.use_image_sky == True:
            try:
                node_imgsky_img = nodes['Image input']
                node_imgsky_alphov = nodes['Image mix']
                node_imgsky_trans = nodes['Image transform']
            except:
                node_imgsky_img = nodes.new(type='CompositorNodeImage')
                node_imgsky_img.name = 'Image input'
                node_imgsky_alphov = nodes.new(type='CompositorNodeAlphaOver')
                node_imgsky_alphov.name = 'Image mix'
                node_imgsky_trans = nodes.new(type='CompositorNodeTransform')
                node_imgsky_trans.name = 'Image transform'
                links.new(
                    node_imgsky_img.outputs[0], node_imgsky_trans.inputs[0])
                links.new(
                    node_imgsky_trans.outputs[0], node_imgsky_alphov.inputs[1])
                pass
            # Update Values
            node_imgsky_trans.inputs[1].default_value = ef.image_sky_x
            node_imgsky_trans.inputs[2].default_value = ef.image_sky_y
            node_imgsky_trans.inputs[3].default_value = ef.image_sky_angle
            node_imgsky_trans.inputs[4].default_value = ef.image_sky_scale * \
                scene.render.resolution_percentage/100
            links.new(latest_node.outputs[0], node_imgsky_alphov.inputs[2])
            latest_node = node_imgsky_alphov
            node_imgsky_img.location = (pos_x-400, 250)
            node_imgsky_trans.location = (pos_x-200, 250)
            node_imgsky_alphov.location = (pos_x, 0)
            pos_x = pos_x+200
            ef_global_sky = True
            global imgs, skyimg
            if imgs != ef.image_sky_img:
                try:
                    path = r"" + bpy.path.abspath(ef.image_sky_img)
                    skyimg = bpy.data.images.load(path)
                    node_imgsky_img.image = skyimg
                except:
                    self.report({'WARNING'}, "Could not load image")
            else:
                try:
                    node_imgsky_img.image = skyimg
                except:
                    pass
            imgs = ef.image_sky_img
            ef_use_sky = False
        else:
            try:
                nodes.remove(nodes['Image input'])
                nodes.remove(nodes['Image mix'])
                nodes.remove(nodes['Image transform'])
            except:
                pass

        # Lens Flare
        if ef.use_flare == True:
            # Tracked Flare
            if ef.flare_type == 'Tracked':
                # Create Tracker
                try:
                    bpy.data.objects['EasyFX - Flare']
                except:
                    bpy.ops.mesh.primitive_uv_sphere_add(
                        segments=10, ring_count=16)
                    flare_sphere = bpy.context.object
                    flare_sphere.name = 'EasyFX - Flare'
                    mat = bpy.data.materials.new("EasyFX - Flare")
                    mat.specular_intensity = 0
                    mat.emit = 5
                    bpy.context.object.data.materials.append(mat)
                try:
                    flare_layer = bpy.context.scene.render.layers['EasyFX - Flare']
                except:
                    flare_layer = bpy.ops.scene.render_layer_add()
                    try:
                        layx = 0
                        while True:
                            flare_layer = bpy.context.scene.view_layers[layx]
                            layx = layx+1
                    except:
                        flare_layer.name = 'EasyFX - Flare'
                        flare_layer.use_sky = False
                    layer_active = 0
                    while layer_active < 20:
                        flare_layer.layers[layer_active] = False
                        flare_layer.layers_zmask[layer_active] = True
                        layer_active = layer_active+1
                    # flare_layer.layers[15] = True
                    # flare_layer.layers[19] = False
                flare_layer.layers = ef.flare_layer
                bpy.ops.object.move_to_layer(layers=ef.flare_layer)
            if ef.flare_type == 'Fixed':
                pos_x = pos_x-600
                try:
                    nodes.remove(nodes['flare_rlayer'])
                except:
                    pass
                try:
                    node_flare_mask1 = nodes['flare_mask1']
                    node_flare_rgb = nodes['flare_rgb']
                    node_flare_dist1 = nodes['flare_dist1']
                    node_flare_dist2 = nodes['flare_dist2']
                    node_flare_mask2 = nodes['flare_mask2']
                    node_flare_mixc = nodes['flare_mixc']
                    node_flare_trans = nodes['flare_translate']
                    node_flare_alphov = nodes['flare_alphaover']
                    node_flare_ckey = nodes['flare_ckey']
                except:
                    node_flare_mask1 = nodes.new(type='CompositorNodeMask')
                    node_flare_mask1.size_source = 'FIXED'
                    node_flare_mask1.name = 'flare_mask1'
                    node_flare_rgb = nodes.new(type='CompositorNodeRGB')
                    node_flare_rgb.name = 'flare_rgb'
                    node_flare_rgb.label = 'Flare Color'
                    node_flare_dist1 = nodes.new(type='CompositorNodeLensdist')
                    node_flare_dist1.inputs[1].default_value = 1
                    node_flare_dist1.name = 'flare_dist1'
                    node_flare_dist2 = nodes.new(type='CompositorNodeLensdist')
                    node_flare_dist2.inputs[1].default_value = 1
                    node_flare_dist2.name = 'flare_dist2'
                    node_flare_mixc = nodes.new(type='CompositorNodeMixRGB')
                    node_flare_mixc.blend_type = 'ADD'
                    node_flare_mixc.name = 'flare_mixc'
                    node_flare_trans = nodes.new(
                        type='CompositorNodeTranslate')
                    node_flare_trans.name = 'flare_translate'
                    node_flare_mask2 = nodes.new(type='CompositorNodeMask')
                    node_flare_mask2.name = 'flare_mask2'
                    node_flare_alphov = nodes.new(
                        type='CompositorNodeAlphaOver')
                    node_flare_alphov.name = 'flare_alphaover'
                    node_flare_ckey = nodes.new(
                        type='CompositorNodeChromaMatte')
                    node_flare_ckey.name = 'flare_ckey'
                    node_flare_ckey.tolerance = 1
                    node_flare_ckey.threshold = 1
                    node_flare_ckey.gain = 0
                    node_flare_ckey.inputs[1].default_value = (0, 0, 0, 1)

                    links.new(
                        node_flare_mask1.outputs[0], node_flare_dist1.inputs[0])
                    links.new(
                        node_flare_dist1.outputs[0], node_flare_mixc.inputs[1])
                    links.new(
                        node_flare_rgb.outputs[0], node_flare_dist2.inputs[0])
                    links.new(
                        node_flare_dist2.outputs[0], node_flare_mixc.inputs[2])
                    links.new(
                        node_flare_mixc.outputs[0], node_flare_trans.inputs[0])
                    links.new(
                        node_flare_trans.outputs[0], node_flare_alphov.inputs[2])
                    links.new(
                        node_flare_mask2.outputs[0], node_flare_alphov.inputs[1])
                    links.new(
                        node_flare_alphov.outputs[0], node_flare_ckey.inputs[0])
                node_flare_rgb.outputs[0].default_value = ef.flare_c
                node_flare_trans.inputs[1].default_value = ef.flare_x
                node_flare_trans.inputs[2].default_value = ef.flare_y
                node_flare_layer = node_flare_ckey

                node_flare_mask1.size_x = ef.flare_center_size
                node_flare_mask1.size_y = ef.flare_center_size
                node_flare_mask1.location = (pos_x, -450)
                node_flare_rgb.location = (pos_x, -700)
                pos_x = pos_x+200
                node_flare_dist1.location = (pos_x, -450)
                node_flare_dist2.location = (pos_x, -700)
                pos_x = pos_x+200
                node_flare_mixc.location = (pos_x, -450)
                pos_x = pos_x+200
                node_flare_trans.location = (pos_x, -450)
                node_flare_mask2.location = (pos_x, -200)
                pos_x = pos_x+200
                node_flare_alphov.location = (pos_x, -200)
                pos_x = pos_x+200
                node_flare_ckey.location = (pos_x, -200)
                pos_x = pos_x+200

                # If Tracked
            else:
                try:
                    nodes.remove(nodes['flare_mask1'])
                    nodes.remove(nodes['flare_rgb'])
                    nodes.remove(nodes['flare_dist1'])
                    nodes.remove(nodes['flare_dist2'])
                    nodes.remove(nodes['flare_mask2'])
                    nodes.remove(nodes['flare_mixc'])
                    nodes.remove(nodes['flare_translate'])
                    nodes.remove(nodes['flare_alphaover'])
                    nodes.remove(nodes['flare_ckey'])
                except:
                    pass
                try:
                    node_flare_layer = nodes['flare_rlayer']
                except:
                    node_flare_layer = nodes.new(type='CompositorNodeRLayers')
                    node_flare_layer.name = 'flare_rlayer'
                    node_flare_layer.layer = 'EasyFX - Flare'
                node_flare_layer.location = (pos_x-200, -600)
            try:
                node_flare_ghost = nodes['flare_ghost']
                node_flare_glow = nodes['flare_glow']
                node_flare_streaks = nodes['flare_streaks']
                node_flare_tonemap = nodes['flare_tonemap']
                node_flare_mix1 = nodes['flare_mix1']
                node_flare_mix2 = nodes['flare_mix2']
                node_flare_mix3 = nodes['flare_mix3']
                node_flare_tonemap2 = nodes['flare_tonemap2']
            except:
                node_flare_ghost = nodes.new(type='CompositorNodeGlare')
                node_flare_ghost.glare_type = 'GHOSTS'
                node_flare_ghost.threshold = 0
                node_flare_ghost.name = 'flare_ghost'
                node_flare_glow = nodes.new(type='CompositorNodeGlare')
                node_flare_glow.glare_type = 'FOG_GLOW'
                node_flare_glow.threshold = 0
                node_flare_glow.quality = 'LOW'
                node_flare_glow.name = 'flare_glow'
                node_flare_streaks = nodes.new(type='CompositorNodeGlare')
                node_flare_streaks.glare_type = 'STREAKS'
                node_flare_streaks.threshold = 0
                node_flare_streaks.streaks = 12
                node_flare_streaks.quality = 'LOW'
                node_flare_streaks.name = 'flare_streaks'
                node_flare_streaks.angle_offset = 10*PI/180
                node_flare_tonemap = nodes.new(type='CompositorNodeTonemap')
                node_flare_tonemap.tonemap_type = 'RH_SIMPLE'
                node_flare_tonemap.key = 0.007
                node_flare_tonemap.name = 'flare_tonemap'
                node_flare_mix1 = nodes.new(type='CompositorNodeMixRGB')
                node_flare_mix1.blend_type = 'SCREEN'
                node_flare_mix1.name = 'flare_mix1'
                node_flare_mix2 = nodes.new(type='CompositorNodeMixRGB')
                node_flare_mix2.blend_type = 'SCREEN'
                node_flare_mix2.name = 'flare_mix2'
                node_flare_mix3 = nodes.new(type='CompositorNodeMixRGB')
                node_flare_mix3.blend_type = 'SCREEN'
                node_flare_mix3.name = 'flare_mix3'
                node_flare_tonemap2 = nodes.new(type='CompositorNodeTonemap')
                node_flare_tonemap2.tonemap_type = 'RH_SIMPLE'
                node_flare_tonemap2.name = 'flare_tonemap2'
                links.new(
                    node_flare_mix2.outputs[0], node_flare_mix3.inputs[2])
                links.new(
                    node_flare_mix1.outputs[0], node_flare_mix2.inputs[1])
                links.new(
                    node_flare_streaks.outputs[0], node_flare_mix2.inputs[2])
                links.new(
                    node_flare_tonemap.outputs[0], node_flare_mix1.inputs[1])
                links.new(
                    node_flare_ghost.outputs[0], node_flare_mix1.inputs[2])
                links.new(
                    node_flare_glow.outputs[0], node_flare_tonemap.inputs[0])

                links.new(
                    node_flare_streaks.outputs[0], node_flare_tonemap2.inputs[0])
                links.new(
                    node_flare_tonemap2.outputs[0], node_flare_mix2.inputs[2])

            links.new(node_flare_layer.outputs[0], node_flare_ghost.inputs[0])
            links.new(node_flare_layer.outputs[0], node_flare_glow.inputs[0])
            links.new(node_flare_layer.outputs[0],
                      node_flare_streaks.inputs[0])
            links.new(latest_node.outputs[0], node_flare_mix3.inputs[1])
            latest_node = node_flare_mix3
            node_flare_ghost.location = (pos_x, -200)
            node_flare_glow.location = (pos_x, -450)
            node_flare_streaks.location = (pos_x, -680)
            pos_x = pos_x+200
            node_flare_tonemap.location = (pos_x, -350)
            pos_x = pos_x+200
            node_flare_tonemap2.location = (pos_x, -400)
            node_flare_mix1.location = (pos_x, -200)
            pos_x = pos_x+200
            node_flare_mix2.location = (pos_x, -200)
            pos_x = pos_x+200
            node_flare_mix3.location = (pos_x, 0)
            pos_x = pos_x+200

            if ef.flare_type == 'Fixed':
                node_flare_tonemap.key = 0.03
                node_flare_tonemap2.location = (pos_x-600, -550)
                node_flare_tonemap2.offset = 10
                node_flare_streaks.iterations = 5
                node_flare_streaks.quality = 'MEDIUM'
                node_flare_streaks.fade = 0.92
                node_flare_ghost.iterations = 4
                node_flare_tonemap2.key = ef.flare_streak_intensity
                node_flare_tonemap2.gamma = ef.flare_streak_lenght
                node_flare_streaks.angle_offset = ef.flare_streak_angle
                node_flare_streaks.streaks = ef.flare_streak_streaks
                node_flare_tonemap.key = ef.flare_glow
                node_flare_mix1.inputs[0].default_value = ef.flare_ghost
            else:
                node_flare_tonemap2.key = ef.flaret_streak_intensity
                node_flare_tonemap2.gamma = ef.flaret_streak_lenght
                node_flare_streaks.angle_offset = ef.flaret_streak_angle
                node_flare_streaks.streaks = ef.flaret_streak_streaks
                node_flare_tonemap.key = ef.flaret_glow
                node_flare_mix1.inputs[0].default_value = ef.flaret_ghost
        else:
            try:
                nodes.remove(nodes['flare_ghost'])
                nodes.remove(nodes['flare_glow'])
                nodes.remove(nodes['flare_streaks'])
                nodes.remove(nodes['flare_tonemap'])
                nodes.remove(nodes['flare_mix1'])
                nodes.remove(nodes['flare_mix2'])
                nodes.remove(nodes['flare_mix3'])
                nodes.remove(nodes['flare_tonemap2'])
                nodes.remove(nodes['flare_rlayer'])
            except:
                pass
            try:
                nodes.remove(nodes['flare_mask1'])
                nodes.remove(nodes['flare_rgb'])
                nodes.remove(nodes['flare_dist1'])
                nodes.remove(nodes['flare_dist2'])
                nodes.remove(nodes['flare_mask2'])
                nodes.remove(nodes['flare_mixc'])
                nodes.remove(nodes['flare_translate'])
                nodes.remove(nodes['flare_alphaover'])
                nodes.remove(nodes['flare_ckey'])
            except:
                pass

        # BW Saturation
        if ef.bw_v != 1:
            try:
                node_bw = nodes['ColorC']
            except:
                node_bw = nodes.new(type='CompositorNodeColorCorrection')
                node_bw.name = 'ColorC'
            links.new(latest_node.outputs[0], node_bw.inputs[0])
            node_bw.master_saturation = ef.bw_v
            node_bw.location = (pos_x, 0)
            pos_x = pos_x+450
            latest_node = node_bw
        else:
            try:
                nodes.remove(nodes['ColorC'])
            except:
                pass

        # Lens Distortion
        if ef.lens_distort_v != 0:
            try:
                node_lensdist = nodes['LensDist']
            except:
                node_lensdist = nodes.new(type='CompositorNodeLensdist')
                node_lensdist.name = 'LensDist'
            node_lensdist.inputs[1].default_value = ef.lens_distort_v
            links.new(latest_node.outputs[0], node_lensdist.inputs[0])
            node_lensdist.use_fit = True
            node_lensdist.location = (pos_x, 0)
            pos_x = pos_x+200
            latest_node = node_lensdist
        else:
            try:
                nodes.remove(nodes['LensDist'])
            except:
                pass

        # Dispersion
        if ef.dispersion_v != 0:
            try:
                node_distortion = nodes['Dispersion']
            except:
                node_distortion = nodes.new(type='CompositorNodeLensdist')
                node_distortion.name = 'Dispersion'
                node_distortion.label = 'Dispersion'
            links.new(latest_node.outputs[0], node_distortion.inputs[0])
            node_distortion.inputs[2].default_value = ef.dispersion_v
            node_distortion.use_projector = True
            node_distortion.location = (pos_x, 0)
            pos_x = pos_x+200
            latest_node = node_distortion
        else:
            try:
                nodes.remove(nodes['Dispersion'])
            except:
                pass
        # Vignette
        if ef.use_vignette == True:
            # Dist
            try:
                node_vig_dist = nodes['VigDist']
                node_vig_math = nodes['VigMath']
                node_vig_blr = nodes['VigBlur']
                node_vig_mix = nodes['VigMix']
            except:
                node_vig_dist = nodes.new(type='CompositorNodeLensdist')
                node_vig_dist.name = 'VigDist'
                node_vig_dist.inputs[1].default_value = 1

                # Math
                node_vig_math = nodes.new(type='CompositorNodeMath')
                node_vig_math.operation = 'GREATER_THAN'
                node_vig_math.inputs[1].default_value = 0
                links.new(node_vig_dist.outputs[0], node_vig_math.inputs[0])
                node_vig_math.name = 'VigMath'

                # Blur
                node_vig_blr = nodes.new(type='CompositorNodeBlur')
                node_vig_blr.filter_type = 'FAST_GAUSS'
                node_vig_blr.use_relative = True
                node_vig_blr.aspect_correction = 'Y'
                node_vig_blr.factor_x = 20
                node_vig_blr.factor_y = 20
                links.new(node_vig_math.outputs[0], node_vig_blr.inputs[0])
                node_vig_blr.name = 'VigBlur'

                # Mix
                node_vig_mix = nodes.new(type='CompositorNodeMixRGB')
                node_vig_mix.blend_type = 'MULTIPLY'
                node_vig_mix.name = 'VigMix'
                links.new(node_vig_blr.outputs[0], node_vig_mix.inputs[2])

            node_vig_mix.inputs[0].default_value = ef.vignette_v/100
            links.new(latest_node.outputs[0], node_vig_dist.inputs[0])
            links.new(latest_node.outputs[0], node_vig_mix.inputs[1])
            node_vig_dist.location = (pos_x, -200)
            pos_x = pos_x+200
            node_vig_math.location = (pos_x, -200)
            pos_x = pos_x+200
            node_vig_blr.location = (pos_x, -200)
            pos_x = pos_x+200
            node_vig_mix.location = (pos_x, 0)
            pos_x = pos_x+200
            latest_node = node_vig_mix
        else:
            try:
                nodes.remove(nodes['VigDist'])
                nodes.remove(nodes['VigMath'])
                nodes.remove(nodes['VigBlur'])
                nodes.remove(nodes['VigMix'])
            except:
                pass

        # Cinematic Borders
        if ef.use_cinematic_border == True:
            img_x = scene.render.resolution_x
            img_y = scene.render.resolution_y
            try:
                img = bpy.data.images['cinematic_border']
            except:
                img = bpy.ops.image.new(
                    name="cinematic_border", width=img_x, height=img_y)
                img = bpy.data.images['cinematic_border']
                for area in bpy.context.screen.areas:
                    if area.type == 'IMAGE_EDITOR':
                        rend = bpy.data.images['Render Result']
                        area.spaces.active.image = rend
            res_per = scene.render.resolution_percentage/100
            try:
                node_cb_img = nodes['Img sky']
                node_cb_trans1 = nodes['imgsky trans1']
                node_cb_trans2 = nodes['imgsky trans2']
                node_cb_alpha1 = nodes['imgsky alpha1']
                node_cb_alpha2 = nodes['imgsky alpha2']
            except:
                node_cb_img = nodes.new(type='CompositorNodeImage')
                node_cb_img.name = 'Img sky'
                node_cb_trans1 = nodes.new(type='CompositorNodeTransform')
                links.new(node_cb_img.outputs[0], node_cb_trans1.inputs[0])
                node_cb_trans1.name = 'imgsky trans1'
                node_cb_trans2 = nodes.new(type='CompositorNodeTransform')
                links.new(node_cb_img.outputs[0], node_cb_trans2.inputs[0])
                node_cb_trans2.name = 'imgsky trans2'
                node_cb_alpha1 = nodes.new(type='CompositorNodeAlphaOver')
                links.new(node_cb_trans1.outputs[0], node_cb_alpha1.inputs[2])
                node_cb_alpha1.name = 'imgsky alpha1'
                node_cb_alpha2 = nodes.new(type='CompositorNodeAlphaOver')
                node_cb_alpha2.name = 'imgsky alpha2'
                links.new(node_cb_alpha1.outputs[0], node_cb_alpha2.inputs[1])
                links.new(node_cb_trans2.outputs[0], node_cb_alpha2.inputs[2])
            node_cb_img.image = img
            node_cb_trans1.inputs[4].default_value = res_per
            node_cb_trans2.inputs[4].default_value = res_per
            node_cb_img.location = (pos_x-200, -400)
            node_cb_trans1.location = (pos_x, -200)
            pos_x = pos_x+200
            node_cb_trans2.location = (pos_x, -350)
            node_cb_alpha1.location = (pos_x, 0)
            pos_x = pos_x+200
            node_cb_alpha2.location = (pos_x, 0)
            pos_x = pos_x+200
            ma = (img_y*res_per)-(img_y*res_per)*ef.cinematic_border_v/2
            node_cb_trans1.inputs[2].default_value = ma
            node_cb_trans2.inputs[2].default_value = -ma
            links.new(latest_node.outputs[0], node_cb_alpha1.inputs[1])
            latest_node = node_cb_alpha2
        else:
            try:
                nodes.remove(nodes['Img sky'])
                nodes.remove(nodes['imgsky trans1'])
                nodes.remove(nodes['imgsky trans2'])
                nodes.remove(nodes['imgsky alpha1'])
                nodes.remove(nodes['imgsky alpha2'])
            except:
                pass

        # Split Image
        if ef.split_image == True:
            try:
                node_split_alpha = nodes['split alpha']
                node_split_mask = nodes['split mask']
            except:
                node_split_alpha = nodes.new(type='CompositorNodeAlphaOver')
                node_split_alpha.name = 'split alpha'
                node_split_mask = nodes.new(type='CompositorNodeBoxMask')
                node_split_mask.name = 'split mask'
                links.new(
                    node_split_mask.outputs[0], node_split_alpha.inputs[0])
                links.new(CIn.outputs[0], node_split_alpha.inputs[1])
            node_split_alpha.location = (pos_x, 150)
            node_split_mask.location = (pos_x-200, 250)
            pos_x = pos_x+200
            node_split_mask.x = -(1-(ef.split_v/100))
            node_split_mask.width = 2
            node_split_mask.height = 2
            links.new(latest_node.outputs[0], node_split_alpha.inputs[2])
            latest_node = node_split_alpha
        else:
            try:
                nodes.remove(nodes['split alpha'])
                nodes.remove(nodes['split mask'])
            except:
                pass

        # Flip image
        if ef.use_flip == True:
            try:
                node_flip = nodes['efFlip']
            except:
                node_flip = nodes.new(type='CompositorNodeFlip')
                node_flip.name = 'efFlip'
            node_flip.location = (pos_x, 0)
            pos_x = pos_x+200
            links.new(latest_node.outputs[0], node_flip.inputs[0])
            latest_node = node_flip
        else:
            try:
                nodes.remove(nodes['efFlip'])
            except:
                pass
        # Output
        links.new(latest_node.outputs[0], COut.inputs[0])
        COut.location = (pos_x, 0)

        # Transoarent Sky
        if ef_use_sky == False and s_sky == False:
            bpy.context.scene.render.film_transparent = True
            s_sky = True
            self.report({'INFO'}, "Re-render Required")
        elif ef_use_sky == True and s_sky == True:
            bpy.context.scene.render.film_transparent = False
            s_sky = False
            self.report({'INFO'}, "Re-render Required")
        return {'FINISHED'}


class EASYFX_OT_UpdateRenderOperator(bpy.types.Operator):
    '''Update and Re-render'''
    bl_idname = "object.update_render_operator"
    bl_label = "Update and Re-render Operator"

    def execute(self, context):
        bpy.ops.object.update_operator()
        bpy.ops.render.render('INVOKE_DEFAULT')
        return {'FINISHED'}


class EASYFX_OT_ResetSettingsOperator(bpy.types.Operator):
    '''Reset all settings'''
    bl_idname = "object.reset_settings_operator"
    bl_label = "Reset Settings"

    def execute(self, context):
        ef = bpy.context.scene.easyfx
        ef.use_auto_update = True
        # Filters
        ef.use_vignette = False
        ef.vignette_v = 70
        ef.use_glow = False
        ef.glow_em = False
        ef.glow_v = 1
        ef.use_streaks = False
        ef.streaks_em = False
        ef.streaks_v = 1
        ef.streaks_n = 4
        ef.streaks_d = 0
        ef.sharpen_v = 0
        ef.soften_v = 0

        # Blurs
        ef.use_speedb = False
        ef.motionb_v = 1
        ef.use_dof = False
        ef.dof_v = 50

        # Color
        ef.bw_v = 1
        ef.contrast_v = 0
        ef.brightness_v = 0
        ef.shadows_v = (1, 1, 1)
        ef.midtones_v = (1, 1, 1)
        ef.highlights_v = (1, 1, 1)
        ef.check_v = (1, 1, 1)

        # Distort / Lens
        ef.use_flip = False
        ef.lens_distort_v = 0
        ef.dispersion_v = 0
        ef.use_flare = False
        ef.flare_type = 'Fixed'
        ef.flare_c = (1, 0.3, 0.084, 1)
        ef.flare_x = 0
        ef.flare_y = 0
        ef.flare_streak_intensity = 0.002
        ef.flare_streak_lenght = 1
        ef.flare_streak_angle = 0
        ef.flare_streak_streaks = 12
        ef.flare_glow = 0.03
        ef.flare_ghost = 1
        ef.flare_layer = (False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False, True, False, False, False, False)
        ef.flaret_streak_intensity = 0.03
        ef.flaret_streak_lenght = 1.5
        ef.flaret_streak_angle = 0
        ef.flaret_streak_streaks = 12
        ef.flaret_glow = 0.1
        ef.flaret_ghost = 1.5
        ef.flare_center_size = 20

        # World
        ef.use_mist = False
        ef.mist_sky = True
        ef.mist_offset = 0
        ef.mist_size = 0.01
        ef.mist_min = 0
        ef.mist_max = 1
        ef.mist_color = (1, 1, 1, 1)

        # Settings
        ef.use_cinematic_border = False
        ef.cinematic_border_v = 0.4
        ef.use_transparent_sky = False
        ef.use_cel_shading = False
        ef.cel_thickness = 1
        ef.split_image = False
        ef.split_v = 50
        ef.use_image_sky = False
        ef.image_sky_img = ""
        ef.image_sky_x = 0
        ef.image_sky_y = 0
        ef.image_sky_angle = 0
        ef.image_sky_scale = 1
        ef.layer_index = 0
        bpy.ops.object.update_operator()
        return {'FINISHED'}
