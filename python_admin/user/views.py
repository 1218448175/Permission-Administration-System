import base64
import hashlib
import json
import random
import uuid
from datetime import datetime
from io import BytesIO

from captcha.image import ImageCaptcha
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from menu.models import SysMenu, SysMenuSerializer
from python_admin import settings
from role.models import SysRole, SysUserRole
from user.models import SysUser


# Create your views here.
class TestView(View):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None or token == '':
            return JsonResponse({'code': 401, 'info': '无token'})
        else:
            userList_obj = SysUser.objects.all()  # 获取模型中所有的实例
            print(userList_obj, type(userList_obj))
            userList_dict = userList_obj.values()  # 转存字典,但仍然是查询类
            print(userList_dict, type(userList_dict))
            userList = list(userList_dict)  # 转为列表
            print(userList, type(userList))
            return JsonResponse({'code': 200, 'info': '测试', 'data': userList})


class JwtTestView(View):
    def get(self, request):
        user = SysUser.objects.get(username='python222', password='123456')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 将用户对象传进去，获取该对象属性集
        payload = jwt_payload_handler(user)
        # 将属性集编码为jwt格式字符串
        token = jwt_encode_handler(payload)

        return JsonResponse({'code': 200, 'token': token})


# 登录逻辑
class LoginView(View):

    # 构建菜单树
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

    def post(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')

        code = request.GET.get('code')
        uu_id = request.GET.get('uuid')
        captcha = cache.get(uu_id)
        print("captcha:", captcha)

        if captcha == '' or captcha is None or captcha.lower() != code.lower():  # 判断验证码
            return JsonResponse({'code': 500, 'info': '验证码错误'})

        try:
            user = SysUser.objects.get(username=username, password=hashlib.md5(password.encode()).hexdigest())  # md5加密
            print(type(user))
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 将用户对象传递进去，获取该对象属性值
            payload = jwt_payload_handler(user)
            # 将属性值编码为jwt格式字符串
            token = jwt_encode_handler(payload)

            # 通过SQL获取改用户的所有角色
            roleList = SysRole.objects.raw(
                "SELECT id, name FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id=" + str(
                    user.id) + ")")

            # 角色名称列表
            roles_ls = []

            # 获取roleList中元素对应的所有菜单，使用集合去重
            menuSet = set()
            for role in roleList:
                roles_ls.append(role.name)
                # 获取单个角色的所有菜单
                menuList = SysMenu.objects.raw(
                    "SELECT * FROM sys_menu WHERE id IN (SELECT menu_id FROM sys_role_menu WHERE role_id=" + str(
                        role.id) + ")")
                print("menuList", menuList)
                menuSet.update(menuList)

            # 拼接为字符串，方便展示
            roles_str = ','.join(roles_ls)
            print(roles_str)

            menuList = list(menuSet)  # set转list
            sorted_menuList = sorted(menuList, key=lambda x: x.order_num)  # 根据order_num排序
            print(sorted_menuList)
            # 构造菜单树
            sysMenuList: list[SysMenu] = self.buildTreeMenu(sorted_menuList)
            print(sysMenuList)

            serializerMenuList = list()
            # 将菜单树序列化，存入列表
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)


        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'info': '用户名或密码错误'})
        return JsonResponse({'code': 200, 'token': token, 'info': '登录成功', 'user': SysUserSerializer(user).data,
                             'menuList': serializerMenuList, 'roles': roles_str})


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        fields = '__all__'


# 修改个人信息
class SaveView(View):
    def post(self, request):
        # 拿到前端post请求
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        if data['id'] == -1:  # 添加
            obj_sysUser = SysUser(username=data['username'], password=data['password'],
                                  email=data['email'], phonenumber=data['phonenumber'],
                                  status=data['status'],
                                  remark=data['remark'])
            obj_sysUser.create_time = datetime.now().date()
            obj_sysUser.avatar = 'default.jpg'
            # 密码默认123456
            obj_sysUser.password = hashlib.md5('123456'.encode()).hexdigest()
            obj_sysUser.save()
        else:  # 修改
            # 根据post信息修改用户信息
            obj_SysUser = SysUser(id=data['id'], username=data['username'], password=data['password'],
                                  avatar=data['avatar'], email=data['email'], phonenumber=data['phonenumber'],
                                  login_date=data['login_date'], status=data['status'], create_time=data['create_time'],
                                  update_time=data['update_time'], remark=data['remark'])
            obj_SysUser.update_time = datetime.now().date()
            obj_SysUser.save()
        return JsonResponse({'code': 200})


# 修改密码逻辑部分
class PwdView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        id = data['id']
        oldPassword = data['oldPassword']
        newPassword = data['newPassword']
        obj_user = SysUser.objects.get(id=id)
        if obj_user.password == hashlib.md5(oldPassword.encode()).hexdigest():
            obj_user.password = hashlib.md5(newPassword.encode()).hexdigest()
            obj_user.update_time = datetime.now().date()
            obj_user.save()

            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'code': 500, 'errorInfo': '原密码错误'})


# 图像上传逻辑
class ImageView(View):
    def post(self, request):
        # 获取文件
        file = request.FILES.get('avatar')
        print('file:', file)
        if file:
            file_name = file.name

            # 获取文件后缀名并重命名文件
            suffixName = file_name.split('.')[-1]
            new_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + suffixName

            file_path = str(settings.MEDIA_ROOT) + '\\userAvatar\\' + new_file_name

            print('file_path', file_path)
            print('new', new_file_name)

            try:
                # 写入文件
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({'code': 200, 'title': new_file_name})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500, 'errorInfo': '上传失败'})


# 头像修改逻辑
class AvatarView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.update_time = datetime.now().date()
        obj_user.save()
        return JsonResponse({'code': 200, 'user': SysUserSerializer(obj_user).data})


# 用户数据分页查询
class SearchView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        query = data['query']
        pageNum = data['pageNum']  # 当前页
        pageSize = data['pageSize']  # 每页大小

        userListPage = Paginator(SysUser.objects.filter(username__icontains=query), pageSize).page(pageNum)  # 分页,数据集类型

        obj_user = userListPage.object_list.values()  # 转成字典
        userList = list(obj_user)  # 转成列表

        # 查询每个用户的角色列表，并以字典形式存入列表， 作为user的动态属性
        for user in userList:
            userId = user['id']
            roleList = SysRole.objects.raw(
                "SELECT id, name FROM sys_role WHERE id IN (SELECT role_id FROM sys_user_role WHERE user_id=" + str(
                    userId) + ")")

            roleDictList = []
            for role in roleList:
                roleDict = {}
                roleDict['name'] = role.name
                roleDict['id'] = role.id
                roleDictList.append(roleDict)

            user['roleList'] = roleDictList

        total = SysUser.objects.filter(username__icontains=query).count()
        return JsonResponse({'code': 200, 'total': total, 'userList': userList})


# 基本操作类ActionView get方式 根据id获取用户信息
class ActionView(View):
    def get(self, request):
        id = request.GET.get('id')
        sysUser = SysUser.objects.get(id=id)
        return JsonResponse({'code': 200, 'user': SysUserSerializer(sysUser).data})

    # 删除数据请求
    def delete(self, request):
        idList = json.loads(request.body.decode('utf-8'))
        print(idList)
        # 先删除关联表，不会报错
        SysUserRole.objects.filter(user__id__in=idList).delete()
        SysUser.objects.filter(id__in=idList).delete()

        return JsonResponse({'code': 200})


# 验证用户名是否重复
class CheckView(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        print("username=", username)
        if SysUser.objects.filter(username=username).exists():
            return JsonResponse({'code': 500})
        else:
            return JsonResponse({'code': 200})


# 重置密码
class PasswordView(View):
    def get(self, request):
        id = request.GET.get('id')
        user_obj = SysUser.objects.get(id=id)
        user_obj.password = hashlib.md5('123456'.encode()).hexdigest()
        user_obj.update_time = datetime.now().date()
        user_obj.save()
        return JsonResponse({'code': 200})


# 设置状态
class StatusView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        id = data['id']
        user_obj = SysUser.objects.get(id=id)
        user_obj.status = data['status']
        user_obj.save()

        return JsonResponse({'code': 200})


class GrantRoleView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user_id = data['user_id']
        roleIdList = data['roleIds']
        print('user_id', user_id)
        print('roleIdList', roleIdList)
        SysUserRole.objects.filter(user_id=user_id).delete()  # 先删除用户角色
        for roleId in roleIdList:
            # 逐个创建授权角色
            userRole = SysUserRole(user_id=user_id, role_id=roleId)
            userRole.save()

        return JsonResponse({'code': 200})


class CaptchaView(View):
    def get(self, request):
        # 验证码字母表
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # 随机取四位作为验证码
        data = ''.join(random.sample(characters, 4))
        print('data', data)
        # 生成图片
        captcha = ImageCaptcha()
        # 使用二进制存储
        imageData: BytesIO = captcha.generate(data)
        # 转换成base64字符串，方便存储
        base64_str = base64.b64encode(imageData.getvalue()).decode()
        print(type(base64_str), base64_str)
        # 随机生成唯一key
        random_uuid = uuid.uuid4()
        # 存入缓存
        cache.set(random_uuid, data, timeout=300)
        return JsonResponse(
            {'code': 200, 'base64str': "data:image/png;base64," + base64_str, 'uuid': random_uuid})
