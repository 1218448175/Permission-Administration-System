import json
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from menu.models import SysMenu, SysMenuSerializer, SysRoleMenu


# Create your views here.
# 构建菜单树
class TreeListView(View):
    def buildTreeMenu(self, sysMenuList):
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            # 寻找子节点
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, 'children'):
                        menu.children = list()
                    menu.children.append(e)

            # 只将最外层菜单加入列表
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        # 返回根节点列表
        return resultMenuList

    def get(self, request):
        menuQuerySet = SysMenu.objects.order_by('order_num')

        # 构造菜单树
        menuList = self.buildTreeMenu(menuQuerySet)
        # 序列化
        serializerMenuList: list[SysMenuSerializer] = list()

        for sysMenu in menuList:
            serializerMenuList.append(SysMenuSerializer(sysMenu).data)

        return JsonResponse({'code': 200, 'treeList': serializerMenuList})


# 添加或修改菜单
class SaveView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        if data['id'] == -1:  # 添加
            obj_sysMenu = SysMenu(name=data['name'], icon=data['icon'],
                                  parent_id=data['parent_id'], order_num=data['order_num'], path=data['path'],
                                  component=data['component'], menu_type=data['menu_type'], perms=data['perms'],
                                  remark=data['remark'])
            obj_sysMenu.create_time = datetime.now().date()
            obj_sysMenu.save()
        else:  # 修改
            obj_sysMenu = SysMenu(id=data['id'], name=data['name'], icon=data['icon'],
                                  parent_id=data['parent_id'], order_num=data['order_num'], path=data['path'],
                                  component=data['component'], menu_type=data['menu_type'], perms=data['perms'],
                                  remark=data['remark'], create_time=data['create_time'],
                                  update_time=data['update_time'])
            obj_sysMenu.update_time = datetime.now().date()
            obj_sysMenu.save()
        return JsonResponse({'code': 200})


# 菜单基本操作
class ActionView(View):
    def get(self, request):
        """
        根据id获取权限信息
        :param request:
        :return:
        """
        id = request.GET.get('id')
        menu_obj = SysMenu.objects.get(id=id)
        return JsonResponse({'code': 200, 'menu': SysMenuSerializer(menu_obj).data})

    def delete(self, request):
        """
        删除菜单
        :param request:
        :return:
        """
        id = json.loads(request.body.decode('utf-8'))

        # 只删叶子菜单
        if SysMenu.objects.filter(parent_id=id).count() > 0:
            return JsonResponse({'code': 500, 'msg': '请先删除子菜单'})
        else:
            SysRoleMenu.objects.filter(menu_id=id).delete()  # 先删关联表
            SysMenu.objects.get(id=id).delete()  # 再删菜单表
            return JsonResponse({'code': 200})
