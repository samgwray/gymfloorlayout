# The site (Next.js), run with `next start`. Built from the repository root.
FROM node:22-alpine AS build
WORKDIR /srv
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# /api/* is proxied to the planning service on the compose network (next.config.ts).
ENV API_URL=http://api:8100 \
    NEXT_TELEMETRY_DISABLED=1
RUN npm run build && npm prune --omit=dev && rm -rf .next/cache

FROM node:22-alpine
WORKDIR /srv
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    API_URL=http://api:8100
COPY --from=build --chown=node:node /srv/package.json /srv/next.config.ts /srv/tsconfig.json ./
COPY --from=build --chown=node:node /srv/node_modules ./node_modules
COPY --from=build --chown=node:node /srv/.next ./.next
COPY --from=build --chown=node:node /srv/public ./public
USER node
EXPOSE 3100
CMD ["node_modules/.bin/next", "start", "--port", "3100"]
