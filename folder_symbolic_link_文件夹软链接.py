bl_info = {
    "name": "文件夹软链接",
    "author": "Corvo, 岑轩漠",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "File",
}

import bpy
import os


class FolderSymbolicLinkProp(bpy.types.PropertyGroup):
    input_path: bpy.props.StringProperty(subtype = 'DIR_PATH')
    output_path: bpy.props.StringProperty(subtype = 'DIR_PATH')

class UpdateSymbolicLink(bpy.types.Operator):
    bl_idname = "scene.update_symbolic_link"
    bl_label = "更新软链接"
    bl_description = "Update Symbolic Link"
    
    def execute(self, context):
        input_path = bpy.context.scene.folder_symbolic_link.input_path
        output_path = bpy.context.scene.folder_symbolic_link.output_path

            # 如果输入路径不存在
        if not os.path.exists(input_path):
            self.report({'INFO'}, "请选择一个存在的'输入路径'!")

        else:
            # 获取原文件夹名称
            split_list = input_path[:-1].split('\\')
            default_folder_name = split_list[-1] 
            print(default_folder_name)  

            # 输出路径改名
            output_path = output_path + default_folder_name + "\\"

            if output_path == input_path:
                self.report({'INFO'}, "'目标路径'不能是'输入路径'父级!换个'输出路径'吧。")

            else:
                # 为避开权限问题，调用windows命令
                if os.path.exists(output_path):
                    rmdir_command = f'rmdir "{output_path}"' # ""括住路径，避免路径空格
                    os.system(rmdir_command)   # 清理旧路径

                mklink_command = f'mklink /j "{output_path}" "{input_path}"'
                os.system(mklink_command)    # 新建软链接
                self.report({'INFO'}, "软链接已更新。")

        return {'FINISHED'}

class FolderSymbolicLinkPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "文件夹软链接"
    bl_idname = "VIEW3D_PT_Folder_Symbolic_Link"
    bl_label = "文件夹软链接"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.folder_symbolic_link, "input_path", text="输入路径")
        layout.prop(context.scene.folder_symbolic_link, "output_path", text="输出路径")
        
        layout = self.layout
        layout.operator("scene.update_symbolic_link", icon = "DECORATE_LINKED")
        
def register():
    bpy.utils.register_class(FolderSymbolicLinkProp)
    bpy.types.Scene.folder_symbolic_link = bpy.props.PointerProperty(type = FolderSymbolicLinkProp)

    bpy.utils.register_class(UpdateSymbolicLink)
    bpy.utils.register_class(FolderSymbolicLinkPanel)

    print("'文件夹软链接'插件   已注册")

def unregister():
    del bpy.types.Scene.folder_symbolic_link
    bpy.utils.unregister_class(FolderSymbolicLinkProp)

    bpy.utils.unregister_class(UpdateSymbolicLink)
    bpy.utils.unregister_class(FolderSymbolicLinkPanel)

    print("'文件夹软链接'插件   已注销")