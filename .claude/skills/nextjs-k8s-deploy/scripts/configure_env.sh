#!/bin/bash

# Next.js Environment Configuration Script
# Sets up environment variables and configurations for the application

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <app_name>"
    exit 1
fi

APP_NAME=$1
APP_DIR="./$APP_NAME"

echo "Configuring environment for Next.js application: $APP_NAME"

# Create environment configuration if app exists
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    
    # Create .env.local for local development
    cat > .env.local << ENV_EOF
# LearnFlow Frontend Environment Variables
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_DAPR_HTTP_PORT=3500
NEXT_PUBLIC_DAPR_GRPC_PORT=50001

# Authentication
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:4000
NEXT_PUBLIC_BETTER_AUTH_TOKEN=dev-token-change-in-production

# Feature flags
NEXT_PUBLIC_ENABLE_MONACO_EDITOR=true
NEXT_PUBLIC_ENABLE_CODE_EXECUTION_SANDBOX=true
NEXT_PUBLIC_MAX_CODE_EXECUTION_TIME=5000
ENV_EOF

    # Update next.config.js to include necessary configurations
    if [ -f "next.config.js" ]; then
        # Backup original
        cp next.config.js next.config.js.bak
        
        # Add necessary configurations
        cat > next.config.js << 'NEXT_CONFIG_EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    outputFileTracing: true,
    serverComponentsExternalPackages: ["monaco-editor"],
  },
  output: 'standalone',
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
NEXT_CONFIG_EOF
    else
        # Create a basic next.config.js if it doesn't exist
        cat > next.config.js << 'NEXT_CONFIG_EOF
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    outputFileTracing: true,
    serverComponentsExternalPackages: ["monaco-editor"],
  },
  output: 'standalone',
};

module.exports = nextConfig;
NEXT_CONFIG_EOF
    fi
    
    # Create a basic app layout if it doesn't exist
    mkdir -p src/app
    if [ ! -f "src/app/layout.tsx" ]; then
        cat > src/app/layout.tsx << 'LAYOUT_EOF
import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'LearnFlow - AI-Powered Python Tutor',
  description: 'Interactive Python learning platform with AI tutoring',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
LAYOUT_EOF
    fi
    
    # Create globals.css if it doesn't exist
    if [ ! -f "src/app/globals.css" ]; then
        cat > src/app/globals.css << 'GLOBALS_EOF
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
GLOBALS_EOF
    fi
    
    cd ..
    echo "✓ Environment configured for $APP_NAME"
else
    echo "✗ Application directory $APP_DIR does not exist"
    exit 1
fi
