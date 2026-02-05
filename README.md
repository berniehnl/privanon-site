# Privanon.com - Defense-Grade Communications Security

**Privanon LLC** is a defense technology company specializing in secure communications and identity protection. This repository contains the source code for the static corporate website.

## 🚀 Features

- **Defense-Grade Design:** High-contrast, dark mode aesthetic tailored for the defense and intelligence sector.
- **Responsive UI:** Fully responsive layout using modern CSS Grid and Flexbox.
- **Dynamic Content:**
  - Automated copyright year updates.
  - "Rolling Rendezvous" terminology standardized across all pages.
  - Interactive radar visualization in the Technology section.
- **Operational Security:**
  - **Zero Tracking:** No external analytics or tracking scripts.
  - **Secure Contact:** PHP-based form handler (`contact.php`) with AJAX submission and error handling.
  - **Privacy:** Self-contained static assets; no dependency on public CDNs for critical functionality.

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3 (Variables), Vanilla JavaScript (ES6+).
- **Backend:** PHP (for contact form processing).
- **Automation:** Python scripts for generating "Insight" articles via Anthropic API.

## 📂 Project Structure

```
privanon-site/
├── index.html          # Main landing page
├── insights.html       # Articles/Blog index
├── leadership.html     # Leadership team bio
├── styles.css          # Main stylesheet
├── script.js           # Frontend logic & animations
├── contact.php         # Server-side form handler
├── scripts/            # Python automation tools
│   ├── generate_article.py
│   └── mission_control.py
└── insight-*.html      # Individual article pages
```

## ⚡ Deployment

This site is designed for static hosting environments (e.g., Hostinger, Netlify, GitHub Pages) with PHP support required only for the contact form.

### Local Development
Simply open `index.html` in your browser. No build step is required.

### Content Updates
To add new Insight articles, run the generator script (requires Anthropic API key):
```bash
cd scripts
python3 generate_article.py
```

## 📄 License

&copy; 2026 Privanon LLC. All rights reserved.
*ITAR and export control regulations may apply to Privanon products and services.*
