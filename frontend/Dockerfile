FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application code
COPY . .

# Build for production (or run dev server)
EXPOSE 5173
CMD ["npm", "run", "dev"]
