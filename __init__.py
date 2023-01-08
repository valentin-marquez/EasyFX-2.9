# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy, math
from bpy.utils import register_class, unregister_class

from .settings import MySettings
from .EasyFX_pnl import EASYFX_PT_UpdatePanel, EASYFX_PT_FilterPanel, EASYFX_PT_BlurPanel, EASYFX_PT_ColorPanel, EASYFX_PT_LensPanel, EASYFX_PT_WorldPanel, EASYFX_PT_StylePanel, EASYFX_PT_SettingPanel
from .EasyFX_op import EASYFX_OT_UpdateOperator, EASYFX_OT_UpdateRenderOperator, EASYFX_OT_ResetSettingsOperator
bl_info = {
    "name": "EasyFX",
    "description": "Do post-production in the Image Editor",
    "author": "Nils Soderman (rymdnisse) & DoubleZ (2.8 port) & Nozz (2.9 port)",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
    "location": "UV/Image Editor > Properties Shelf (N)",
    "warning": "",
    "category": "Render"
}

classes = (
    MySettings,
    EASYFX_PT_UpdatePanel,
    EASYFX_PT_FilterPanel,
    EASYFX_PT_BlurPanel,
    EASYFX_PT_ColorPanel,
    EASYFX_PT_LensPanel,
    EASYFX_PT_WorldPanel,
    EASYFX_PT_StylePanel,
    EASYFX_PT_SettingPanel,
    EASYFX_OT_UpdateOperator,
    EASYFX_OT_UpdateRenderOperator,
    EASYFX_OT_ResetSettingsOperator
)


def register():
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.easyfx = bpy.props.PointerProperty(type=MySettings)


        

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.easyfx
