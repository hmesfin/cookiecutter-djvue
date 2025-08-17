{% if cookiecutter.use_docker == 'y' -%}
# Development stage
FROM node:{{ cookiecutter.node_version }}-alpine AS development

WORKDIR /app

# Copy package files
COPY frontend/package.json ./
COPY frontend/package-lock.json* ./

# Install dependencies
# Use npm install if package-lock.json doesn't exist (first time setup)
RUN if [ -f package-lock.json ]; then \
        npm ci --prefer-offline --no-audit; \
    else \
        npm install --no-audit --no-fund && npm cache clean --force; \
    fi

# Copy source code
COPY frontend/ .

# Expose port
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Build stage
FROM node:{{ cookiecutter.node_version }}-alpine AS build

WORKDIR /app

# Copy package files
COPY frontend/package.json ./
COPY frontend/package-lock.json* ./

# Install dependencies
# Use npm install if package-lock.json doesn't exist (first time setup)
RUN if [ -f package-lock.json ]; then \
        npm ci --prefer-offline --no-audit; \
    else \
        npm install --no-audit --no-fund && npm cache clean --force; \
    fi

# Copy source code
COPY frontend/ .

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine AS production

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
{%- endif %}