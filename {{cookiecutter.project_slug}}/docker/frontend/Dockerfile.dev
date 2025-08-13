{% if cookiecutter.use_docker == 'y' -%}
# Development Dockerfile for frontend
FROM node:{{ cookiecutter.node_version }}-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git

# Create entrypoint script that handles initial setup
RUN cat > /docker-entrypoint.sh << 'EOF'
#!/bin/sh
set -e

# Wait for package.json to be available
max_attempts=30
attempt=0
while [ ! -f "package.json" ] && [ $attempt -lt $max_attempts ]; do
    echo "Waiting for package.json to be mounted (attempt $((attempt+1))/$max_attempts)..."
    sleep 1
    attempt=$((attempt+1))
done

if [ ! -f "package.json" ]; then
    echo "ERROR: package.json not found after waiting. Please ensure the volume is mounted correctly."
    exit 1
fi

# Always check and install dependencies
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "Installing Node.js dependencies..."
    # Use legacy-peer-deps to handle any remaining conflicts
    npm install --legacy-peer-deps
    echo "Dependencies installed successfully!"
else
    echo "Dependencies already installed, checking for updates..."
    # Quick check if package.json has changed
    npm install --legacy-peer-deps
fi

# Verify vite is installed
if [ ! -f "node_modules/.bin/vite" ]; then
    echo "Vite not found, installing dependencies..."
    npm install --legacy-peer-deps
fi

# Execute the main command
exec "$@"
EOF

RUN chmod +x /docker-entrypoint.sh

# Expose Vite dev server port
EXPOSE 5173

# Use entrypoint to handle setup
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
{%- endif %}