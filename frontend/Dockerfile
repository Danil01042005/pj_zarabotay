# Dockerfile для фронтенда

FROM node:18

WORKDIR /frontend

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./

CMD ["npm", "start"]
