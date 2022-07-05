FROM node:16.15-alpine

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installing dependencies
COPY package*.json .
COPY yarn.lock .
RUN yarn install

# Copying source files
COPY . .

EXPOSE 3000
CMD [ "yarn", "start"]