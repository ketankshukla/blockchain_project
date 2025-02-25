# 🛠️ Frontend Setup

<div style="background-color: #f6f8fa; padding: 15px; border-radius: 8px; border-left: 5px solid #24292e;">

This document provides instructions for setting up the frontend development environment for the blockchain application.

</div>

## 📋 Prerequisites

Before setting up the frontend environment, ensure you have the following installed:

- Python 3.8+ (already required for backend)
- Node.js 16+ (for frontend tooling)
- npm or yarn (package managers)

## 📁 Project Structure

The frontend will be organized within the following structure:

```
frontend/
├── static/                # Static assets
│   ├── css/               # CSS files
│   │   └── tailwind.css   # Tailwind CSS
│   ├── js/                # JavaScript files
│   │   ├── components/    # UI components
│   │   ├── services/      # API services
│   │   └── app.js         # Main application
│   └── images/            # Image assets
├── templates/             # Flask templates
│   ├── base.html          # Base template
│   ├── components/        # Reusable components
│   └── pages/             # Page templates
└── routes.py              # Flask routes
```

## 🚀 Initial Setup

### 1. Create Frontend Directories

Create the necessary directory structure for the frontend:

```powershell
# Navigate to project root
cd e:\projects\blockchain_project\refactored

# Create frontend directories
mkdir -p frontend/static/css
mkdir -p frontend/static/js/components
mkdir -p frontend/static/js/services
mkdir -p frontend/static/images
mkdir -p frontend/templates/components
mkdir -p frontend/templates/pages
```

### 2. Set Up Tailwind CSS

Install and configure Tailwind CSS for styling:

```powershell
# Initialize npm project
npm init -y

# Install Tailwind CSS and dependencies
npm install tailwindcss postcss autoprefixer postcss-cli

# Initialize Tailwind CSS
npx tailwindcss init
```

Create a `postcss.config.js` file:

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

Update the `tailwind.config.js` file:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./frontend/templates/**/*.html",
    "./frontend/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3f51b5',
        secondary: '#f50057',
        success: '#4caf50',
        warning: '#ff9800',
        error: '#f44336',
      },
    },
  },
  plugins: [],
}
```

Create a source CSS file for Tailwind:

```css
/* frontend/static/css/tailwind.src.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom components */
@layer components {
  .btn {
    @apply px-4 py-2 rounded font-semibold focus:outline-none focus:ring-2 transition-colors;
  }
  
  .btn-primary {
    @apply bg-primary text-white hover:bg-opacity-90 focus:ring-primary focus:ring-opacity-50;
  }
  
  .btn-secondary {
    @apply bg-secondary text-white hover:bg-opacity-90 focus:ring-secondary focus:ring-opacity-50;
  }
  
  /* Add more custom components */
}
```

Add build script to `package.json`:

```json
"scripts": {
  "build:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css"
}
```

### 3. Set Up Alpine.js

Install Alpine.js for reactive components:

```powershell
# Install Alpine.js
npm install alpinejs
```

Create a main JavaScript file to initialize Alpine.js:

```javascript
// frontend/static/js/app.js
import Alpine from 'alpinejs';

// Make Alpine available globally
window.Alpine = Alpine;

// Start Alpine
Alpine.start();

// Global app state
document.addEventListener('alpine:init', () => {
  Alpine.store('app', {
    darkMode: localStorage.getItem('darkMode') === 'true',
    
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('darkMode', this.darkMode);
      document.documentElement.classList.toggle('dark', this.darkMode);
    },
    
    init() {
      // Apply dark mode on page load if enabled
      document.documentElement.classList.toggle('dark', this.darkMode);
    }
  });
});
```

### 4. Create Base HTML Template

Create a base HTML template that will be extended by other pages:

```html
<!-- frontend/templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blockchain App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/tailwind.css') }}">
    <script defer src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block head %}{% endblock %}
</head>
<body class="bg-gray-100 dark:bg-gray-900 min-h-screen" x-data x-bind:class="{'dark': $store.app.darkMode}">
    <header class="bg-white dark:bg-gray-800 shadow">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-xl font-bold text-primary">Blockchain App</a>
            
            <nav class="hidden md:flex space-x-4">
                <a href="/dashboard" class="text-gray-700 dark:text-gray-300 hover:text-primary">Dashboard</a>
                <a href="/wallets" class="text-gray-700 dark:text-gray-300 hover:text-primary">Wallets</a>
                <a href="/transactions" class="text-gray-700 dark:text-gray-300 hover:text-primary">Transactions</a>
                <a href="/contacts" class="text-gray-700 dark:text-gray-300 hover:text-primary">Contacts</a>
                <a href="/blockchain" class="text-gray-700 dark:text-gray-300 hover:text-primary">Blockchain</a>
            </nav>
            
            <div class="flex items-center space-x-2">
                <button @click="$store.app.toggleDarkMode()" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700">
                    <svg x-show="!$store.app.darkMode" class="w-5 h-5 text-gray-700" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                    </svg>
                    <svg x-show="$store.app.darkMode" class="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
                    </svg>
                </button>
                
                <div class="relative" x-data="{ isOpen: false }">
                    <button @click="isOpen = !isOpen" class="flex items-center text-gray-700 dark:text-gray-300 hover:text-primary">
                        <span>Account</span>
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    </button>
                    
                    <div x-show="isOpen" @click.away="isOpen = false" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-10">
                        <a href="/profile" class="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Profile</a>
                        <a href="/settings" class="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Settings</a>
                        <a href="/logout" class="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Logout</a>
                    </div>
                </div>
                
                <button class="md:hidden p-2" @click="mobileMenuOpen = !mobileMenuOpen">
                    <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>
        </div>
        
        <!-- Mobile menu -->
        <div x-data="{ mobileMenuOpen: false }" x-show="mobileMenuOpen" class="md:hidden bg-white dark:bg-gray-800 shadow-md">
            <nav class="flex flex-col px-4 py-2">
                <a href="/dashboard" class="py-2 text-gray-700 dark:text-gray-300 hover:text-primary">Dashboard</a>
                <a href="/wallets" class="py-2 text-gray-700 dark:text-gray-300 hover:text-primary">Wallets</a>
                <a href="/transactions" class="py-2 text-gray-700 dark:text-gray-300 hover:text-primary">Transactions</a>
                <a href="/contacts" class="py-2 text-gray-700 dark:text-gray-300 hover:text-primary">Contacts</a>
                <a href="/blockchain" class="py-2 text-gray-700 dark:text-gray-300 hover:text-primary">Blockchain</a>
            </nav>
        </div>
    </header>
    
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="bg-white dark:bg-gray-800 shadow-inner mt-auto">
        <div class="container mx-auto px-4 py-6">
            <p class="text-center text-gray-600 dark:text-gray-400">© 2025 Blockchain App. All rights reserved.</p>
        </div>
    </footer>
    
    <!-- Toast notification container -->
    <div id="toast-container" class="fixed bottom-4 right-4 z-50"></div>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

### 5. Set Up Flask Routes

Create a basic routes file for the frontend:

```python
# frontend/routes.py
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route('/')
def index():
    return render_template('pages/index.html')

@frontend.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')

@frontend.route('/wallets')
def wallets():
    return render_template('pages/wallets.html')

@frontend.route('/wallets/<address>')
def wallet_details(address):
    return render_template('pages/wallet_details.html', address=address)

@frontend.route('/transactions')
def transactions():
    return render_template('pages/transactions.html')

@frontend.route('/contacts')
def contacts():
    return render_template('pages/contacts.html')

@frontend.route('/blockchain')
def blockchain():
    return render_template('pages/blockchain.html')

@frontend.route('/login')
def login():
    return render_template('pages/login.html')

@frontend.route('/register')
def register():
    return render_template('pages/register.html')

@frontend.route('/settings')
def settings():
    return render_template('pages/settings.html')
```

## 🔧 Development Workflow

### Building CSS

To build the CSS for development:

```powershell
# Build Tailwind CSS
npm run build:css
```

### Setting Up a Development Environment

1. Start the FastAPI backend server
2. Start the Flask frontend server
3. Rebuild CSS when making style changes

You can create a batch file to simplify the development workflow:

```powershell
# Create dev.bat script

@echo off
echo Starting development environment...
echo.

:: Terminal 1 - FastAPI backend
start cmd /k "cd e:\projects\blockchain_project\refactored && python -m api.main"

:: Terminal 2 - Flask frontend
start cmd /k "cd e:\projects\blockchain_project\refactored && python -m frontend.app"

:: Terminal 3 - CSS watcher
start cmd /k "cd e:\projects\blockchain_project\refactored && npm run watch:css"

echo Development environment started!
```

Add a watch script to `package.json`:

```json
"scripts": {
  "build:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css",
  "watch:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css --watch"
}
```

## 📦 Production Setup

For production, you'll want to optimize the frontend assets:

### 1. Install Production Dependencies

```powershell
# Install production dependencies
npm install cssnano --save-dev
```

### 2. Update PostCSS Config for Production

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  }
}
```

### 3. Add Production Build Script

Add to `package.json`:

```json
"scripts": {
  "build:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css",
  "watch:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css --watch",
  "build:prod": "NODE_ENV=production npm run build:css"
}
```

### 4. Set Up Webpack for JavaScript Bundling (Optional)

For larger applications, you might want to use Webpack for JavaScript bundling:

```powershell
# Install Webpack and dependencies
npm install webpack webpack-cli babel-loader @babel/core @babel/preset-env --save-dev
```

Create a `webpack.config.js` file:

```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  entry: './frontend/static/js/app.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'frontend/static/js/dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  devtool: process.env.NODE_ENV === 'production' ? false : 'inline-source-map'
};
```

Add Webpack scripts to `package.json`:

```json
"scripts": {
  "build:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css",
  "watch:css": "postcss frontend/static/css/tailwind.src.css -o frontend/static/css/tailwind.css --watch",
  "build:js": "webpack",
  "watch:js": "webpack --watch",
  "build:prod": "NODE_ENV=production npm run build:css && NODE_ENV=production npm run build:js"
}
```

## 🚧 Next Steps

After setting up the basic frontend structure, proceed with:

1. Creating individual page templates
2. Implementing API services
3. Developing UI components
4. Setting up authentication flow
5. Connecting frontend to the FastAPI backend

Refer to the [API Integration](API_INTEGRATION.md) document for details on connecting to the backend API.
