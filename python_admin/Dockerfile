# backend/Dockerfile
FROM python:3.10-slim

# 1. 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. 设置容器内的工作目录为 /app
WORKDIR /app

# 3. 安装系统依赖 (为了编译 mysqlclient 和 pillow)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. 复制依赖文件
# 因为 Dockerfile 和 requirements.txt 在同一级，所以直接写 .
COPY requirements.txt .

# 5. 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 6. 复制整个项目代码
# "." 代表当前目录（即包含 manage.py, menu, user 等文件夹的根目录）
# 它们会被复制到容器内的 /app 目录下
COPY . .

# 7. 暴露端口
EXPOSE 8000

# 8. 启动命令
# 关键点：这里的项目名必须是你截图中的 'python_admin' (包含 settings.py 的那个文件夹)
# 格式：python_admin.wsgi:application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "python_admin.wsgi:application"]