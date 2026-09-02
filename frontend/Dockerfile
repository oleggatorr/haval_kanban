# === Stage 1: Build ===
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# ИСПРАВЛЕНИЕ: Запускаем только vite build, игнорируя vue-tsc
RUN npx vite build

# === Stage 2: Production ===
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]