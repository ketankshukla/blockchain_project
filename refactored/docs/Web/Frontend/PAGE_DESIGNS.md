# 📄 Page Designs

<div style="background-color: #fff0f0; padding: 15px; border-radius: 8px; border-left: 5px solid #f56565;">

This document outlines the key page designs for the blockchain application web interface.

</div>

## 📋 Page Overview

The application will consist of the following main pages:

1. **Login/Registration** - User authentication
2. **Dashboard** - Overview of wallets and recent activity
3. **Wallets** - Manage wallets and view balances
4. **Transactions** - View and create transactions
5. **Contacts** - Manage recipient contact list
6. **Blockchain Explorer** - View blockchain data and blocks
7. **Settings** - User preferences and application settings

## 🔐 Authentication Pages

### Login Page

The login page provides access to the application for registered users.

**Key Elements:**
- Username/email input
- Password input with toggle visibility
- "Remember me" checkbox
- Login button
- Link to registration page
- Password recovery link

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│         BLOCKCHAIN APP         │
│                                │
│  ┌─────────────────────────┐   │
│  │      LOGIN FORM         │   │
│  │                         │   │
│  │  Username/Email         │   │
│  │  [                    ] │   │
│  │                         │   │
│  │  Password               │   │
│  │  [                    ] │   │
│  │                         │   │
│  │  [x] Remember me        │   │
│  │                         │   │
│  │  [     LOGIN     ]      │   │
│  │                         │   │
│  │  New user? Register     │   │
│  │  Forgot password?       │   │
│  └─────────────────────────┘   │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

### Registration Page

The registration page allows new users to create an account.

**Key Elements:**
- Username input
- Email input
- Password input with strength indicator
- Password confirmation
- Registration button
- Link to login page

## 📊 Dashboard Page

The dashboard provides an overview of the user's blockchain activity.

**Key Elements:**
- Wallet summary cards with balances
- Recent transactions list
- Blockchain status summary
- Quick action buttons (Send, Receive, etc.)

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────┐  ┌─────────────┐  │
│  │ WELCOME │  │ WALLET      │  │
│  │ [User]  │  │ OVERVIEW    │  │
│  └─────────┘  └─────────────┘  │
│                                │
│  ┌───────────────────────────┐ │
│  │      WALLET CARDS         │ │
│  │ ┌─────┐ ┌─────┐ ┌─────┐   │ │
│  │ │Wallet│ │Wallet│ │Wallet│ │ │
│  │ │  1   │ │  2   │ │  3   │ │ │
│  │ └─────┘ └─────┘ └─────┘   │ │
│  │                           │ │
│  │ [+ Add New Wallet]        │ │
│  └───────────────────────────┘ │
│                                │
│  ┌───────────────────────────┐ │
│  │    RECENT TRANSACTIONS    │ │
│  │                           │ │
│  │ • Transaction 1           │ │
│  │ • Transaction 2           │ │
│  │ • Transaction 3           │ │
│  │                           │ │
│  │ [View All Transactions]   │ │
│  └───────────────────────────┘ │
│                                │
│  ┌───────────────────────────┐ │
│  │    BLOCKCHAIN STATUS      │ │
│  │                           │ │
│  │ Blocks: 1,234             │ │
│  │ Last mined: 10 min ago    │ │
│  │ Pending tx: 3             │ │
│  │                           │ │
│  │ [View Blockchain]         │ │
│  └───────────────────────────┘ │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## 💼 Wallets Page

The wallets page allows users to manage their blockchain wallets.

**Key Elements:**
- List of wallets with balances and details
- Create new wallet button
- Wallet details/edit view
- Send/receive transaction buttons
- Transaction history per wallet

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────────────────────┐   │
│  │ WALLETS              [+]│   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ WALLET 1                │   │
│  │ Address: abc...123      │   │
│  │ Balance: 123.45         │   │
│  │ [SEND] [RECEIVE] [EDIT] │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ WALLET 2                │   │
│  │ Address: def...456      │   │
│  │ Balance: 67.89          │   │
│  │ [SEND] [RECEIVE] [EDIT] │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ WALLET 3                │   │
│  │ Address: ghi...789      │   │
│  │ Balance: 0.12           │   │
│  │ [SEND] [RECEIVE] [EDIT] │   │
│  └─────────────────────────┘   │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## 💸 Transactions Page

The transactions page displays the user's transaction history and allows creation of new transactions.

**Key Elements:**
- Transaction list with filtering options
- Transaction details view
- Create new transaction button
- Search and filter options

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────────────────┐ [+]   │
│  │ TRANSACTIONS        │       │
│  └─────────────────────┘       │
│                                │
│  ┌─────────────────────────┐   │
│  │ FILTERS                 │   │
│  │ [ALL|SENT|RECEIVED|PENDING] │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Transaction 1           │   │
│  │ Date: 2023-01-01        │   │
│  │ From: abc...123         │   │
│  │ To: def...456           │   │
│  │ Amount: 10.00           │   │
│  │ Status: Confirmed       │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Transaction 2           │   │
│  │ Date: 2023-01-02        │   │
│  │ From: ghi...789         │   │
│  │ To: abc...123           │   │
│  │ Amount: 5.00            │   │
│  │ Status: Pending         │   │
│  └─────────────────────────┘   │
│                                │
│  [Load More]                   │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## 👥 Contacts Page

The contacts page allows users to manage their list of contacts for easy transactions.

**Key Elements:**
- Contact list with search
- Contact details view
- Add/edit/delete contact functions
- Quick transaction buttons

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────────────────┐ [+]   │
│  │ CONTACTS            │       │
│  └─────────────────────┘       │
│                                │
│  ┌─────────────────────────┐   │
│  │ Search: [          ]    │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Contact 1               │   │
│  │ Address: abc...123      │   │
│  │ [SEND] [EDIT] [DELETE]  │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Contact 2               │   │
│  │ Address: def...456      │   │
│  │ [SEND] [EDIT] [DELETE]  │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Contact 3               │   │
│  │ Address: ghi...789      │   │
│  │ [SEND] [EDIT] [DELETE]  │   │
│  └─────────────────────────┘   │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## ⛓️ Blockchain Explorer Page

The blockchain explorer allows users to view and navigate the blockchain data.

**Key Elements:**
- Block list with pagination
- Block details view
- Transaction list within blocks
- Search by block hash/index

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────────────────────┐   │
│  │ BLOCKCHAIN EXPLORER     │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Search: [          ]    │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Block #1234             │   │
│  │ Hash: abc...123         │   │
│  │ Prev Hash: def...456    │   │
│  │ Timestamp: 2023-01-01   │   │
│  │ Transactions: 5         │   │
│  │ [View Details]          │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ Block #1233             │   │
│  │ Hash: ghi...789         │   │
│  │ Prev Hash: jkl...012    │   │
│  │ Timestamp: 2023-01-01   │   │
│  │ Transactions: 3         │   │
│  │ [View Details]          │   │
│  └─────────────────────────┘   │
│                                │
│  [< Prev] [Next >]            │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## ⚙️ Settings Page

The settings page allows users to configure application preferences.

**Key Elements:**
- User profile settings
- Application preferences
- Security settings
- Notification preferences

**Layout:**
```
┌────────────────────────────────┐
│           HEADER               │
├────────────────────────────────┤
│                                │
│  ┌─────────────────────────┐   │
│  │ SETTINGS                │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ USER PROFILE            │   │
│  │ Username: [          ]  │   │
│  │ Email: [             ]  │   │
│  │ [Change Password]       │   │
│  │ [Save Changes]          │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ PREFERENCES             │   │
│  │ [ ] Dark Mode           │   │
│  │ [x] Email Notifications │   │
│  │ [ ] Browser Notifications │ │
│  │ Currency: [USD▼]        │   │
│  │ [Save Preferences]      │   │
│  └─────────────────────────┘   │
│                                │
│  ┌─────────────────────────┐   │
│  │ SECURITY                │   │
│  │ [Enable Two-Factor Auth]│   │
│  │ [View Session History]  │   │
│  │ [Logout All Devices]    │   │
│  └─────────────────────────┘   │
│                                │
├────────────────────────────────┤
│           FOOTER               │
└────────────────────────────────┘
```

## 🎨 Design Consistency

All pages will maintain consistent styling with:

1. **Header** - Main navigation
2. **Footer** - Copyright, links, and support info
3. **Common Components** - Notifications, modals, and buttons
4. **Responsive Layout** - Adapting to different screen sizes
