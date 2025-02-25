# 🔌 API Integration

<div style="background-color: #e6f7ff; padding: 15px; border-radius: 8px; border-left: 5px solid #1890ff;">

This document details how the frontend will integrate with the FastAPI backend endpoints.

</div>

## 📡 API Communication Strategy

### Client-Side API Service

The frontend will use a modular API service structure to communicate with the backend:

```javascript
// api/base.js - Base API client
const API = {
  baseUrl: '/api',
  
  // Get authentication token from local storage
  getToken() {
    return localStorage.getItem('auth_token');
  },
  
  // Default headers for all requests
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  },
  
  // Generic request method
  async request(endpoint, method = 'GET', data = null) {
    const url = `${this.baseUrl}/${endpoint}`;
    
    const options = {
      method,
      headers: this.getHeaders(),
      credentials: 'include', // Include cookies for CSRF protection
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data);
    }
    
    try {
      const response = await fetch(url, options);
      
      // Handle HTTP errors
      if (!response.ok) {
        const errorData = await response.json();
        throw {
          status: response.status,
          message: errorData.message || 'An error occurred',
          errors: errorData.errors || [],
          data: errorData.data
        };
      }
      
      // Parse JSON response
      const result = await response.json();
      return result.data; // Extract data from standard API envelope
      
    } catch (error) {
      // Re-throw to be handled by caller
      throw error;
    }
  },
  
  // Convenience methods
  async get(endpoint) {
    return this.request(endpoint, 'GET');
  },
  
  async post(endpoint, data) {
    return this.request(endpoint, 'POST', data);
  },
  
  async put(endpoint, data) {
    return this.request(endpoint, 'PUT', data);
  },
  
  async delete(endpoint) {
    return this.request(endpoint, 'DELETE');
  }
};

export default API;
```

### Domain-Specific API Services

Based on the central API client, specialized services handle specific domain objects:

```javascript
// api/wallet.js - Wallet-specific API methods
import API from './base';

const WalletAPI = {
  // Get all wallets
  getWallets() {
    return API.get('wallets');
  },
  
  // Get specific wallet by address
  getWallet(address) {
    return API.get(`wallets/${address}`);
  },
  
  // Create new wallet
  createWallet(walletData) {
    return API.post('wallets', walletData);
  },
  
  // Update wallet metadata
  updateWallet(address, walletData) {
    return API.put(`wallets/${address}`, walletData);
  },
  
  // Get wallet balance
  getBalance(address) {
    return API.get(`wallets/${address}/balance`);
  },
  
  // Get wallet transactions
  getTransactions(address) {
    return API.get(`wallets/${address}/transactions`);
  }
};

export default WalletAPI;
```

## 🔄 Request/Response Handling

### Error Handling

Consistent error handling pattern for API requests:

```javascript
// Example of component using the API with error handling
async function loadWallets() {
  try {
    // Show loading state
    this.loading = true;
    
    // Make API request
    const wallets = await WalletAPI.getWallets();
    
    // Update component state
    this.wallets = wallets;
    this.error = null;
    
  } catch (error) {
    // Handle different types of errors
    if (error.status === 401) {
      // Authentication error - redirect to login
      window.location.href = '/login';
    } else {
      // Display error in component
      this.error = error.message || 'Failed to load wallets';
      
      // Optional: Log detailed error for debugging
      console.error('API Error:', error);
      
      // Show user-friendly notification
      this.$notify({
        type: 'error',
        title: 'Error',
        message: this.error
      });
    }
  } finally {
    // Always hide loading state
    this.loading = false;
  }
}
```

### Loading States

Managing loading states during API calls:

```javascript
// Global loading indicator management
const loadingManager = {
  activeRequests: 0,
  
  startLoading() {
    this.activeRequests++;
    document.dispatchEvent(new Event('loading:start'));
  },
  
  stopLoading() {
    this.activeRequests--;
    if (this.activeRequests <= 0) {
      this.activeRequests = 0;
      document.dispatchEvent(new Event('loading:stop'));
    }
  }
};

// Enhanced API base with loading management
const API = {
  // ... other methods from above
  
  async request(endpoint, method = 'GET', data = null) {
    loadingManager.startLoading();
    
    try {
      // ...existing request code
      const result = await fetch(...);
      return result;
    } catch (error) {
      throw error;
    } finally {
      loadingManager.stopLoading();
    }
  }
};
```

## 🔐 Authentication Integration

### Login Flow

```javascript
// api/auth.js
import API from './base';

const AuthAPI = {
  // Login user and get token
  async login(credentials) {
    const response = await API.post('auth/login', credentials);
    
    // Store token in local storage
    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.user));
    }
    
    return response;
  },
  
  // Logout user
  async logout() {
    try {
      await API.post('auth/logout');
    } finally {
      // Clear local storage regardless of API response
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },
  
  // Check if user is authenticated
  isAuthenticated() {
    return !!localStorage.getItem('auth_token');
  },
  
  // Get current user data
  getCurrentUser() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  },
  
  // Refresh access token using refresh token
  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await API.post('auth/refresh', {
      refresh_token: refreshToken
    });
    
    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
    }
    
    return response;
  }
};

export default AuthAPI;
```

### Token Refresh Interceptor

Automatically refreshing expired tokens:

```javascript
// api/interceptors.js
import AuthAPI from './auth';

// Response interceptor for handling token expiration
export async function handleApiResponse(response) {
  // If response is unauthorized (401)
  if (response.status === 401) {
    const originalRequest = response.config;
    
    // Avoid infinite loops - don't retry refresh token requests
    if (originalRequest.url.includes('auth/refresh')) {
      throw new Error('Refresh token failed');
    }
    
    try {
      // Try to refresh the token
      await AuthAPI.refreshToken();
      
      // Retry the original request with new token
      const newToken = localStorage.getItem('auth_token');
      originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
      
      return fetch(originalRequest.url, originalRequest);
    } catch (error) {
      // If refresh fails, redirect to login
      AuthAPI.logout();
      window.location.href = '/login';
      throw error;
    }
  }
  
  return response;
}

// Apply interceptor to API requests
export function setupInterceptors(API) {
  const originalRequest = API.request;
  
  API.request = async function(...args) {
    try {
      const response = await originalRequest.apply(this, args);
      return await handleApiResponse(response);
    } catch (error) {
      throw error;
    }
  };
  
  return API;
}
```

## 📊 Data Management

### State Management

Managing API data in frontend state:

```javascript
// Alpine.js data store example
document.addEventListener('alpine:init', () => {
  Alpine.store('wallets', {
    items: [],
    loading: false,
    error: null,
    
    async fetchWallets() {
      this.loading = true;
      this.error = null;
      
      try {
        this.items = await WalletAPI.getWallets();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    
    getWallet(address) {
      return this.items.find(wallet => wallet.address === address);
    },
    
    // Additional methods for creating, updating wallets
  });
});
```

### Caching Strategy

Implementing simple client-side caching:

```javascript
// Caching utility
const ApiCache = {
  cache: new Map(),
  
  // Set cache timeout (in milliseconds)
  DEFAULT_TIMEOUT: 5 * 60 * 1000, // 5 minutes
  
  // Get cached data if available and not expired
  get(key) {
    const cached = this.cache.get(key);
    
    if (!cached) {
      return null;
    }
    
    // Check if cache is expired
    if (Date.now() - cached.timestamp > cached.timeout) {
      this.cache.delete(key);
      return null;
    }
    
    return cached.data;
  },
  
  // Store data in cache
  set(key, data, timeout = this.DEFAULT_TIMEOUT) {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      timeout
    });
  },
  
  // Remove item from cache
  remove(key) {
    this.cache.delete(key);
  },
  
  // Clear entire cache
  clear() {
    this.cache.clear();
  }
};

// Enhanced API get method with caching
async function cachedGet(endpoint, forceRefresh = false) {
  const cacheKey = `api:${endpoint}`;
  
  // Return cached data if available and not forced refresh
  if (!forceRefresh) {
    const cachedData = ApiCache.get(cacheKey);
    if (cachedData) {
      return cachedData;
    }
  }
  
  // Otherwise fetch fresh data
  const data = await API.get(endpoint);
  
  // Cache the response
  ApiCache.set(cacheKey, data);
  
  return data;
}
```

## 🛠️ API Service Implementation Examples

### Transaction Service

```javascript
// api/transaction.js
import API from './base';

const TransactionAPI = {
  // Get all transactions
  getTransactions(page = 1, limit = 20, filter = null) {
    let endpoint = `transactions?page=${page}&limit=${limit}`;
    
    if (filter) {
      endpoint += `&filter=${filter}`;
    }
    
    return API.get(endpoint);
  },
  
  // Get transaction by ID
  getTransaction(id) {
    return API.get(`transactions/${id}`);
  },
  
  // Create new transaction
  createTransaction(transactionData) {
    return API.post('transactions', transactionData);
  },
  
  // Get pending transactions
  getPendingTransactions() {
    return API.get('transactions/pending');
  }
};

export default TransactionAPI;
```

### Blockchain Service

```javascript
// api/blockchain.js
import API from './base';

const BlockchainAPI = {
  // Get blockchain information
  getInfo() {
    return API.get('blockchain');
  },
  
  // Get list of blocks
  getBlocks(page = 1, limit = 20) {
    return API.get(`blockchain/blocks?page=${page}&limit=${limit}`);
  },
  
  // Get specific block by hash
  getBlock(hash) {
    return API.get(`blockchain/blocks/${hash}`);
  },
  
  // Mine pending transactions
  minePendingTransactions(minerAddress) {
    return API.post('blockchain/mine', { miner_address: minerAddress });
  },
  
  // Validate blockchain
  validateBlockchain() {
    return API.get('blockchain/validate');
  }
};

export default BlockchainAPI;
```

### Contact Service

```javascript
// api/contact.js
import API from './base';

const ContactAPI = {
  // Get all contacts
  getContacts() {
    return API.get('contacts');
  },
  
  // Get specific contact
  getContact(address) {
    return API.get(`contacts/${address}`);
  },
  
  // Create new contact
  createContact(contactData) {
    return API.post('contacts', contactData);
  },
  
  // Update contact
  updateContact(address, contactData) {
    return API.put(`contacts/${address}`, contactData);
  },
  
  // Delete contact
  deleteContact(address) {
    return API.delete(`contacts/${address}`);
  }
};

export default ContactAPI;
```

## 📱 Responsive API Considerations

### Data Loading Optimization

Adjusting data fetching based on device capability:

```javascript
// Device-aware data loading
function getPageSize() {
  // Determine appropriate page size based on device/screen
  if (window.innerWidth < 640) {
    return 10; // Mobile
  } else if (window.innerWidth < 1024) {
    return 15; // Tablet
  } else {
    return 25; // Desktop
  }
}

// Usage in API call
const transactions = await TransactionAPI.getTransactions(1, getPageSize());
```

### Image and Asset Optimization

Requesting appropriate image sizes:

```javascript
// Example of responsive image request
function getQRCodeSize() {
  return window.innerWidth < 640 ? 128 : 256;
}

// Usage in API call
const qrCode = await API.get(`wallets/${address}/qrcode?size=${getQRCodeSize()}`);
```

## 🧪 API Testing

### Mock API for Development

Setting up a mock API for development and testing:

```javascript
// mock/api.js - Mock API implementation
const MockAPI = {
  // Simulate network delay
  delay(ms = 300) {
    return new Promise(resolve => setTimeout(resolve, ms));
  },
  
  // Mock data storage
  data: {
    wallets: [
      {
        address: 'abc123',
        nickname: 'Main Wallet',
        balance: 123.45
      },
      {
        address: 'def456',
        nickname: 'Savings',
        balance: 67.89
      }
    ],
    transactions: [
      // Mock transactions
    ],
    contacts: [
      // Mock contacts
    ]
  },
  
  // Mock get request
  async get(endpoint) {
    await this.delay();
    
    if (endpoint === 'wallets') {
      return [...this.data.wallets];
    }
    
    // Match specific wallet endpoint
    const walletMatch = endpoint.match(/wallets\/([^/]+)$/);
    if (walletMatch) {
      const address = walletMatch[1];
      const wallet = this.data.wallets.find(w => w.address === address);
      if (!wallet) {
        throw { status: 404, message: 'Wallet not found' };
      }
      return { ...wallet };
    }
    
    // Add more endpoint handlers
    
    throw { status: 404, message: 'Endpoint not found' };
  },
  
  // Mock post request
  async post(endpoint, data) {
    await this.delay();
    
    if (endpoint === 'wallets') {
      const newWallet = {
        address: 'w' + Math.random().toString(36).substring(2, 10),
        nickname: data.nickname,
        balance: 0
      };
      
      this.data.wallets.push(newWallet);
      return { ...newWallet };
    }
    
    // Add more endpoint handlers
    
    throw { status: 404, message: 'Endpoint not found' };
  },
  
  // Add more methods (put, delete)
};

export default MockAPI;
```
