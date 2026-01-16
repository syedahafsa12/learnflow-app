# Docusaurus Deployment - Reference Documentation

## Overview
This skill creates and deploys Docusaurus documentation sites to Kubernetes. It's designed to create professional documentation sites for projects like LearnFlow and other applications.

## Architecture
The deployment includes:
- Docusaurus application container with optimized static build
- Nginx web server for serving static assets
- Kubernetes Deployment with health checks
- Service for network access
- Optional Ingress for external access

## Docker Image Optimization

### Multi-Stage Build
The Dockerfile uses a two-stage build process:
1. **Builder**: Build the Docusaurus site with all dependencies
2. **Production**: Serve static assets with optimized Nginx configuration

### Nginx Configuration
Optimized for static site serving:
- Gzip compression for text assets
- Long-term caching for static assets
- SPA routing support
- Security headers
- MIME type optimization

## Docusaurus Configuration

### Site Metadata
Essential configuration options:
- `title`: Site title
- `tagline`: Short description
- `favicon`: Site icon
- `url`: Production URL
- `baseUrl`: Base path for site

### Preset Configuration
The classic preset includes:
- **Docs**: Documentation with sidebar navigation
- **Blog**: Blog functionality
- **Theme**: Customizable appearance

### Theme Configuration
Customizable elements:
- Navbar and footer
- Social media cards
- Syntax highlighting themes
- Custom CSS

## Kubernetes Configuration

### Deployment Strategy
- Single replica for static content
- Conservative resource allocation
- Health checks for availability

### Resource Configuration
Default resource requests and limits:
- CPU Request: 50m
- CPU Limit: 200m
- Memory Request: 128Mi
- Memory Limit: 256Mi

### Service Configuration
- ClusterIP service type (internal access)
- HTTP port 80
- Health check endpoints

## Documentation Structure

### Recommended Sections for LearnFlow
1. **Getting Started**
   - Installation guide
   - Quick start tutorial
   - Prerequisites

2. **Architecture**
   - System design
   - Component diagrams
   - Technology stack

3. **API Documentation**
   - REST API reference
   - Authentication methods
   - Rate limiting

4. **Development**
   - Contributing guide
   - Code style
   - Testing procedures

5. **Deployment**
   - Infrastructure setup
   - Environment variables
   - Scaling guidelines

## Template Variables
The configuration templates use these variables:
- `{{SITE_TITLE}}`: Title of the documentation site
- `{{SITE_TAGLINE}}`: Tagline or subtitle
- `{{SITE_URL}}`: Production URL of the site
- `{{BASE_URL}}`: Base path for the site
- `{{ORGANIZATION_NAME}}`: Organization or company name
- `{{PROJECT_NAME}}`: Project repository name

## Search Integration

### Algolia DocSearch
For full-text search functionality:
- Register site with Algolia DocSearch
- Configure search parameters
- Add search component to navbar

### Local Search
Alternative search implementations:
- Lunr.js integration
- Custom search indexing
- Client-side search functionality

## Plugin System

### Official Plugins
- `@docusaurus/plugin-content-docs`: Documentation content
- `@docusaurus/plugin-content-blog`: Blog content
- `@docusaurus/plugin-content-pages`: Static pages
- `@docusaurus/plugin-sitemap`: Sitemap generation
- `@docusaurus/plugin-google-gtag`: Google Analytics

### Community Plugins
- Versioning for documentation
- Multi-language support
- Custom remark/rehype plugins
- MDX support enhancements

## SEO Optimization

### Meta Tags
Automatic generation of:
- Page titles
- Meta descriptions
- Open Graph tags
- Twitter cards

### Sitemap Generation
- Automatic sitemap.xml creation
- Priority and frequency settings
- Multi-language support

## Internationalization
- Locale configuration
- Translation file management
- Right-to-left language support
- Date/time formatting

## Security Considerations
- Content Security Policy headers
- Cross-origin resource sharing (CORS)
- Secure asset handling
- Input sanitization for Markdown

## Performance Optimization

### Asset Optimization
- Image optimization
- Bundle splitting
- Code splitting
- Lazy loading

### Caching Strategy
- Browser caching headers
- CDN integration
- Asset fingerprinting
- Compression algorithms

## Monitoring and Analytics

### Built-in Metrics
- Page view tracking
- Navigation analytics
- Error reporting
- Performance metrics

### Third-party Integration
- Google Analytics
- Plausible Analytics
- Custom event tracking
- Heatmap tools

## Troubleshooting

### Common Issues
1. **Build failures**: Check dependencies and Node.js version
2. **Routing issues**: Verify base URL configuration
3. **Asset loading**: Check path configurations
4. **Search problems**: Verify search plugin configuration

### Diagnostic Commands
```bash
# Check build output
npm run build

# Local development server
npm run start

# Check Kubernetes resources
kubectl get all -n <namespace>

# View container logs
kubectl logs deployment/<site-name> -n <namespace>
```

## Integration with LearnFlow
For the LearnFlow platform, this skill provides:
- Comprehensive documentation site
- API reference documentation
- Architecture and design documents
- User guides and tutorials
- Developer documentation
- Skill usage instructions