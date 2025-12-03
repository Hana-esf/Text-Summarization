# Use Node.js to build the React app
FROM node:18 AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Use a basic HTTP server to serve the app
FROM node:18

WORKDIR /app

COPY --from=build /app/build /app/build

RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "5000"]

EXPOSE 5000
