# Stage 1: Build the React application
FROM node:14.5.0-alpine as build

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
ENV PUBLIC_URL /

# Copy package.json and yarn.lock
COPY package.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of your frontend-react directory into the image
COPY . ./

# Build the React application
RUN yarn run build

# Stage 2: Serve the app using Nginx
FROM nginx:stable

# Copy the built app from the first stage into Nginx's serving directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
