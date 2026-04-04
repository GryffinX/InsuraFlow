# Build stage
FROM node:20-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM node:20-slim

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./
COPY --from=builder /app/build ./build

EXPOSE 3000

ENV NODE_ENV=production
CMD ["node", "build"]
