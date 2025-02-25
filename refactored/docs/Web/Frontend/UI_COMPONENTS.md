# 🧩 UI Components

<div style="background-color: #edf7ed; padding: 15px; border-radius: 8px; border-left: 5px solid #4caf50;">

This document details the reusable UI components for the blockchain application's web interface.

</div>

## 🎨 Design System

The application will use a consistent design system with the following characteristics:

- **Color Palette**
  - Primary: `#3f51b5` (Indigo)
  - Secondary: `#f50057` (Pink)
  - Success: `#4caf50` (Green)
  - Warning: `#ff9800` (Orange)
  - Error: `#f44336` (Red)
  - Background: `#f5f5f5` (Light Grey)
  - Text: `#212121` (Dark Grey)

- **Typography**
  - Primary Font: 'Roboto', sans-serif
  - Headings: 'Roboto Condensed', sans-serif
  - Monospace: 'Roboto Mono', monospace (for addresses and hashes)

- **Spacing**
  - Base unit: 8px
  - Margins and padding follow multiples of the base unit

## 📦 Component Library

### Navigation Components

#### 1. Header

Main navigation component with app logo, navigation links, and user account dropdown.

```html
<!-- Header Component -->
<header class="app-header">
  <div class="logo">Blockchain App</div>
  <nav class="main-nav">
    <a href="/dashboard">Dashboard</a>
    <a href="/wallets">Wallets</a>
    <a href="/transactions">Transactions</a>
    <a href="/contacts">Contacts</a>
    <a href="/blockchain">Blockchain</a>
  </nav>
  <div class="user-menu" x-data="{ open: false }">
    <button @click="open = !open">
      <span x-text="username">User</span>
      <i class="icon-chevron-down"></i>
    </button>
    <div x-show="open" class="dropdown-menu">
      <a href="/profile">Profile</a>
      <a href="/settings">Settings</a>
      <a href="/logout">Logout</a>
    </div>
  </div>
</header>
```

#### 2. Sidebar

Alternative navigation component for desktop layouts.

```html
<!-- Sidebar Component -->
<aside class="sidebar" x-data="{ expanded: true }">
  <button @click="expanded = !expanded" class="toggle-btn">
    <i class="icon-menu"></i>
  </button>
  <nav class="sidebar-nav">
    <a href="/dashboard" class="nav-item">
      <i class="icon-dashboard"></i>
      <span x-show="expanded">Dashboard</span>
    </a>
    <!-- More nav items -->
  </nav>
</aside>
```

### Data Display Components

#### 1. Wallet Card

Displays wallet information with balance and actions.

```html
<!-- Wallet Card Component -->
<div class="wallet-card" x-data="walletCard()">
  <div class="wallet-header">
    <h3 x-text="wallet.nickname || 'Wallet'"></h3>
    <span class="wallet-balance" x-text="formatCurrency(wallet.balance)"></span>
  </div>
  <div class="wallet-address">
    <code x-text="formatAddress(wallet.address)"></code>
    <button @click="copyToClipboard(wallet.address)" class="icon-button">
      <i class="icon-copy"></i>
    </button>
  </div>
  <div class="wallet-actions">
    <button @click="showSendForm" class="btn btn-primary">Send</button>
    <button @click="showReceiveInfo" class="btn btn-secondary">Receive</button>
  </div>
</div>
```

#### 2. Transaction List

Displays a paginated list of transactions.

```html
<!-- Transaction List Component -->
<div class="transaction-list" x-data="transactionList()">
  <div class="list-filters">
    <select x-model="filter" @change="applyFilter">
      <option value="all">All Transactions</option>
      <option value="sent">Sent</option>
      <option value="received">Received</option>
      <option value="pending">Pending</option>
    </select>
  </div>
  
  <div class="list-container">
    <template x-for="tx in transactions" :key="tx.id">
      <div class="transaction-item" :class="tx.type">
        <div class="tx-icon">
          <i :class="getTransactionIcon(tx)"></i>
        </div>
        <div class="tx-details">
          <div class="tx-address" x-text="formatAddress(getCounterpartyAddress(tx))"></div>
          <div class="tx-timestamp" x-text="formatDate(tx.timestamp)"></div>
        </div>
        <div class="tx-amount" :class="tx.type">
          <span x-text="formatAmount(tx)"></span>
        </div>
        <div class="tx-status">
          <span class="status-badge" :class="tx.status" x-text="tx.status"></span>
        </div>
      </div>
    </template>
  </div>
  
  <div class="pagination-controls">
    <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
    <span x-text="currentPage"></span>
    <button @click="nextPage" :disabled="!hasMorePages">Next</button>
  </div>
</div>
```

#### 3. Block Explorer

Interactive component to explore blockchain blocks.

```html
<!-- Block Explorer Component -->
<div class="block-explorer" x-data="blockExplorer()">
  <div class="explorer-controls">
    <input type="text" x-model="searchQuery" placeholder="Search by block hash or index...">
    <button @click="searchBlock" class="btn">Search</button>
  </div>
  
  <div class="block-list">
    <template x-for="block in blocks" :key="block.hash">
      <div class="block-item" @click="selectBlock(block)">
        <div class="block-index">#<span x-text="block.index"></span></div>
        <div class="block-hash">
          <code x-text="formatHash(block.hash)"></code>
        </div>
        <div class="block-time" x-text="formatDate(block.timestamp)"></div>
        <div class="block-tx-count">
          <span x-text="block.transactions.length"></span> transactions
        </div>
      </div>
    </template>
  </div>
  
  <div x-show="selectedBlock" class="block-details">
    <h3>Block Details</h3>
    <div class="detail-row">
      <span class="label">Hash:</span>
      <code x-text="selectedBlock?.hash"></code>
    </div>
    <div class="detail-row">
      <span class="label">Previous Hash:</span>
      <code x-text="selectedBlock?.previous_hash"></code>
    </div>
    <div class="detail-row">
      <span class="label">Timestamp:</span>
      <span x-text="formatDate(selectedBlock?.timestamp)"></span>
    </div>
    <div class="detail-row">
      <span class="label">Nonce:</span>
      <span x-text="selectedBlock?.nonce"></span>
    </div>
    
    <h4>Transactions</h4>
    <div class="block-transactions">
      <!-- Transaction list inside block -->
    </div>
  </div>
</div>
```

### Form Components

#### 1. Send Transaction Form

Form for creating and sending new transactions.

```html
<!-- Send Transaction Form -->
<form @submit.prevent="sendTransaction()" class="transaction-form" x-data="sendTransactionForm()">
  <div class="form-group">
    <label for="from-wallet">From Wallet</label>
    <select id="from-wallet" x-model="form.sender" required>
      <template x-for="wallet in wallets" :key="wallet.address">
        <option :value="wallet.address" x-text="getWalletLabel(wallet)"></option>
      </template>
    </select>
    <div class="wallet-balance">
      Balance: <span x-text="formatCurrency(getSelectedWalletBalance())"></span>
    </div>
  </div>
  
  <div class="form-group">
    <label for="to-address">To Address</label>
    <div class="address-input-group">
      <input id="to-address" type="text" x-model="form.recipient" required
             placeholder="Enter recipient address">
      <button type="button" @click="showContactPicker" class="btn-icon">
        <i class="icon-contacts"></i>
      </button>
    </div>
  </div>
  
  <div class="form-group">
    <label for="amount">Amount</label>
    <input id="amount" type="number" x-model="form.amount" required
           min="0.00001" step="0.00001" placeholder="0.00000">
    <div class="amount-validation" x-show="!isValidAmount()">
      Amount exceeds available balance
    </div>
  </div>
  
  <div class="form-actions">
    <button type="button" @click="resetForm" class="btn btn-secondary">Cancel</button>
    <button type="submit" class="btn btn-primary" :disabled="!isFormValid()">Send</button>
  </div>
  
  <!-- Confirmation Modal -->
  <div x-show="showConfirmation" class="modal">
    <div class="modal-content">
      <h3>Confirm Transaction</h3>
      <p>Please review the transaction details:</p>
      <div class="confirmation-details">
        <!-- Transaction details -->
      </div>
      <div class="modal-actions">
        <button @click="showConfirmation = false" class="btn btn-secondary">Cancel</button>
        <button @click="confirmTransaction" class="btn btn-primary">Confirm</button>
      </div>
    </div>
  </div>
</form>
```

#### 2. Contact Form

Form for adding and editing contacts.

```html
<!-- Contact Form -->
<form @submit.prevent="saveContact()" class="contact-form" x-data="contactForm()">
  <div class="form-group">
    <label for="contact-name">Name</label>
    <input id="contact-name" type="text" x-model="form.name" required>
  </div>
  
  <div class="form-group">
    <label for="contact-address">Wallet Address</label>
    <input id="contact-address" type="text" x-model="form.address" required
           pattern="^[a-zA-Z0-9]{26,35}$">
    <div class="validation-message" x-show="!isValidAddress()">
      Please enter a valid wallet address
    </div>
  </div>
  
  <div class="form-group">
    <label for="contact-notes">Notes (Optional)</label>
    <textarea id="contact-notes" x-model="form.notes"></textarea>
  </div>
  
  <div class="form-actions">
    <button type="button" @click="resetForm" class="btn btn-secondary">Cancel</button>
    <button type="submit" class="btn btn-primary" :disabled="!isFormValid()">Save Contact</button>
  </div>
</form>
```

### Feedback Components

#### 1. Toast Notifications

Displays temporary notifications for user feedback.

```html
<!-- Toast Notification Component -->
<div class="toast-container" x-data="toastNotifications()">
  <template x-for="(toast, index) in toasts" :key="index">
    <div class="toast" :class="toast.type" x-show="toast.visible"
         x-transition:enter="toast-enter"
         x-transition:leave="toast-leave">
      <div class="toast-icon">
        <i :class="getToastIcon(toast)"></i>
      </div>
      <div class="toast-content">
        <div class="toast-title" x-text="toast.title"></div>
        <div class="toast-message" x-text="toast.message"></div>
      </div>
      <button @click="removeToast(index)" class="toast-close">×</button>
    </div>
  </template>
</div>

<script>
  function toastNotifications() {
    return {
      toasts: [],
      showToast(type, title, message, duration = 5000) {
        const toast = { type, title, message, visible: true };
        this.toasts.push(toast);
        
        setTimeout(() => {
          toast.visible = false;
          setTimeout(() => {
            this.toasts = this.toasts.filter(t => t !== toast);
          }, 300); // Animation duration
        }, duration);
      },
      removeToast(index) {
        this.toasts[index].visible = false;
        setTimeout(() => {
          this.toasts.splice(index, 1);
        }, 300);
      },
      getToastIcon(toast) {
        const icons = {
          success: 'icon-check-circle',
          error: 'icon-alert-circle',
          warning: 'icon-alert-triangle',
          info: 'icon-info'
        };
        return icons[toast.type] || icons.info;
      }
    };
  }
</script>
```

#### 2. Loading Indicator

Displays loading state for asynchronous operations.

```html
<!-- Loading Indicator Component -->
<div class="loading-overlay" x-data="{ loading: false }" x-show="loading"
     x-transition:enter="fade-in" x-transition:leave="fade-out">
  <div class="loading-spinner"></div>
  <div class="loading-text" x-text="loadingText || 'Loading...'"></div>
</div>

<script>
  // Global loading state management
  window.loadingState = {
    start(text = 'Loading...') {
      Alpine.store('loading').show(text);
    },
    stop() {
      Alpine.store('loading').hide();
    }
  };
  
  document.addEventListener('alpine:init', () => {
    Alpine.store('loading', {
      visible: false,
      text: 'Loading...',
      show(text) {
        this.text = text;
        this.visible = true;
      },
      hide() {
        this.visible = false;
      }
    });
  });
</script>
```

## 📱 Responsive Design

All components will be responsive with these breakpoints:

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

Components will use a mobile-first approach, with specific styling for larger screens using media queries.
