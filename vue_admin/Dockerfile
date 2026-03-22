# --- 阶段 1: 构建 ---
# 使用 Node 18 (Vue 3 推荐 LTS 版本)
FROM node:18-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
# 如果是 npm: RUN npm install
# 如果是 yarn: RUN yarn install
# 这里默认用 npm，如果有 package-lock.json 推荐用 ci 加速
RUN npm ci || npm install

# 复制源代码
COPY . .

# 执行构建
# Vue 3 (Vite 或 CLI) 默认输出目录通常都是 dist
RUN npm run build

# --- 阶段 2: 生产运行 ---
FROM nginx:alpine

# 删除 Nginx 默认配置（你已经写了这一行，很好）
RUN rm /etc/nginx/conf.d/default.conf

# 【修改这里】将本地的 nginx.conf 拷贝并重命名为 default.conf
# 这样能确保它完全替代 Nginx 的默认服务器配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 将构建好的 dist 目录复制到 Nginx 静态资源目录
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]