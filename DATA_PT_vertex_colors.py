# 「プロパティ」エリア > 「オブジェクトデータ」タブ > 「頂点カラー」パネル
# "Propaties" Area > "Object Data" Tab > "Vertex Colors" Panel

import bpy
from bpy.props import *

################
# オペレーター #
################

class MoveActiveVertexColor(bpy.types.Operator):
	bl_idname = "object.move_active_vertex_color"
	bl_label = "Move Vertex Color"
	bl_description = "Move up or down the active vertex color layer"
	bl_options = {'REGISTER', 'UNDO'}

	items = [
		('UP', "To Up", "", 1),
		('DOWN', "To Down", "", 2),
		]
	mode : EnumProperty(items=items, name="Direction", default="UP")

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		if (obj):
			if (obj.type == 'MESH'):
				if (2 <= len(obj.data.vertex_colors)):
					return True
		return False

	def execute(self, context):
		obj = context.active_object
		me = obj.data
		if (self.mode == 'UP'):
			if (me.vertex_colors.active_index <= 0):
				return {'CANCELLED'}
			target_index = me.vertex_colors.active_index - 1
		elif (self.mode == 'DOWN'):
			target_index = me.vertex_colors.active_index + 1
			if (len(me.vertex_colors) <= target_index):
				return {'CANCELLED'}
		pre_mode = obj.mode
		bpy.ops.object.mode_set(mode='OBJECT')
		vertex_color = me.vertex_colors.active
		vertex_color_target = me.vertex_colors[target_index]
		for data_name in dir(vertex_color):
			if (data_name[0] != '_' and data_name != 'bl_rna' and data_name != 'rna_type' and data_name != 'data'):
				temp = vertex_color.__getattribute__(data_name)
				temp_target = vertex_color_target.__getattribute__(data_name)
				vertex_color.__setattr__(data_name, temp_target)
				vertex_color_target.__setattr__(data_name, temp)
				vertex_color.__setattr__(data_name, temp_target)
				vertex_color_target.__setattr__(data_name, temp)
		for i in range(len(vertex_color.data)):
			temp = vertex_color.data[i].color[:]
			vertex_color.data[i].color = vertex_color_target.data[i].color[:]
			vertex_color_target.data[i].color = temp[:]
		me.vertex_colors.active_index = target_index
		bpy.ops.object.mode_set(mode=pre_mode)
		return {'FINISHED'}

class VertexColorSet(bpy.types.Operator):
	bl_idname = "object.vertex_color_set"
	bl_label = "Fill Vertex Color"
	bl_description = "Fill the active vertex color layer with the specified color"
	bl_options = {'REGISTER', 'UNDO'}

	color : FloatVectorProperty(name="Vertex Color", default=(1, 1, 1, 1), min=0, max=1, soft_min=0, soft_max=1, step=3, precision=10, subtype='COLOR_GAMMA', size=4)

	@classmethod
	def poll(cls, context):
		obj = context.active_object
		if (obj):
			if (obj.type == 'MESH'):
				if (obj.data.vertex_colors.active):
					return True
		return False

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		obj = context.active_object
		pre_mode = obj.mode
		bpy.ops.object.mode_set(mode='OBJECT')
		me = obj.data
		active_col = me.vertex_colors.active
		for data in active_col.data:
			data.color = self.color
		bpy.ops.object.mode_set(mode=pre_mode)
		return {'FINISHED'}

class AddVertexColorSelectedObject(bpy.types.Operator):
	bl_idname = "object.add_vertex_color_selected_object"
	bl_label = "Add Vertex Colors Together"
	bl_description = "Add vertex colors with specified color and name to the selected objects"
	bl_options = {'REGISTER', 'UNDO'}

	name : StringProperty(name="Name", default="Col")
	color : FloatVectorProperty(name="Vertex Color", default=(1, 1, 1, 1), min=0, max=1, soft_min=0, soft_max=1, step=10, precision=3, subtype='COLOR_GAMMA', size=4)

	@classmethod
	def poll(cls, context):
		for obj in context.selected_objects:
			if (obj.type == 'MESH'):
				return True
		return False

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		for obj in context.selected_objects:
			if (obj.type == "MESH"):
				me = obj.data
				try:
					col = me.vertex_colors[self.name]
				except KeyError:
					col = me.vertex_colors.new(name=self.name)
				for data in col.data:
					data.color = self.color
		return {'FINISHED'}

################
# クラスの登録 #
################

classes = [
	MoveActiveVertexColor,
	VertexColorSet,
	AddVertexColorSelectedObject
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
		row = self.layout.row()
		if (context.active_object.type == 'MESH'):
			if (context.active_object.data.vertex_colors.active):
				sub = row.row(align=True)
				sub.operator(MoveActiveVertexColor.bl_idname, icon='TRIA_UP', text="").mode = 'UP'
				sub.operator(MoveActiveVertexColor.bl_idname, icon='TRIA_DOWN', text="").mode = 'DOWN'
				row.operator(VertexColorSet.bl_idname, icon='BRUSH_DATA', text="Fill Vertices")
				row.operator(AddVertexColorSelectedObject.bl_idname, icon='PLUGIN', text="Add Together")
	if (context.preferences.addons[__name__.partition('.')[0]].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
