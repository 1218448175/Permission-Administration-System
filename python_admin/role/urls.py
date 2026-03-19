from django.urls import path

from role.views import ListAllView, SearchView, SaveView, ActionView, MenusView, GrantView

urlpatterns = [
    path('listAll', ListAllView.as_view(), name='listAll'),  # 查询所有角色信息
    path('search', SearchView.as_view(), name='search'),  # 根据条件查询角色信息
    path('save', SaveView.as_view(), name='save'),  # 添加或修改角色
    path('action', ActionView.as_view(), name='action'),  # 操作视图
    path('menus', MenusView.as_view(), name='menus'),  # 根据角色查询菜单权限
    path('grant', GrantView.as_view(), name='grant'),  # 授权角色权限
]
