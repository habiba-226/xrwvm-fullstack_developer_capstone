# Set the working directory inside the database folder
WORKDIR /app/database

# Copy package.json and package-lock.json first for better caching
COPY package.json ./ 
COPY package-lock.json ./ 

# Install dependenciesa
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 3030

# Command to run the application
CMD ["node", "app.js"]
