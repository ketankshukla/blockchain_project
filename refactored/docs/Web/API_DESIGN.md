# 🔌 FastAPI Design Document

<div style="background-color: #fff8e1; padding: 15px; border-radius: 8px; border-left: 5px solid #ffc107;">

This document details the design of the FastAPI backend for the blockchain application, focusing on endpoints, request/response models, and integration with the existing business logic.

</div>

## 📋 Table of Contents

- [API Architecture](#api-architecture)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Request/Response Models](#requestresponse-models)
- [Business Logic Integration](#business-logic-integration)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)

## 🏗️ API Architecture

<div style="background-color: #e6f7ff; padding: 15px; border-radius: 8px; border-left: 5px solid #1890ff;">

### Why FastAPI?

FastAPI is selected for several key advantages:

1. **Performance** - One of the fastest Python frameworks available
2. **Automatic Documentation** - Swagger UI and ReDoc integration
3. **Data Validation** - Pydantic integration for request/response validation
4. **Modern Python** - Type hints, async support, and dependency injection
5. **Easy Integration** - Works well with SQLAlchemy and other libraries

### API Structure

```
api/
├── main.py            # FastAPI application entry point
├── dependencies.py    # Dependency injection
├── config.py          # Configuration settings
├── database.py        # Database setup
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic models
├── routes/            # API route definitions
│   ├── auth.py
│   ├── wallets.py
│   ├── transactions.py
│   ├── blockchain.py
│   └── contacts.py
├── services/          # Business logic services
│   ├── blockchain.py
│   ├── wallet.py
│   ├── transaction.py
│   └── contact.py
└── utils/             # Utility functions
```

</div>

## 🔐 Authentication

<div style="background-color: #f9f0ff; padding: 15px; border-radius: 8px; border-left: 5px solid #9c27b0;">

### JWT Authentication

The API will use JWT (JSON Web Tokens) for authentication:

1. **Token-Based Flow**
   - User logs in with username/password
   - Server validates credentials and returns JWT
   - Client includes JWT in Authorization header
   - Server validates token for protected endpoints

2. **Token Structure**
   - Header: Algorithm and token type
   - Payload: User ID, expiration time, roles
   - Signature: Ensures token integrity

3. **Implementation**
   - Use FastAPI's built-in security utilities
   - OAuth2PasswordBearer for token extraction
   - JWT encoding/decoding with PyJWT

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Invalidate token (optional)

### Auth Dependencies

```python
# Example FastAPI auth dependency (conceptual, not actual code)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(user_id)
    if user is None:
        raise credentials_exception
    return user
```

</div>

## 🌐 API Endpoints

<div style="background-color: #e8f4fd; padding: 15px; border-radius: 8px; border-left: 5px solid #2196f3;">

### Wallet Endpoints

```
GET    /api/wallets                  # List all wallets
POST   /api/wallets                  # Create new wallet
GET    /api/wallets/{address}        # Get wallet details
PUT    /api/wallets/{address}        # Update wallet
GET    /api/wallets/{address}/balance # Get wallet balance
GET    /api/wallets/{address}/transactions # Get wallet transactions
```

### Transaction Endpoints

```
GET    /api/transactions             # List transactions
POST   /api/transactions             # Create transaction
GET    /api/transactions/{id}        # Get transaction details
GET    /api/transactions/pending     # Get pending transactions
```

### Blockchain Endpoints

```
GET    /api/blockchain               # Get blockchain info
GET    /api/blockchain/blocks        # List blocks
GET    /api/blockchain/blocks/{hash} # Get block details
POST   /api/blockchain/mine          # Mine pending transactions
GET    /api/blockchain/validate      # Validate blockchain
```

### Contact Endpoints

```
GET    /api/contacts                 # List contacts
POST   /api/contacts                 # Create contact
GET    /api/contacts/{address}       # Get contact details
PUT    /api/contacts/{address}       # Update contact
DELETE /api/contacts/{address}       # Delete contact
```

### Auth Endpoints

```
POST   /api/auth/register            # Register new user
POST   /api/auth/login               # Login and get token
POST   /api/auth/refresh             # Refresh token
```

### Example Route Implementation

```python
# Example FastAPI route (conceptual, not actual code)

@router.post("/transactions", response_model=schemas.TransactionResponse)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate sender wallet belongs to current user
    wallet = db.query(models.Wallet).filter(
        models.Wallet.address == transaction.sender_address,
        models.Wallet.user_id == current_user.id
    ).first()
    
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to send from this wallet"
        )
    
    # Call business logic service
    transaction_service = TransactionService(db)
    result = transaction_service.create_transaction(
        transaction.sender_address,
        transaction.recipient_address,
        transaction.amount
    )
    
    return result
```

</div>

## 📝 Request/Response Models

<div style="background-color: #f0fff0; padding: 15px; border-radius: 8px; border-left: 5px solid #2e8b57;">

### Pydantic Models

FastAPI uses Pydantic models for request validation and response serialization:

```python
# Example Pydantic models (conceptual, not actual code)

# Auth schemas
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

# Wallet schemas
class WalletBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    nickname: Optional[str] = None

class WalletCreate(WalletBase):
    pass

class Wallet(WalletBase):
    address: str
    balance: float
    
    class Config:
        orm_mode = True

# Transaction schemas
class TransactionCreate(BaseModel):
    sender_address: str
    recipient_address: str
    amount: float

class Transaction(BaseModel):
    id: str
    sender_address: str
    recipient_address: str
    amount: float
    timestamp: datetime
    type: str
    block_hash: Optional[str] = None
    is_pending: bool
    
    class Config:
        orm_mode = True

# Standard API response
class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    errors: List[str] = []
```

### Response Envelope

All API responses will use a consistent envelope format:

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully",
  "errors": []
}
```

For errors:

```json
{
  "success": false,
  "data": null,
  "message": "Operation failed",
  "errors": ["Specific error message"]
}
```

</div>

## 🔄 Business Logic Integration

<div style="background-color: #fff2f0; padding: 15px; border-radius: 8px; border-left: 5px solid #ff4d4f;">

### Service Layer

To integrate existing business logic with the API, a service layer will be created:

```python
# Example service layer concept (not actual code)

class BlockchainService:
    def __init__(self, db_session):
        self.db = db_session
        self.data_handler = DatabaseDataHandler(db_session)  # Adapter for new DB
        self.blockchain = Blockchain(self.data_handler)
    
    def get_blockchain_info(self):
        """Get blockchain information."""
        return {
            "length": len(self.blockchain.chain),
            "is_valid": self.blockchain.validate_chain(),
            "pending_transactions": len(self.blockchain.pending_transactions)
        }
    
    def mine_pending_transactions(self, miner_address):
        """Mine pending transactions and reward the miner."""
        # Validate miner wallet exists
        wallet = self.db.query(Wallet).filter(Wallet.address == miner_address).first()
        if not wallet:
            raise ValueError("Invalid miner wallet address")
        
        # Call existing business logic
        return self.blockchain.mine_pending_transactions(miner_address)
```

### Adapter Pattern

The adapter pattern will be used to make existing business logic work with the new database:

```python
# Example adapter pattern (conceptual, not actual code)

class DatabaseDataHandler:
    """Adapter that implements the same interface as the original DataHandler
    but uses SQLAlchemy instead of JSON files."""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def load_blockchain(self):
        """Load blockchain data from database."""
        blocks = self.db.query(Block).order_by(Block.index).all()
        return [self._block_to_dict(block) for block in blocks]
    
    def save_blockchain(self, chain_data):
        """Save blockchain data to database."""
        # Implementation to save blockchain data
        
    def _block_to_dict(self, block):
        """Convert Block ORM object to dictionary."""
        return {
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "index": block.index,
            "timestamp": block.timestamp.timestamp(),
            "nonce": block.nonce,
            "transactions": [self._transaction_to_dict(tx) for tx in block.transactions]
        }
```

### Dependency Injection

FastAPI's dependency injection system will be used to provide services to endpoints:

```python
# Example dependency injection (conceptual, not actual code)

def get_blockchain_service(db: Session = Depends(get_db)):
    return BlockchainService(db)

@router.get("/blockchain", response_model=schemas.BlockchainInfo)
async def get_blockchain_info(
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    return blockchain_service.get_blockchain_info()
```

</div>

## ⚠️ Error Handling

<div style="background-color: #fffbe6; padding: 15px; border-radius: 8px; border-left: 5px solid #faad14;">

### Exception Handlers

FastAPI allows defining custom exception handlers:

```python
# Example exception handlers (conceptual, not actual code)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "errors": [exc.detail], "data": None},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": "Validation error", "errors": errors, "data": None},
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"success": False, "message": str(exc), "errors": [str(exc)], "data": None},
    )
```

### Business Logic Exceptions

Custom exceptions for business logic errors:

```python
class InsufficientBalanceError(Exception):
    """Raised when a wallet has insufficient balance for a transaction."""
    pass

class InvalidTransactionError(Exception):
    """Raised when a transaction is invalid."""
    pass

class BlockchainValidationError(Exception):
    """Raised when blockchain validation fails."""
    pass
```

### Error Codes

Standardized error codes for API clients:

```python
ERROR_CODES = {
    "AUTHENTICATION_ERROR": "Authentication failed",
    "AUTHORIZATION_ERROR": "User not authorized for this operation",
    "INSUFFICIENT_BALANCE": "Wallet has insufficient balance",
    "INVALID_TRANSACTION": "Transaction is invalid",
    "BLOCKCHAIN_INVALID": "Blockchain validation failed",
    "RESOURCE_NOT_FOUND": "Requested resource not found",
    # Additional error codes...
}
```

</div>

## ⚡ Performance Considerations

<div style="background-color: #f3e5f5; padding: 15px; border-radius: 8px; border-left: 5px solid #9c27b0;">

### Async Support

FastAPI supports asynchronous endpoints for improved performance:

```python
@router.get("/wallets", response_model=List[schemas.Wallet])
async def get_wallets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    # Async query example
    result = await db.execute(
        select(models.Wallet).offset(skip).limit(limit)
    )
    wallets = result.scalars().all()
    return wallets
```

### Database Optimization

1. **Indexing** - Create appropriate indexes for frequently queried fields
2. **Query Optimization** - Use SQLAlchemy's joinedload for related data
3. **Pagination** - Implement skip/limit for large result sets
4. **Selective Loading** - Load only required columns

### Caching

Implement caching for frequently accessed data:

```python
# Example caching with FastAPI (conceptual, not actual code)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@router.get("/blockchain/blocks", response_model=List[schemas.Block])
@cache(expire=60)  # Cache for 60 seconds
async def get_blocks(
    skip: int = 0,
    limit: int = 100,
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    return blockchain_service.get_blocks(skip, limit)
```

### Rate Limiting

Implement rate limiting to prevent abuse:

```python
# Example rate limiting with FastAPI (conceptual, not actual code)
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@router.post("/transactions", response_model=schemas.Transaction)
@limiter.limit("5/minute")  # 5 requests per minute
async def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    blockchain_service: BlockchainService = Depends(get_blockchain_service)
):
    return blockchain_service.create_transaction(
        transaction.sender_address,
        transaction.recipient_address,
        transaction.amount,
        current_user.id
    )
```

</div>

## 📚 Conclusion

<div style="background-color: #f0f2f5; padding: 15px; border-radius: 8px; border-left: 5px solid #8c8c8c;">

The FastAPI implementation will provide a robust, modern API for the blockchain application with the following benefits:

1. **Modern Architecture** - RESTful endpoints with proper validation
2. **Strong Typing** - Type safety with Pydantic models
3. **Documentation** - Automatic API documentation with Swagger/ReDoc
4. **Security** - JWT authentication and proper error handling
5. **Performance** - Asynchronous support and optimization features

By following the design outlined in this document, the existing business logic can be reused while providing a modern, web-friendly interface for the application.

</div>
