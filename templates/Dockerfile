FROM node:alpine

WORKDIR /templates

COPY * ./

RUN npm install

COPY . .

EXPOSE 8549

CMD [ "npm", "run", "dev" ]