FROM node:20-alpine
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN npm install -g @angular/cli
RUN npm install
ENV NODE_OPTIONS=--openssl-legacy-provider
CMD ["ng", "serve", "--host", "0.0.0.0"]