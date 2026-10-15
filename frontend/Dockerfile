FROM node:24-alpine AS development
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund --fetch-retries=5 --fetch-retry-factor=2 --fetch-retry-mintimeout=10000 --fetch-retry-maxtimeout=120000 --fetch-timeout=300000
COPY . .
RUN mkdir -p /app/.next && chown -R node:node /app
USER node
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]

FROM node:24-alpine AS build
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund --fetch-retries=5 --fetch-retry-factor=2 --fetch-retry-mintimeout=10000 --fetch-retry-maxtimeout=120000 --fetch-timeout=300000
COPY . .
RUN npm run build

FROM node:24-alpine AS production
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
RUN addgroup -S -g 10001 netpulse && adduser -S -u 10001 -G netpulse netpulse
COPY --from=build --chown=netpulse:netpulse /app ./
USER 10001:10001
EXPOSE 3000
CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]
