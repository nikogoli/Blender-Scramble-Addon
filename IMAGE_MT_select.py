# 「UVエディター」エリア > 「選択」メニュー
# "UV Editor" Area > "Select" Menu

import bpy
import bmesh
from bpy.props import *

################
# オペレーター #
################

class SelectSeamEdge(bpy.types.Operator):
	bl_idname = "uv.select_seam_edge"
	bl_label = "Select ALL Separated Vertices"
	bl_description = "Select all vertices linked to seam edges and separated when unwrapping"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		activeObj = context.active_object
		me = activeObj.data
		bpy.ops.object.mode_set(mode='OBJECT')
		bm = bmesh.new()
		bm.from_mesh(me)
		uv_lay = bm.loops.layers.uv.active
		use_uv_select_sync = context.scene.tool_settings.use_uv_select_sync
		verts = {}
		for face in bm.faces:
			for loop in face.loops:
				uv = loop[uv_lay].uv
				index = loop.vert.index
				if (str(index) in verts):
					for u in verts[str(index)]:
						if (u == uv[:]):
							break
					else:
						verts[str(index)].append(uv[:])
				else:
					verts[str(index)] = [uv[:]]
		for face in bm.faces:
			for loop in face.loops:
				uv = loop[uv_lay].uv
				vert = loop.vert
				index = vert.index
				if (2 <= len(verts[str(index)])):
					loop[uv_lay].select = True
					if (use_uv_select_sync):
						vert.select = True
		bm.to_mesh(me)
		bm.free()
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}

class SelectLinkedVetex(bpy.types.Operator):
	bl_idname = "uv.select_linked_vertex"
	bl_label = "Select The OTHER Separated Vertices"
	bl_description = "Select other vertices referencing the same part of the mesh as the selected ones do"
	bl_options = {'REGISTER', 'UNDO'}

	keep_pre : BoolProperty(name="Keep Selection", default=True)
	
	def execute(self, context):
		activeObj = context.active_object
		me = activeObj.data
		bpy.ops.object.mode_set(mode='OBJECT')
		bm = bmesh.new()
		bm.from_mesh(me)
		uv_lay = bm.loops.layers.uv.active
		idxs = []
		pre_loops = []
		for face in bm.faces:
			for loop in face.loops:
				index = loop.vert.index
				if loop[uv_lay].select == True:
					idxs.append(index)
					pre_loops.append(loop)
		for face in bm.faces:
			for loop in face.loops:
				if (not self.keep_pre) and (loop in pre_loops):
					loop[uv_lay].select = False
					continue
				index = loop.vert.index
				if index in idxs:
					loop[uv_lay].select = True
		bm.to_mesh(me)
		bm.free()
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}

################
# クラスの登録 #
################

classes = [
	SelectSeamEdge,
	SelectLinkedVetex
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
		self.layout.separator()
		self.layout.operator(SelectSeamEdge.bl_idname, icon="PLUGIN")
		self.layout.operator(SelectLinkedVetex.bl_idname, icon="PLUGIN")
	if (context.preferences.addons[__name__.partition('.')[0]].preferences.use_disabled_menu):
		self.layout.separator()
		self.layout.operator('wm.toggle_menu_enable', icon='CANCEL').id = __name__.split('.')[-1]
