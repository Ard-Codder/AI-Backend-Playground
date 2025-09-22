# 🏗️ AI Backend Playground - Architecture Guide

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Project Structure](#project-structure)
3. [Backend Architecture](#backend-architecture)
4. [ML Components](#ml-components)
5. [Database Design](#database-design)
6. [API Design](#api-design)
7. [Authentication Flow](#authentication-flow)
8. [Docker Architecture](#docker-architecture)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Pipeline](#deployment-pipeline)

---

## 🎯 System Overview

**AI Backend Playground** is a full-stack demonstration project showcasing modern backend development practices combined with machine learning algorithms implemented from scratch. The system is designed to demonstrate professional-level skills in:

- **Backend Development**: FastAPI, async/await, PostgreSQL
- **Machine Learning**: Custom algorithm implementations
- **DevOps**: Docker, CI/CD, testing strategies
- **Software Architecture**: Clean code, separation of concerns

### Core Philosophy
- **Learning-oriented**: Algorithms implemented from scratch (not using sklearn)
- **Production-ready**: Real authentication, database, Docker deployment
- **Modern practices**: Async programming, type hints, comprehensive testing
- **Portfolio-focused**: Clean code that demonstrates technical skills

---

## 📁 Project Structure

```
ai-backend-playground/
├── 🌐 backend/                  # FastAPI Web Application
│   └── app/
│       ├── models/              # SQLAlchemy Database Models
│       ├── routes/              # API Endpoints (Controllers)
│       ├── services/            # Business Logic Layer
│       ├── schemas/             # Pydantic Data Validation
│       ├── auth/                # Authentication & Security
│       ├── db.py                # Database Configuration
│       └── main.py              # Application Entry Point
│
├── 🤖 ml_core/                  # Machine Learning Library
│   ├── kmeans.py                # K-Means Clustering Algorithm
│   ├── decision_tree.py         # Decision Tree Classifier
│   ├── random_forest.py         # Random Forest Ensemble
│   └── tests/                   # ML Algorithm Tests
│
├── 🧪 tests/                    # Integration & API Tests
├── 🐳 docker/                   # Docker Configuration
├── 📊 data/                     # Sample Datasets
├── 🚀 .github/workflows/        # CI/CD Automation
└── 📚 docs/                     # Documentation
```

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between web, business logic, data, and ML
2. **Dependency Injection**: Database sessions and services injected as dependencies
3. **Async-First**: Full async/await support for maximum performance
4. **Type Safety**: Comprehensive type hints throughout the codebase
5. **Testing**: Unit and integration tests for all components

---

## 🌐 Backend Architecture

### 🔧 Technology Stack

- **Framework**: FastAPI (async web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic for request/response schemas
- **Migration**: Alembic for database schema management

### 🏛️ Application Layers

#### 1. **API Layer** (`routes/`)
```python
# Example: User registration endpoint
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return UserResponse.model_validate(user)
```

**Responsibilities:**
- HTTP request/response handling
- Input validation via Pydantic
- Dependency injection
- Error handling and status codes

#### 2. **Service Layer** (`services/`)
```python
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(email=user_data.email, hashed_password=hashed_password)
        # Business logic here...
```

**Responsibilities:**
- Business logic implementation
- Data validation and transformation
- Orchestrating database operations
- Error handling and business rules

#### 3. **Data Layer** (`models/`)
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Relationships and constraints...
```

**Responsibilities:**
- Database schema definition
- Relationships between entities
- Data constraints and indexes
- ORM mappings

### 🔄 Request Flow

```
1. HTTP Request → FastAPI Router
2. Router → Pydantic Validation
3. Router → Service Layer (Business Logic)
4. Service → Database Layer (Data Access)
5. Database → Service (Data Response)
6. Service → Router (Business Response)
7. Router → HTTP Response
```

---

## 🤖 ML Components

### 🧠 Custom Algorithm Implementations

All ML algorithms are implemented from scratch using only NumPy, demonstrating understanding of the mathematical foundations:

#### 1. **K-Means Clustering** (`kmeans.py`)

```python
class KMeans:
    def fit(self, X: np.ndarray) -> 'KMeans':
        # Initialize centroids randomly
        self.centroids = self._initialize_centroids(X)
        
        for iteration in range(self.max_iters):
            # Calculate distances to centroids
            distances = self._calculate_distance(X, self.centroids)
            
            # Assign clusters based on minimum distance
            new_labels = self._assign_clusters(distances)
            
            # Check for convergence
            if np.array_equal(self.labels, new_labels):
                break
                
            # Update centroids
            self.centroids = self._update_centroids(X, new_labels)
```

**Algorithm Steps:**
1. **Initialize** centroids randomly
2. **Assign** points to nearest centroids
3. **Update** centroids to cluster means
4. **Repeat** until convergence
5. **Calculate** final inertia (within-cluster sum of squares)

#### 2. **Decision Tree** (`decision_tree.py`)

```python
def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
    # Stopping conditions
    if depth >= self.max_depth or len(np.unique(y)) == 1:
        return Node(value=self._most_common_class(y))
    
    # Find best split using information gain
    best_feature, best_threshold, best_gain = self._best_split(X, y)
    
    # Create split and build subtrees recursively
    left_mask = X[:, best_feature] <= best_threshold
    left_subtree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
    right_subtree = self._build_tree(X[~left_mask], y[~left_mask], depth + 1)
    
    return Node(best_feature, best_threshold, left_subtree, right_subtree)
```

**Algorithm Steps:**
1. **Calculate** information gain for all possible splits
2. **Select** the split with maximum information gain
3. **Recursively** build left and right subtrees
4. **Stop** when maximum depth reached or pure nodes found

#### 3. **Random Forest** (`random_forest.py`)

```python
def fit(self, X: np.ndarray, y: np.ndarray) -> 'RandomForest':
    for i in range(self.n_estimators):
        # Bootstrap sampling
        X_bootstrap, y_bootstrap = self._get_bootstrap_sample(X, y)
        
        # Random feature selection
        feature_indices = self._get_random_features(X.shape[1])
        
        # Train individual tree
        tree = DecisionTree(max_depth=self.max_depth)
        tree.fit(X_bootstrap[:, feature_indices], y_bootstrap)
        
        self.trees.append(tree)
        self.feature_indices.append(feature_indices)
```

**Algorithm Steps:**
1. **Bootstrap** sampling for each tree
2. **Random** feature selection for each split
3. **Train** individual decision trees
4. **Aggregate** predictions via majority voting

### 🖥️ CLI Interface

Each algorithm includes a command-line interface for easy testing:

```bash
# K-Means clustering
python -m ml_core.kmeans --data data.csv --clusters 3 --output results.csv

# Decision Tree classification
python -m ml_core.decision_tree --data data.csv --target class --max-depth 5

# Random Forest ensemble
python -m ml_core.random_forest --data data.csv --target class --n-estimators 100
```

---

## 🗄️ Database Design

### 📊 Entity Relationship Diagram

```
┌─────────────────┐         ┌─────────────────┐
│      Users      │         │      Tasks      │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ email (UNIQUE)  │         │ title           │
│ username (UNIQUE│         │ description     │
│ full_name       │◄────────┤ owner_id (FK)   │
│ hashed_password │ 1     ∞ │ status          │
│ is_active       │         │ priority        │
│ is_superuser    │         │ created_at      │
│ created_at      │         │ updated_at      │
│ updated_at      │         │ due_date        │
└─────────────────┘         │ completed_at    │
                            └─────────────────┘
```

### 🔍 Key Design Decisions

1. **User Authentication**
   - Separate `username` and `email` for flexibility
   - `hashed_password` using bcrypt (never store plain text)
   - `is_active` for soft user deactivation
   - `is_superuser` for admin privileges

2. **Task Management**
   - Enum-based `status` and `priority` for data integrity
   - Nullable `due_date` for optional deadlines
   - `completed_at` timestamp for completion tracking
   - Foreign key relationship to users

3. **Indexing Strategy**
   - Primary keys automatically indexed
   - `email` and `username` indexed for login queries
   - `owner_id` indexed for task filtering

### 🔧 Database Configuration

```python
# Async database setup
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQL logging in development
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency injection for database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 🔌 API Design

### 📋 RESTful Endpoints

#### Authentication Endpoints
```
POST /api/v1/auth/register    # User registration
POST /api/v1/auth/login       # User login (returns JWT)
```

#### User Management
```
GET    /api/v1/users/me       # Get current user profile
PUT    /api/v1/users/me       # Update current user
DELETE /api/v1/users/me       # Delete current user
GET    /api/v1/users/         # List all users (admin only)
GET    /api/v1/users/{id}     # Get user by ID (admin only)
```

#### Task Management
```
POST   /api/v1/tasks/         # Create new task
GET    /api/v1/tasks/         # List user's tasks (with filters)
GET    /api/v1/tasks/{id}     # Get specific task
PUT    /api/v1/tasks/{id}     # Update task
DELETE /api/v1/tasks/{id}     # Delete task
GET    /api/v1/tasks/stats    # Get task statistics
```

#### ML Endpoints
```
GET    /api/v1/ml/            # List available ML algorithms
POST   /api/v1/ml/upload-data # Upload CSV for ML processing
POST   /api/v1/ml/kmeans      # Run K-Means clustering (future)
POST   /api/v1/ml/classify    # Run classification (future)
```

### 📝 Request/Response Schemas

```python
# Example: Task creation
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_completed: bool
    
    class Config:
        from_attributes = True  # Enable ORM mode
```

### 🔐 API Security

1. **JWT Authentication**
   - Bearer token in Authorization header
   - Configurable expiration time
   - Secure token validation

2. **Input Validation**
   - Pydantic schemas for all inputs
   - Length limits and format validation
   - SQL injection prevention via ORM

3. **CORS Configuration**
   - Configurable allowed origins
   - Proper headers for browser security

---

## 🔐 Authentication Flow

### 🎫 JWT Token Lifecycle

```
1. User Registration/Login
   ├── Validate credentials
   ├── Generate JWT token
   └── Return token to client

2. API Request with Token
   ├── Extract Bearer token from header
   ├── Validate token signature
   ├── Check token expiration
   ├── Extract user information
   └── Inject user into request context

3. Token Refresh (future)
   ├── Validate refresh token
   ├── Generate new access token
   └── Return new token pair
```

### 🔑 Security Implementation

```python
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### 🛡️ Protection Middleware

```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Extract and validate current user from JWT token"""
    token = credentials.credentials
    token_data = await verify_token(token)
    
    user_service = UserService(db)
    user = await user_service.get_by_username(token_data.username)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    return user
```

---

## 🐳 Docker Architecture

### 📦 Multi-Container Setup

```yaml
# docker-compose.yml
services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ai_playground
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Database Administration
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

  # FastAPI Backend
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/ai_playground
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app/backend  # Development volume mount
      - ./ml_core:/app/ml_core
```

### 🏗️ Dockerfile Strategy

```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Application code
COPY backend/ ./backend/
COPY ml_core/ ./ml_core/

# Non-root user for security
RUN adduser --disabled-password appuser && chown -R appuser:appuser /app
USER appuser

# Runtime configuration
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 🔧 Development vs Production

**Development Mode:**
- Volume mounts for hot reloading
- Debug logging enabled
- Local database with sample data

**Production Mode:**
- Optimized image without development tools
- Environment-based configuration
- Health checks and restart policies
- Secret management via environment variables

---

## 🧪 Testing Strategy

### 🎯 Testing Pyramid

```
           /\
          /  \
         /    \
        /  E2E \       ← End-to-End (Minimal)
       /________\
      /          \
     /Integration \    ← API & Database Tests
    /______________\
   /                \
  /      Unit        \   ← ML Algorithms & Business Logic
 /____________________\
```

### 🔬 Test Categories

#### 1. **Unit Tests** - ML Algorithms
```python
def test_kmeans_convergence():
    """Test K-Means algorithm convergence"""
    X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8]])
    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(X)
    
    assert len(np.unique(labels)) == 2
    assert kmeans.inertia > 0
    assert kmeans.centroids is not None
```

#### 2. **Integration Tests** - API Endpoints
```python
def test_create_task_authenticated():
    """Test task creation with valid authentication"""
    # Register and login user
    user_data = {"email": "test@example.com", "username": "testuser", "password": "password123"}
    register_response = client.post("/api/v1/auth/register", json=user_data)
    login_response = client.post("/api/v1/auth/login", data={"username": "testuser", "password": "password123"})
    
    # Create task with JWT token
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"title": "Test Task", "description": "Test Description"}
    
    response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
```

#### 3. **Performance Tests** - ML Algorithms
```python
def test_kmeans_performance():
    """Test K-Means performance with larger datasets"""
    X = np.random.rand(1000, 10)  # 1000 samples, 10 features
    
    start_time = time.time()
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X)
    execution_time = time.time() - start_time
    
    assert execution_time < 5.0  # Should complete within 5 seconds
```

### 🚀 Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: ai_playground_test
        options: --health-cmd pg_isready --health-interval 10s
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    
    - name: Run linters
      run: |
        black --check backend/ ml_core/ tests/
        flake8 backend/ ml_core/ tests/
        mypy backend/ ml_core/
    
    - name: Run tests
      run: pytest --cov=backend --cov=ml_core --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## 🚀 Deployment Pipeline

### 🔄 CI/CD Workflow

```
1. Code Push to GitHub
   ├── Trigger GitHub Actions
   ├── Run linters (black, flake8, mypy)
   ├── Execute test suite
   └── Generate coverage report

2. Build & Package
   ├── Build Docker image
   ├── Run security scans
   ├── Push to Docker registry
   └── Create deployment artifacts

3. Deploy to Environment
   ├── Pull latest image
   ├── Update database schema
   ├── Deploy with zero downtime
   └── Run health checks

4. Monitor & Alert
   ├── Application metrics
   ├── Error tracking
   ├── Performance monitoring
   └── Automated rollback if needed
```

### 🌐 Deployment Options

#### **Option 1: Cloud Platforms**
- **Heroku**: Simple git-based deployment
- **Railway**: Modern container deployment
- **DigitalOcean App Platform**: Managed container service
- **AWS ECS/Fargate**: Enterprise container orchestration

#### **Option 2: VPS Deployment**
```bash
# Example deployment script
#!/bin/bash
git pull origin main
docker-compose down
docker-compose pull
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

#### **Option 3: Kubernetes**
```yaml
# k8s deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-backend
  template:
    spec:
      containers:
      - name: backend
        image: ardcodder/ai-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

---

## 🎯 Key Benefits & Learning Outcomes

### 💡 Technical Skills Demonstrated

1. **Modern Python Development**
   - Async/await programming
   - Type hints and static analysis
   - Dependency injection patterns
   - Clean architecture principles

2. **API Development Best Practices**
   - RESTful API design
   - Authentication and authorization
   - Input validation and error handling
   - API documentation (OpenAPI/Swagger)

3. **Database Management**
   - ORM design and relationships
   - Query optimization
   - Migration strategies
   - Connection pooling

4. **Machine Learning Fundamentals**
   - Algorithm implementation from scratch
   - Mathematical understanding of ML concepts
   - Performance optimization
   - CLI tool development

5. **DevOps and Deployment**
   - Containerization strategies
   - CI/CD pipeline design
   - Testing automation
   - Production deployment

### 🏆 Portfolio Value

This project demonstrates:
- **Full-stack capabilities** from ML algorithms to API deployment
- **Production readiness** with proper testing and deployment
- **Code quality** with linting, formatting, and documentation
- **Modern practices** using current technology stack
- **Learning mindset** implementing algorithms from scratch rather than using libraries

---

## ✅ Project Status & Future Extensions

### 🎯 **CURRENT STATUS: PRODUCTION READY v1.0.0**

**All Core Features Completed:**
- ✅ Backend API with authentication (FastAPI + JWT)
- ✅ ML algorithms implemented from scratch (K-Means, Decision Tree, Random Forest)
- ✅ Docker containerization with multi-service setup
- ✅ CI/CD pipeline configured (GitHub Actions)
- ✅ Comprehensive testing (unit + integration)
- ✅ Professional documentation and architecture

### 🚀 **Optional Future Enhancements (v2.0+)**
- Frontend interface (React/Vue.js)
- WebSocket real-time features
- Redis caching layer
- Advanced ML algorithms (Neural Networks, Deep Learning)
- Microservices architecture
- Advanced monitoring and alerting
- Multi-tenant support

This architecture provides a solid foundation for both learning and professional development, demonstrating industry-standard practices while maintaining educational value through custom ML implementations.
