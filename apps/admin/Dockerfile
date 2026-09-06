# ColourPages Control Center — build from repo root:
#   docker build -f apps/admin/Dockerfile -t colourpages-admin .

FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat

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

RUN apk add --no-cache wget && \
    addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV CATALOG_DIR=/catalog/books
ENV DATA_DIR=/data/books
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

COPY --from=builder --chown=nextjs:nodejs /app/apps/admin/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/admin/.next/static ./.next/static

COPY --chown=nextjs:nodejs catalog /catalog
COPY --chown=nextjs:nodejs data /data

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/api/health || exit 1

CMD ["node", "server.js"]
