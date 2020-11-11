FROM node:14.8.0-alpine

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package.json .
COPY package-lock.json .
RUN npm install --production
RUN npm install react-scripts@3.4.1 -g

COPY . .
