# 「プロパティ」エリア > 「カーブデータ」タブ > 「シェイプ」パネル
# "Propaties" Area > "Curve" Tab > "Shape" Panel

import bpy
from bpy.props import *

################
# オペレーター #
################

class CopyCurveShapeSetting(bpy.types.Operator):
	bl_idname = "curve.copy_curve_shape_setting"
	bl_label = "Copy Shape Settings"
	bl_description = "Copy active curve's shape settings to other selected curves"
	bl_options = {'REGISTER', 'UNDO'}

	dimensions : BoolProperty(name="Curve type (2D/3D)", default=True)
	resolution_u : BoolProperty(name="Viewport", default=True)
	render_resolution_u : BoolProperty(name="Rendering", default=True)
	fill_mode : BoolProperty(name="Fill Mode", default=True)
	use_fill_deform : BoolProperty(name="Fill Deformed", default=True)
	twist_mode : BoolProperty(name="Twist Method", default=True)
	use_radius : BoolProperty(name="Radius", default=True)
	use_stretch : BoolProperty(name="Stretch", default=True)
	twist_smooth : BoolProperty(name="Smooth", default=True)
	use_deform_bounds : BoolProperty(name="Bounds Clamp", default=True)

	@classmethod
	def poll(cls, context):
		if len(context.selected_objects) >= 2:
			curves = [ob for ob in context.selected_objects if ob.type=='CURVE']
			if len(curves) >= 2:
				return True
		return False

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	def draw(self, context):
		row = self.layout.row()
		column = row.column().box()
		column.label(text="Resolution U")
		column.prop(self, 'resolution_u')
		column.prop(self, 'render_resolution_u')
		column = row.column()
		column.box().prop(self, 'dimensions')
		box = column.box()
		box.prop(self, 'twist_mode')
		box.prop(self, 'twist_smooth')
		row = self.layout.row()
		column = row.column().box()
		column.prop(self, 'fill_mode')
		column.prop(self, 'use_fill_deform')
		column = row.column().box()
		column.prop(self, 'use_radius')
		column.prop(self, 'use_stretch')
		column.prop(self, 'use_deform_bounds')

	def execute(self, context):
		active_ob = context.active_object
		active_curve = active_ob.data
		for ob in context.selected_objects:
			if active_ob.name != ob.name:
				if ob.type == 'CURVE':
					curve = ob.data
					if self.dimensions:
						curve.dimensions = active_curve.dimensions
					if self.resolution_u:
						curve.resolution_u = active_curve.resolution_u
					if self.render_resolution_u:
						curve.render_resolution_u = active_curve.render_resolution_u
					if self.fill_mode:
						curve.fill_mode = active_curve.fill_mode
					if self.use_fill_deform:
						curve.use_fill_deform = active_curve.use_fill_deform
					if self.twist_mode:
						curve.twist_mode = active_curve.twist_mode
					if self.use_radius:
						curve.use_radius = active_curve.use_radius
					if self.use_stretch:
						curve.use_stretch = active_curve.use_stretch
					if self.twist_smooth:
						curve.twist_smooth = active_curve.twist_smooth
					if self.use_deform_bounds:
						curve.use_deform_bounds = active_curve.use_deform_bounds
		return {'FINISHED'}

################
# クラスの登録 #
################

classes = [
	CopyCurveShapeSetting
]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)


################
# メニュー追加 #
################

# メニューのオン/オフの判定
def IsMenuEnable(self_id):
	for id in bpy.context.preferences.addons[__name__.partition('.')[0]].preferences.disabled_menu.split(','):
		if (id == self_id):
			return False
	else:
		return True

# メニューを登録する関数
def menu(self, context):
	if (IsMenuEnable(__name__.split('.')[-1])):
		if eval(f"bpy.ops.{CopyCurveShapeSetting.bl_idname}"):
			self.layout.operator(CopyCurveShapeSetting.bl_idname, icon='COPY_ID')
	if (context.preferences.addons[__name__.partition('.')[0]].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
