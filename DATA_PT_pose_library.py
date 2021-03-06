# 「プロパティ」エリア > 「アーマチュアデータ」タブ > 「ポーズライブラリ」パネル
# "Propaties" Area > "Armature" Tab > "Pose Library" Panel

import bpy
from bpy.props import *

################
# オペレーター #
################

class MoveActivePose(bpy.types.Operator):
	bl_idname = "poselib.move_active_pose"
	bl_label = "Move Pose"
	bl_description = "Move the pose up or down in the active Pose Library"
	bl_options = {'REGISTER'}

	is_up : BoolProperty(name="To Up", default=False)

	@classmethod
	def poll(cls, context):
		if (not context.object):
			return False
		if (not context.object.pose_library):
			return False
		if (len(context.object.pose_library.pose_markers) < 2):
			return False
		return True

	def execute(self, context):
		pose_markers = context.object.pose_library.pose_markers
		source = pose_markers.active
		if (not self.is_up):
			if (pose_markers.active_index < len(pose_markers)-1):
				target = pose_markers[pose_markers.active_index+1]
				pose_markers.active_index += 1
			else:
				return {'CANCELLED'}
		else:
			if (0 < pose_markers.active_index):
				target = pose_markers[pose_markers.active_index-1]
				pose_markers.active_index -= 1
			else:
				return {'CANCELLED'}
		for data_name in dir(source):
			if (data_name[0] != "_" and "rna" not in data_name):
				temp_source = source.__getattribute__(data_name)
				temp_target = target.__getattribute__(data_name)
				source.__setattr__(data_name, temp_target)
				target.__setattr__(data_name, temp_source)
		return {'FINISHED'}

class MoveActivePoseMost(bpy.types.Operator):
	bl_idname = "poselib.move_active_pose_most"
	bl_label = "Move Pose to Top / Bottom"
	bl_description = "Move the pose to top or bottom of the active pose library"
	bl_options = {'REGISTER'}

	is_top : BoolProperty(name="Move to Top", default=False)

	@classmethod
	def poll(cls, context):
		if (not context.object):
			return False
		if (not context.object.pose_library):
			return False
		if (len(context.object.pose_library.pose_markers) < 2):
			return False
		return True

	def execute(self, context):
		pose_markers = context.object.pose_library.pose_markers
		if (not self.is_top):
			for i in range(len(pose_markers)-pose_markers.active_index):
				bpy.ops.poselib.move_active_pose(is_up=False)
		else:
			for i in range(pose_markers.active_index):
				bpy.ops.poselib.move_active_pose(is_up=True)
		return {'FINISHED'}

################
# クラスの登録 #
################

classes = [
	MoveActivePose,
	MoveActivePoseMost
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
		if (context.object):
			if (context.object.pose_library):
				if (len(context.object.pose_library.pose_markers)):
					sp = self.layout.split(factor=0.15)
					row = sp.row()
					row.alignment = 'CENTER'
					row.operator(MoveActivePose.bl_idname, icon='TRIA_UP', text="").is_up = True
					row.operator(MoveActivePose.bl_idname, icon='TRIA_DOWN', text="").is_up = False
					row = sp.row()
					row.operator(MoveActivePoseMost.bl_idname, icon='TRIA_UP_BAR', text="Move to Top").is_top = True
					row.operator(MoveActivePoseMost.bl_idname, icon='TRIA_DOWN_BAR', text="Move to Bottom").is_top = False
	if (context.preferences.addons[__name__.partition('.')[0]].preferences.use_disabled_menu):
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
