from django.db import models
from rest_framework import serializers

from role.models import SysRole


# Create your models here.

# 系统菜单类
class SysMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="菜单名称")
    icon = models.CharField(max_length=100, null=True, verbose_name="菜单图标")
    parent_id = models.IntegerField(null=True, verbose_name="父菜单ID")
    order_num = models.IntegerField(null=True, verbose_name="显示顺序")
    path = models.CharField(max_length=200, null=True, verbose_name="路由地址")
    component = models.CharField(max_length=255, null=True, verbose_name="组件路径")
    menu_type = models.CharField(max_length=1, null=True, verbose_name="菜单类型（M目录 C菜单 F按钮）")
    perms = models.CharField(max_length=100, null=True, verbose_name="权限标识")
    create_time = models.DateField(null=True, verbose_name="创建时间", )
    update_time = models.DateField(null=True, verbose_name="更新时间")
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    # 重写小于方法，用于后续排序
    def __lt__(self, other):
        return self.order_num < other.order_num

    class Meta:
        db_table = 'sys_menu'


# 序列化
class SysMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    # 获取字菜单的序列化数据列表
    def get_children(self, obj):
        print('111')
        if hasattr(obj, 'children'):
            serializerMenuList: list[SysMenuSerializer2] = list()
            for child in obj.children:
                serializerMenuList.append(SysMenuSerializer2(child).data)
            return serializerMenuList

    class Meta:
        model = SysMenu
        fields = '__all__'


# 子菜单序列化类
class SysMenuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SysMenu
        fields = '__all__'


# 系统角色菜单类
class SysRoleMenu(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(SysRole, on_delete=models.PROTECT)
    menu = models.ForeignKey(SysMenu, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sys_role_menu'


class SysRoleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRoleMenu
        fields = '__all__'
