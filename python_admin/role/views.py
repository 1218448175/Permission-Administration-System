import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from menu.models import SysRoleMenu
from role.models import SysRole, SysRoleSerializer, SysUserRole


# Create your views here.
# 查询所有角色信息
class ListAllView(View):
    def get(self, request):
        roles = SysRole.objects.all().values()  # 转成字典
        roleList = list(roles)  # 把外层容器换成列表
        return JsonResponse({'code': 200, 'roleList': roleList})


# 根据角色名搜索数据
class SearchView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        query = data['query']
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小

        roleListPage = Paginator(SysRole.objects.filter(name__icontains=query), pageSize).page(pageNum)  # 分页,数据集类型

        obj_role = roleListPage.object_list.values()  # 转成字典
        roleList = list(obj_role)  # 转成列表
        total = SysRole.objects.filter(name__icontains=query).count()
        return JsonResponse({'code': 200, 'total': total, 'roleList': roleList})


# 添加或修改角色信息
class SaveView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        if (data['id'] == -1):  # 添加
            obj_role = SysRole(name=data['name'], code=data['code'], remark=data['remark'])
            obj_role.create_time = datetime.now().date()
            obj_role.save()
        else:  # 修改
            obj_sysRole = SysRole(id=data['id'], name=data['name'], code=data['code'],
                                  remark=data['remark'], create_time=data['create_time'],
                                  update_time=data['update_time'])
            obj_sysRole.update_time = datetime.now().date()
            obj_sysRole.save()

        return JsonResponse({'code': 200})


class ActionView(View):
    def get(self, request):
        # 根据获取角色数据
        id = request.GET.get('id')
        role_obj = SysRole.objects.get(id=id)
        return JsonResponse({'code': 200, 'role': SysRoleSerializer(role_obj).data})

    def delete(self, request):
        # 以id列表形式存储
        idList = json.loads(request.body.decode('utf-8'))

        # 先删除角色关联表
        SysRoleMenu.objects.filter(role_id__in=idList).delete()
        SysUserRole.objects.filter(role_id__in=idList).delete()

        # 删除角色
        SysRole.objects.filter(id__in=idList).delete()

        return JsonResponse({'code': 200})


# 根据角色查询菜单权限
class MenusView(View):
    def get(self, request):
        id = request.GET.get('id')
        menuList = SysRoleMenu.objects.filter(role_id=id).values("menu_id")
        menuIdList = [m['menu_id'] for m in menuList]

        return JsonResponse({'code': 200, 'menuIdList': menuIdList})


# 角色权限授权
class GrantView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        role_id = data['id']
        menuIdList = data['menuIdList']

        # 先删除角色菜单关联表中所有数据
        SysRoleMenu.objects.filter(role_id=role_id).delete()

        # 再将选中权限授权
        for menuId in menuIdList:
            roleMenu = SysRoleMenu(role_id=role_id, menu_id=menuId)
            roleMenu.update_time = datetime.now().date()
            roleMenu.save()

        return JsonResponse({'code': 200})
