FROM node:18-alpine

WORKDIR /app

# Copy và install backend dependencies
COPY backend/package*.json ./backend/
WORKDIR /app/backend
RUN npm install --production

# Quay lại root để copy tất cả files
WORKDIR /app
COPY . .

# Expose port
EXPOSE 7860

# Chạy server từ thư mục backend
CMD ["node", "backend/server.js"]