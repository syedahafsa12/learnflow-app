#!/bin/bash

# Docusaurus Site Configuration Script
# Configures a Docusaurus site with LearnFlow-specific settings

set -e  # Exit on any error

if [ $# -eq 0 ]; then
    echo "Usage: $0 <site_name>"
    exit 1
fi

SITE_NAME=$1
SITE_DIR="./$SITE_NAME"

echo "Configuring Docusaurus site: $SITE_NAME"

if [ -d "$SITE_DIR" ]; then
    cd "$SITE_DIR"
    
    # Update package.json with LearnFlow-specific settings
    if [ -f "package.json" ]; then
        # Backup original
        cp package.json package.json.bak
        
        # Update package.json with new name and description
        jq --arg name "${SITE_NAME}-docs" \
           --arg desc "LearnFlow Documentation Site" \
           '.name = $name | .description = $desc' package.json > tmp_package.json && mv tmp_package.json package.json
    fi
    
    # Create custom CSS if it doesn't exist
    mkdir -p src/css
    if [ ! -f "src/css/custom.css" ]; then
        cat > src/css/custom.css << 'CSS_EOF
/**
 * Any CSS included here will be global. The classic template
 * bundles Infima by default. Infima is a CSS framework designed to
 * work well for content-centric websites.
 */

/* You can override the default Infima variables here. */
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
  --ifm-color-primary-darker: #277148;
  --ifm-color-primary-darkest: #205d3b;
  --ifm-color-primary-light: #33925d;
  --ifm-color-primary-lighter: #359962;
  --ifm-color-primary-lightest: #3cad6e;
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}

/* For readability concerns, you should choose a lighter palette in dark mode. */
[data-theme='dark'] {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: #21af90;
  --ifm-color-primary-darker: #1fa588;
  --ifm-color-primary-darkest: #1a8870;
  --ifm-color-primary-light: #29d5b0;
  --ifm-color-primary-lighter: #32d8b4;
  --ifm-color-primary-lightest: #4fddbf;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}

/* LearnFlow specific styles */
.learnflow-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
  margin-bottom: 2rem;
  color: white;
  text-align: center;
}

.learnflow-feature {
  border-left: 4px solid #667eea;
  padding-left: 1rem;
  margin: 1rem 0;
}
CSS_EOF
    fi
    
    # Create a custom header component if it doesn't exist
    mkdir -p src/components
    cat > src/components/Header.js << 'HEADER_EOF'
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useBaseUrl } from '@docusaurus/useBaseUrl';
import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={clsx('hero learnflow-header', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">LearnFlow Documentation</h1>
        <p className="hero__subtitle">AI-Powered Python Learning Platform</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}
HEADER_EOF

    cat > src/components/Header.module.css << 'MODULE_EOF'
.heroBanner {
  padding: 4rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

@media screen and (max-width: 996px) {
  .heroBanner {
    padding: 2rem;
  }
}

.buttons {
  display: flex;
  align-items: center;
  justify-content: center;
}
MODULE_EOF

    cd ..
    echo "✓ Site $SITE_NAME configured successfully"
else
    echo "✗ Site directory $SITE_DIR does not exist"
    exit 1
fi
