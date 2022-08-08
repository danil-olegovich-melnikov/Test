FROM node:14

WORKDIR /app/front

COPY package.json ./
COPY entrypoint.sh ./

RUN npm install

COPY . ./

ENTRYPOINT ["sh", "/app/react_app/entrypoint.sh"]
