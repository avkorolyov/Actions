FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production --ignore-scripts

COPY public ./public
COPY server.js ./

EXPOSE 4173
CMD ["npm", "start"]

