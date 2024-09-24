# Stage 1: Build
FROM node:20-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js app
RUN npm run build

# Stage 2: Production
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /app/package*.json ./
COPY --from=build /app/.next ./.next/
COPY --from=build /app/public ./
COPY --from=build /app/node_modules ./node_modules

# Set environment variable for production
ENV NODE_ENV=production

# Expose port 3000
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]
# CMD ["sh"] 


