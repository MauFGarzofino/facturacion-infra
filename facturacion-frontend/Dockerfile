# 1. Build del frontend
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# 2. Servir archivos estáticos con NGINX
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Reemplazar el default.conf con nuestra configuración para SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
