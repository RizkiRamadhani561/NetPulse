FROM node:24-alpine AS development
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY package.json ./
RUN npm install --no-audit --no-fund
COPY . .
RUN mkdir -p /app/.next && chown -R node:node /app
USER node
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]

FROM node:24-alpine AS build
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY package.json ./
RUN npm install --no-audit --no-fund
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
