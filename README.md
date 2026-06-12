# RBAC 权限管理系统

> 基于 Django 5 + Vue 3 的前后端分离权限管理系统，支持 JWT 鉴权、动态路由、角色-菜单-权限精细化管控

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.2-brightgreen.svg)](https://vuejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docs.docker.com/compose/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF.svg)](https://github.com/features/actions)

**在线地址**: [http://123.56.116.79/#/login](http://123.56.116.79/#/login)（测试账号：admin / 123456）

## ✨ 核心特性

- 🔐 **JWT 鉴权** — 自定义中间件统一鉴权，无状态 Token，支持过期自动刷新
- 👤 **用户管理** — 用户增删改查、头像上传、角色授权、状态启停、密码重置
- 🎭 **角色管理** — 角色 CRUD，支持按角色分配菜单/按钮级权限
- 📋 **菜单权限** — 目录/菜单/按钮三级权限树，支持动态路由生成，排序和图标自定义
- 🔢 **验证码** — 登录图形验证码，Redis 缓存（300s TTL），base64 返回
- 📦 **前后端分离** — Vue 3 + Element Plus 前端，Django REST Framework 后端，Nginx 反向代理
- 🐳 **Docker 部署** — 4 服务编排（backend / frontend / db / redis），一键启动
- 🚀 **CI/CD** — GitHub Actions 自动测试 + SSH 远程部署到阿里云

## 🛠️ 技术栈

### 后端 (Backend)

| 技术 | 版本 | 用途 |
|------|------|------|
| Django | 5.2 | Web 框架 |
| Django REST Framework | 3.16 | 序列化 / API 视图 |
| djangorestframework-jwt | — | JWT 签发与验证 |
| Gunicorn | 23 | WSGI 生产服务器 |
| MySQL | 8.0 | 关系型数据库 |
| Redis | 7 | 缓存 / 会话 / 验证码 |
| django-redis | — | Redis 缓存后端 |
| django-cors-headers | — | 跨域处理 |
| mysqlclient | — | MySQL 驱动 |
| Pillow | — | 图片处理（头像） |

### 前端 (Frontend)

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.2 | 渐进式框架 |
| Vue Router | 4 | SPA 路由 |
| Vuex | 4 | 状态管理 |
| Element Plus | 2.2 | UI 组件库 |
| Axios | — | HTTP 客户端 |
| Nginx | alpine | 静态资源 + 反向代理 |

### 基础设施

| 技术 | 用途 |
|------|------|
| Docker Compose | 容器编排（4 服务） |
| GitHub Actions | CI/CD 自动测试与部署 |
| 阿里云 ECS | 生产环境托管 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 16+
- MySQL 8.0
- Redis 7
- Docker & Docker Compose（可选，用于容器化部署）

### Docker 一键部署（推荐）

```bash
# 1. 克隆项目
git clone <repository_url>
cd django_projects

# 2. 构建并启动所有服务（backend + frontend + db + redis）
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 访问
# 前端: http://localhost
# 后端 API: http://localhost:8000
```

### 本地开发

#### 后端

```bash
# 1. 进入后端目录
cd python_admin

# 2. 创建虚拟环境并激活
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库（确保 MySQL 已运行，创建数据库 db_admin）
# 编辑 python_admin/settings.py 或设置环境变量：
#   DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=db_admin DB_USER=root DB_PASSWORD=your_password

# 5. 执行迁移
python manage.py migrate --noinput

# 6. 启动开发服务器
python manage.py runserver
```

#### 前端

```bash
# 1. 进入前端目录
cd vue_admin

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run serve
```

### 访问服务

- **前端界面**: [http://localhost:8080](http://localhost:8080)（开发模式） / [http://localhost](http://localhost)（Docker 模式）
- **后端 API**: [http://localhost:8000](http://localhost:8000)

## 📡 API 接口

### 用户模块 `/user/`

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 登录 | POST | `/user/login` | JWT 登录，返回 Token |
| 验证码 | GET | `/user/captcha` | 获取图形验证码（Redis） |
| 查询列表 | POST | `/user/search` | 分页查询用户列表 |
| 新增/修改 | POST | `/user/save` | 保存用户信息 |
| 查询/删除 | GET / DELETE | `/user/action` | 按 ID 查询或删除 |
| 修改密码 | POST | `/user/updateUserPwd` | 修改当前用户密码 |
| 重置密码 | POST | `/user/resetPassword` | 管理员重置他人密码 |
| 上传头像 | POST | `/user/updateAvatar` | 更新用户头像 |
| 上传图片 | POST | `/user/uploadImage` | 通用图片上传 |
| 状态切换 | POST | `/user/status` | 启用/禁用用户 |
| 授权角色 | POST | `/user/grantRole` | 为用户分配角色 |
| 用户名查重 | POST | `/user/check` | 检查用户名是否重复 |

### 角色模块 `/role/`

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 全部角色 | GET | `/role/listAll` | 查询所有角色 |
| 分页查询 | POST | `/role/search` | 按条件分页查询 |
| 新增/修改 | POST | `/role/save` | 保存角色信息 |
| 查询/删除 | GET / DELETE | `/role/action` | 按 ID 查询或删除 |
| 角色菜单 | GET | `/role/menus` | 查询角色拥有的菜单 |
| 授权菜单 | POST | `/role/grant` | 为角色分配菜单权限 |

### 菜单模块 `/menu/`

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 菜单树 | GET | `/menu/treeList` | 获取完整菜单权限树 |
| 新增/修改 | POST | `/menu/save` | 保存菜单信息 |
| 查询/删除 | GET / DELETE | `/menu/action` | 按 ID 查询或删除（仅叶子节点） |

### 认证说明

除以下白名单路径外，所有接口需在 Header 中携带 JWT Token：

```
白名单: /user/login, /user/captcha, /media/*, /api/*
```

```bash
# 请求示例
curl -X POST "http://localhost:8000/user/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: <JWT_TOKEN>" \
  -d '{"pageNum": 1, "pageSize": 10}'
```

## 📁 项目结构

```
django_projects/
├── .github/workflows/deploy.yml      # CI/CD：Push main → 测试 → SSH 远程部署
├── docker-compose.yml                # 4 服务编排（backend / frontend / db / redis）
├── db_admin.sql                      # MySQL 全量导出（含种子数据）
├── README.md                         # 项目说明
│
├── python_admin/                     # Django 后端
│   ├── Dockerfile                    # Python 3.10-slim + Gunicorn
│   ├── manage.py                     # Django CLI
│   ├── requirements.txt              # 生产依赖
│   ├── requirements-test.txt         # 测试依赖（pytest 等）
│   ├── pytest.ini                    # Pytest 配置
│   ├── conftest.py                   # Pytest fixtures
│   ├── media/userAvatar/             # 用户头像上传目录
│   ├── python_admin/                 # Django 项目配置
│   │   ├── settings.py               # 数据库 / Redis / CORS / JWT / 中间件
│   │   ├── urls.py                   # 根路由：/user/ → /role/ → /menu/
│   │   ├── wsgi.py                   # WSGI 入口（Gunicorn）
│   │   └── asgi.py                   # ASGI 入口
│   ├── user/                         # 用户应用
│   │   ├── models.py                 # SysUser 模型
│   │   ├── views.py                  # LoginView / SaveView / SearchView 等
│   │   ├── urls.py                   # 11 个端点
│   │   ├── middleware.py             # JwtAuthenticationMiddleware（核心鉴权）
│   │   └── tests/                    # 用户模块测试
│   ├── role/                         # 角色应用
│   │   ├── models.py                 # SysRole / SysUserRole + Serializers
│   │   ├── views.py                  # SearchView / GrantView 等
│   │   ├── urls.py                   # 6 个端点
│   │   └── tests/                    # 角色模块测试
│   └── menu/                         # 菜单应用
│       ├── models.py                 # SysMenu / SysRoleMenu + Serializers
│       ├── views.py                  # TreeListView / SaveView 等
│       ├── urls.py                   # 3 个端点
│       └── tests/                    # 菜单模块测试
│
├── vue_admin/                        # Vue 3 前端 SPA
│   ├── Dockerfile                    # 多阶段构建：node:18 → nginx:alpine
│   ├── nginx.conf                    # API 代理 + History 模式 + Gzip
│   ├── package.json                  # 依赖声明
│   ├── vue.config.js                 # Vue CLI 配置
│   ├── public/                       # 静态资源
│   ├── src/                          # Vue 源码
│   │   ├── api/                      # API 请求封装
│   │   ├── components/               # 公共组件（SVG 图标等）
│   │   ├── router/                   # 路由配置 + 路由守卫
│   │   ├── store/                    # Vuex 状态管理
│   │   ├── utils/                    # 工具函数（request 封装等）
│   │   └── views/                    # 页面组件
│   └── dist/                         # 生产构建产物
│
└── readme_resources/
    └── framework_graph.png           # 架构图
```

## 🗄️ 数据库模型

所有表使用 `utf8mb4` 字符集，外键采用 `ON DELETE PROTECT`。

| 模型 | 表名 | 用途 | 关键字段 |
|------|------|------|------|
| `SysUser` | `sys_user` | 用户账户 | `id`, `username`(unique), `password`(MD5), `avatar`, `email`, `phonenumber`, `login_date`, `status`(1=启用/0=禁用), `create_time`, `update_time`, `remark` |
| `SysRole` | `sys_role` | 角色 | `id`, `name`, `code`, `create_time`, `update_time`, `remark` |
| `SysMenu` | `sys_menu` | 菜单权限树 | `id`, `name`(unique), `icon`, `parent_id`(自引用), `order_num`, `path`, `component`, `menu_type`(M=目录/C=菜单/F=按钮), `perms`, `create_time`, `update_time`, `remark` |
| `SysUserRole` | `sys_user_role` | 用户↔角色 | `id`, `user_id`(FK), `role_id`(FK) |
| `SysRoleMenu` | `sys_role_menu` | 角色↔菜单 | `id`, `role_id`(FK), `menu_id`(FK) |

### 菜单类型说明

| 类型 | 标识 | 说明 |
|------|------|------|
| 目录 (M) | `menu_type='M'` | 一级导航分组，如「系统管理」 |
| 菜单 (C) | `menu_type='C'` | 具体页面入口，如「用户列表」 |
| 按钮 (F) | `menu_type='F'` | 页面内操作权限，如「新增用户」「删除」 |

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────┐
│                    浏览器                        │
│          http://123.56.116.79/#/login            │
└───────────────────┬─────────────────────────────┘
                    │ HTTP
                    ▼
┌─────────────────────────────────────────────────┐
│              Nginx (Frontend :80)                │
│  静态资源 /      →  /usr/share/nginx/html        │
│  API 请求 /api/  →  proxy_pass backend:8000     │
│  History Mode   →  try_files /index.html        │
└───────────────────┬─────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  Vue 3 SPA      │   │  Gunicorn :8000 │
│  (静态文件)      │   │  Django 5.2     │
│                 │   │  DRF + JWT      │
└─────────────────┘   └───────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │  MySQL 8 │   │  Redis 7 │   │  Media   │
       │  :3306   │   │  :6379   │   │  上传文件  │
       └──────────┘   └──────────┘   └──────────┘
```

### 鉴权流程

1. 用户通过 `/user/login` 登录，获取 JWT Token（含验证码校验）
2. 后续所有请求在 Header 携带 `Authorization: <TOKEN>`
3. `JwtAuthenticationMiddleware` 拦截请求，校验 Token 有效性
4. 白名单路径（`/user/login`, `/user/captcha`, `/media/*`, `/api/*`）跳过鉴权
5. Token 过期或无效返回 401

### 菜单树算法

- **两遍扫描构建**：第一遍遍历所有菜单节点，第二遍根据 `parent_id` 将子节点挂载到父节点
- **根节点筛选**：`parent_id == 0` 的节点作为顶层，按 `order_num` 排序
- **递归嵌套**：目录包含菜单，菜单包含按钮，前端据此生成动态路由

## ⚙️ 配置说明

### 环境变量

Django 通过 `os.environ.get()` 读取配置，Docker 模式下在 `docker-compose.yml` 中注入：

```bash
# 数据库
DB_HOST=db            # Docker 中为服务名，本地为 127.0.0.1
DB_PORT=3306
DB_NAME=db_admin
DB_USER=root
DB_PASSWORD=819924zxc

# Redis
REDIS_LOCATION=redis://redis:6379/1

# Django
DEBUG=False           # 生产环境设为 False
```

### CORS 配置

```python
CORS_ORIGIN_ALLOW_ALL = True        # 允许所有来源（开发环境）
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
```

> ⚠️ **生产环境建议**：将 `CORS_ORIGIN_ALLOW_ALL` 改为 `False`，配置 `CORS_ORIGIN_WHITELIST` 为实际前端域名。

### Nginx 配置

- **API 代理**：`/api/` 请求转发至 `backend:8000/`
- **媒体文件**：`/api/media/` 直接代理到 Django 媒体路由（`^~` 优先匹配，避免被 SPA 拦截）
- **Gzip 压缩**：CSS / JS / JSON / 文本默认开启
- **静态缓存**：图片 / 字体等资源 30 天强缓存

## 🧪 测试

项目使用 **pytest** 作为测试运行器，CI 要求代码覆盖率 ≥ 80%。

```bash
# 进入后端目录
cd python_admin

# 安装测试依赖
pip install -r requirements-test.txt

# 运行所有测试
python -m pytest user/tests/ role/tests/ menu/tests/ --tb=short

# 运行单个模块
python -m pytest user/tests/ -v

# 查看覆盖率报告
python -m pytest user/tests/ role/tests/ menu/tests/ --cov=. --cov-report=html
```

## 🚀 CI/CD 部署流水线

```
Git Push (main) → GitHub Actions
                      ├─ ① 检出代码
                      ├─ ② 安装 Python 3.10
                      ├─ ③ 安装依赖 + 测试依赖
                      ├─ ④ pytest + 覆盖率检查 (≥80%)
                      │
                      └─ ⑤ 测试通过 → SSH 到阿里云
                           ├─ cd /home/zjiaxing/db_admin
                           ├─ git pull origin main
                           ├─ docker-compose up -d
                           ├─ docker-compose restart backend/frontend
                           └─ docker image prune -f
```

## 📝 关键架构约定

1. **Plain Django View** — 所有 View 继承 `django.views.View`，返回 `JsonResponse`（不使用 DRF ViewSet）
2. **Serializer 在 models.py** — 序列化器与模型定义在同一文件
3. **自定义 JWT** — 不使用 Django 内置 auth，通过 `JwtAuthenticationMiddleware` 统一鉴权
4. **MD5 密码** — 密码使用 MD5 哈希（⚠️ 生产环境应升级为 bcrypt/PBKDF2）
5. **无 Django Admin** — `django.contrib.admin` 未在 INSTALLED_APPS 中
6. **Raw SQL 谨慎** — 部分查询使用 `raw()`，修改时注意 SQL 注入风险

## 🐛 常见问题

### 本地开发环境

#### MySQL 连接失败

```bash
# 检查 MySQL 是否运行
mysql -u root -p -e "SHOW DATABASES;"

# 确认数据库存在
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS db_admin DEFAULT CHARSET utf8mb4;"
```

#### Redis 连接失败

```bash
# 检查 Redis 是否运行
redis-cli ping     # 应返回 PONG

# 如果未安装 Redis，可以临时使用本地内存缓存
# 修改 settings.py: 删除 CACHES 配置或将 LOCATION 改为本地地址
```

#### 前端代理跨域

前端开发模式下，修改 `vue_admin/vue.config.js` 中的 proxy 指向后端地址：

```javascript
devServer: {
  proxy: {
    '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true }
  }
}
```

### Docker 环境

#### 端口被占用

```bash
# 检查端口占用
netstat -ano | findstr :80       # Windows
lsof -i :80                       # macOS/Linux

# 停止冲突服务或修改 docker-compose.yml 端口映射
```

#### 数据库迁移失败

```bash
# 进入后端容器执行迁移
docker-compose exec backend python manage.py migrate --noinput
```

#### 容器状态异常

```bash
# 查看容器日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
docker-compose logs redis

# 完全重建
docker-compose down -v
docker-compose up -d --build
```

## 📚 参考资源

- [Django 5.2 文档](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [Vue 3 文档](https://vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
