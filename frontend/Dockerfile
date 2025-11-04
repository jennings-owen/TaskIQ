# Frontend Dockerfile for React Application
# Multi-stage build: Build stage + Production stage with nginx

# Stage 1: Build React application
FROM node:22-alpine AS builder

WORKDIR /app

# Accept build argument for backend URL
ARG REACT_APP_BACK_END_URL=http://localhost:8000
ENV REACT_APP_BACK_END_URL=$REACT_APP_BACK_END_URL

# Copy package files and node_modules from local environment
COPY package*.json ./
COPY node_modules ./node_modules

# Copy application code
COPY . .

# Build production bundle using existing node_modules
# The REACT_APP_BACK_END_URL will be baked into the build
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create non-root user for security
RUN addgroup -g 1000 appgroup && \
    adduser -D -u 1000 -G appgroup appuser && \
    chown -R appuser:appgroup /usr/share/nginx/html && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chown -R appuser:appgroup /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appgroup /var/run/nginx.pid

USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

