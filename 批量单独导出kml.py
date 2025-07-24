# -*- coding: utf-8 -*-

import tkinter.messagebox as messagebox
import os
import tkinter as tk
from tkinter import filedialog, ttk
import geopandas as gpd
import simplekml

# 目标文件夹路径的路径变量
shapefile_pathr = ""
# 导出 JPG 文件的路径变量
output_directory2 = ""

def select_target_folder():
    global shapefile_path, shapefile_pathr
    shapefile_path = filedialog.askopenfilename(filetypes=[("Shapefile", "*.shp")], title=u"选择目标shp文件")
    shapefile_pathr = shapefile_path
    folder_label.config(text=u"目标文件路径: " + shapefile_path)

    # 读取 Shapefile 并获取字段名
    gdf = gpd.read_file(shapefile_path)
    field_names = list(gdf.columns)

    # 更新下拉列表的值
    field_combo['values'] = field_names

def select_target_folder2():
    global output_directory, output_directory2
    output_directory = filedialog.askdirectory()
    output_directory2 = output_directory
    folder_label2.config(text=u"目标KML文件路径: " + output_directory)

def export_polygons_to_kml():
    # 获取用户选择的字段名和地理形状类型
    field_name = field_combo.get()
    shape_type = shape_combo.get()

    # 读取 Shapefile
    gdf = gpd.read_file(shapefile_pathr)

    # 如果数据的坐标参考系统 (CRS) 不是 EPSG:4326（WGS84），则进行转换
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    # 遍历 GeoDataFrame 中的所有地理形状
    for index, row in gdf.iterrows():
        # 创建一个新的 KML 对象
        kml = simplekml.Kml()

        # 获取当前的地理形状
        shape = row.geometry

        # 根据用户选择的地理形状类型来将地理形状添加到 KML
        if shape_type == '面':
            kml.newpolygon(name=f"Polygon_{index}", outerboundaryis=list(shape.exterior.coords))
        elif shape_type == '线':
            kml.newlinestring(name=f"Line_{index}", coords=list(shape.coords))

        # 使用用户选择的字段名来命名 KML 文件
        kml_file_name = os.path.join(output_directory2, f"{row[field_name]}.kml")

        # 保存 KML 文件
        kml.save(kml_file_name)

    # 在所有操作完成后显示消息框
    messagebox.showinfo("完成", "所有KML文件导出完成")

# 创建GUI窗口
root = tk.Tk()
root.title("SHP文件批量转KML(pangsen)")

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的宽度和高度
window_width = 700
window_height = 300

# 计算窗口的位置
x = (screen_width - window_width) / 2
y = (screen_height - window_height) / 2

# 设置窗口位置和大小
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

# 创建 "选择字段" 标签
field_label = tk.Label(root, text="选择字段: ")
field_label.place(relx=0.1, rely=0.6, anchor=tk.CENTER)

# 创建字段选择下拉列表
field_combo = ttk.Combobox(root)
field_combo.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

# 创建 "选择形状类型" 标签
shape_label = tk.Label(root, text="选择形状类型: ")
shape_label.place(relx=0.1, rely=0.7, anchor=tk.CENTER)

# 创建形状类型下拉列表
shape_combo = ttk.Combobox(root, values=["面", "线"])
shape_combo.place(relx=0.3, rely=0.7, anchor=tk.CENTER)

# 创建选择目标文件夹按钮
select_button = tk.Button(root, text="选择目标shp文件", command=select_target_folder)
select_button.place(relx=0.2, rely=0.4, anchor=tk.CENTER)

# 导出目标文件夹按钮
select_button2 = tk.Button(root, text="导出目标文件夹", command=select_target_folder2)
select_button2.place(relx=0.2, rely=0.2, anchor=tk.CENTER)

# 创建显示目标文件夹路径的标签
folder_label = tk.Label(root, text="选择目标shp文件路径: ")
folder_label.place(relx=0.6, rely=0.4, anchor=tk.CENTER)

# 创建显示导出路径的标签
folder_label2 = tk.Label(root, text="导出文件夹路径: ")
folder_label2.place(relx=0.6, rely=0.2, anchor=tk.CENTER)

# 创建导出按钮
export_button = tk.Button(root, text="开始导出", command=export_polygons_to_kml)
export_button.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

# 运行主循环
root.mainloop()
