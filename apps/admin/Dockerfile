# ColourPages Control Center — production image
# Build from repo root: docker build -f apps/admin/Dockerfile -t colourpages-admin .

FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat

FROM base AS deps
WORKDIR /app/apps/admin
COPY apps/admin/package.json apps/admin/package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app/apps/admin
COPY apps/admin/package.json apps/admin/package-lock.json ./
RUN npm ci
COPY apps/admin/ ./
COPY catalog /catalog
COPY data /data
ENV CATALOG_DIR=/catalog/books
ENV DATA_DIR=/data/books
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV CATALOG_DIR=/catalog/books
ENV DATA_DIR=/data/books
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Standalone Next.js server
COPY --from=builder --chown=nextjs:nodejs /app/apps/admin/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/admin/.next/static ./apps/admin/.next/static

# Catalog + book artifacts (mount volumes over these in production for persistence)
COPY --chown=nextjs:nodejs catalog /catalog
COPY --chown=nextjs:nodejs data /data

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

CMD ["node", "apps/admin/server.js"]
