### Python 权限管理系统实战项目 (Django5 + Vue3)

## 1. 项目简介

本项目是一套基于 **Django 5** 和 **Vue 3** 开发的前后端分离权限管理系统。项目定位为高级 Python 就业实战课程，旨在提高开发者在前后端分离架构下的实战水平 。系统通过 **JWT (JSON Web Token)** 技术实现状态无关的身份验证，并提供了完整的用户、角色、权限管理功能 。

## 2. 技术栈

### 后端 (Backend)

- **核心框架**: Django 5.0

- **API 框架**: Django Rest Framework (DRF)

- **身份验证**: JWT (djangorestframework-jwt)

- **数据库**: MySQL 8.0

- **缓存**: Redis

- **跨域处理**: django-cors-headers

### 前端 (Frontend)

- **核心框架**: Vue 3.2

- **UI 组件库**: Element Plus

- **网络请求**: Axios

- **状态管理**: Vuex

- **路由管理**: Vue Router

---

## 3. 项目架构图

项目采用经典的前后端分离三层架构设计：

![](.\readme_resources\framework_graph.png)

项目逻辑流说明 ：

1. **鉴权层**：前端登录获取 JWT Token，后续请求均在 Header 中携带 Token 。后端通过自定义中间件 `JwtAuthenticationMiddleware` 进行统一鉴权 。

2. **路由层**：后端采用多模块分发，主 `urls.py` 将请求分发至 `user`、`role`、`menu` 等子模块 。

3. **数据层**：利用 DRF 的 `Serializers` 实现模型对象（SysUser）与 JSON 数据之间的相互转换，解决序列化问题 。

---

## 4. 功能模块

- **登录认证**: 支持基于 JWT 的登录验证、MD5 加密 。

- **用户管理**: 实现用户信息的增删改查及角色授权 。

- **角色管理**: 实现角色信息的增删改查及权限分配 。

- **权限管理**: 菜单和权限的增删改查，支持动态路由生成 。

- **高级功能**: 包含登录验证码、Redis 缓存、路由守卫、自定义 SVG 图标组件等 。

---

## 5. 项目目录结构

Plaintext

```
python222_admin2/
├── menu/               # 菜单/权限模块 
├── role/               # 角色模块 
├── user/               # 用户模块 
│   ├── middleware.py   # 自定义 JWT 鉴权中间件 
│   ├── serializers.py  # DRF 序列化器 
│   └── models.py       # 用户实体类 (SysUser) 
├── python222_admin2/   # 项目配置中心 [cite: 6]
│   ├── settings.py     # 数据库、中间件、CORS 配置 [cite: 4, 7, 24]
│   └── urls.py         # 总路由分发 [cite: 6]
└── manage.py           # 项目管理脚本 [cite: 4]
```

---

## 6. 快速开始

### 后端环境搭建

1. **创建数据库**: 在 MySQL 8 中创建名为 `db_admin2` 的数据库 。

2. **安装依赖**:
   
   Bash
   
   ```
   pip install django djangorestframework djangorestframework-jwt django-cors-headers mysqlclient
   ```

3. **执行迁移**:
   
   Bash
   
   ```
   python manage.py makemigrations user
   python manage.py migrate user
   ```

4. **运行项目**: `python manage.py runserver` 。

### 前端环境搭建

1. **安装 Node.js**: 推荐版本 16 。

2. **安装依赖**: `npm install` 。

3. **启动开发服务器**: `npm run serve`
