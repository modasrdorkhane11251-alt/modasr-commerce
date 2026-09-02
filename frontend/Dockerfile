FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Build application
RUN npm run build

# Create non-root user
RUN addgroup -g 1000 nextuser && \
    adduser -D -u 1000 -G nextuser nextuser && \
    chown -R nextuser:nextuser /app
USER nextuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

# Run application
CMD ["npm", "start"]
