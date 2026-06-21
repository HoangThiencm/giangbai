FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy source code
COPY . .

# Expose port (Hugging Face Spaces dùng port 7860)
EXPOSE 7860

# Start server
CMD ["node", "server.js"]

