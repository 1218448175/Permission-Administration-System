from django.urls import path

from user.views import TestView, JwtTestView, LoginView, SaveView, PwdView, AvatarView, ImageView, SearchView, \
    ActionView, CheckView, PasswordView, StatusView, GrantRoleView, CaptchaView

urlpatterns = [
    path('test', TestView.as_view(), name='test'),  # 测试接口，as_view()调用view()方法, 将请求转发到get/post/put
    path('jwt_test', JwtTestView.as_view(), name='jwt_test'),  # jwt测试
    path('login', LoginView.as_view(), name='login'),  # 用户登录
    path('save', SaveView.as_view(), name='save'),  # 用户修改
    path('updateUserPwd', PwdView.as_view(), name='updateUserPwd'),  # 修改密码
    path('updateAvatar', AvatarView.as_view(), name='updateUserPwd'),  # 更新头像
    path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 上传图像
    path('search', SearchView.as_view(), name='search'),  # 用户信息分页查询
    path('action', ActionView.as_view(), name='action'),  # 用户信息操作
    path('check', CheckView.as_view(), name='check'),  # 用户名查重
    path('resetPassword', PasswordView.as_view(), name='resetPassword'),  # 重置密码
    path('status', StatusView.as_view(), name='status'),  # 改变状态
    path('grantRole', GrantRoleView.as_view(), name='grantRole'),  # 授权角色
    path('captcha', CaptchaView.as_view(), name='captcha'),  # 验证码
]
