FROM node:20-alpine

WORKDIR /app

COPY package.json package.json
COPY tsconfig.json tsconfig.json
COPY next.config.ts next.config.ts
COPY postcss.config.js postcss.config.js
COPY tailwind.config.ts tailwind.config.ts
COPY src ./src
COPY public ./public
COPY next-env.d.ts next-env.d.ts

RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
