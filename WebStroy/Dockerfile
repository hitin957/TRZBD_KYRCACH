FROM node:alpine

WORKDIR /templates

COPY * ./

RUN npm install

COPY . .

EXPOSE 6000

CMD [ "npm", "run", "dev" ]