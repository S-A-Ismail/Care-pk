# Multi-stage build keeps the final images lean.
# docker-compose.yml targets the 'dev' stage for local development.
# To build a production image manually:
#   docker build --target production -t care-pk .

# ── Stage 1: dev ──────────────────────────────────────────────
# Used by docker-compose for local development.
# Source files are mounted as a volume (not COPY'd) so edits on the
# host machine are visible inside the container immediately.
FROM node:20-alpine AS dev

WORKDIR /app

# Copy manifests first so this layer is cached. Docker only re-runs
# `npm install` when package.json or package-lock.json actually changes,
# not on every source-file edit.
COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]


# ── Stage 2: builder ──────────────────────────────────────────
# Compiles the Next.js app into the .next/ output directory.
# Not used directly — the production stage copies its output.
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
# `npm ci` (clean install) is stricter than `npm install`:
# it requires package-lock.json and never updates it, making builds reproducible.
RUN npm ci

COPY . .
RUN npm run build


# ── Stage 3: production ───────────────────────────────────────
# Minimal runtime image — no source files, no dev dependencies.
# Only the compiled .next/ output and production node_modules are included.
FROM node:20-alpine AS production

WORKDIR /app
ENV NODE_ENV=production

COPY package.json package-lock.json* ./
# --omit=dev skips devDependencies (TypeScript, ESLint, etc.), shrinking the image.
RUN npm ci --omit=dev

# Copy only the built artefacts from the builder stage, not the full source tree.
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "start"]
