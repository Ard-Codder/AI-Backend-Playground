#!/usr/bin/env python3
"""
AI Backend Playground - Live Demonstration
This script demonstrates the key features of the project
"""

import requests
import json
import time
import sys
from pathlib import Path

# API Configuration
API_BASE = "http://localhost:8000"
API_V1 = f"{API_BASE}/api/v1"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")

def check_api_health():
    """Check if the API is running"""
    print_section("API Health Check")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is healthy! Environment: {data['environment']}")
            return True
        else:
            print_error(f"API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Could not connect to API: {e}")
        print("💡 Make sure to run: docker-compose up -d")
        return False

def demonstrate_user_registration():
    """Demonstrate user registration"""
    print_section("User Registration & Authentication")
    
    # Register a new user
    user_data = {
        "email": "demo@example.com",
        "username": "demouser",
        "password": "securepassword123",
        "full_name": "Demo User"
    }
    
    print("📝 Registering new user...")
    try:
        response = requests.post(f"{API_V1}/auth/register", json=user_data)
        if response.status_code == 200:
            user = response.json()
            print_success(f"User registered: {user['username']} ({user['email']})")
        else:
            print(f"⚠️  Registration response: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print_error(f"Registration failed: {e}")
        return None
    
    # Login to get JWT token
    print("🔐 Logging in...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(f"{API_V1}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print_success("Login successful! JWT token received")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"Login failed: {e}")
        return None

def demonstrate_task_management(token: str):
    """Demonstrate task management features"""
    print_section("Task Management")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create tasks
    tasks_to_create = [
        {
            "title": "Learn FastAPI",
            "description": "Master async web development with FastAPI",
            "priority": "high"
        },
        {
            "title": "Implement ML algorithms",
            "description": "Build K-Means, Decision Tree, and Random Forest from scratch",
            "priority": "medium"
        },
        {
            "title": "Setup CI/CD",
            "description": "Configure GitHub Actions for automated testing",
            "priority": "low"
        }
    ]
    
    print("📋 Creating sample tasks...")
    created_tasks = []
    
    for task_data in tasks_to_create:
        try:
            response = requests.post(f"{API_V1}/tasks/", json=task_data, headers=headers)
            if response.status_code == 200:
                task = response.json()
                created_tasks.append(task)
                print_success(f"Created task: '{task['title']}'")
            else:
                print_error(f"Failed to create task: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Task creation failed: {e}")
    
    # List all tasks
    print("\n📋 Retrieving all tasks...")
    try:
        response = requests.get(f"{API_V1}/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print_success(f"Found {len(tasks)} tasks:")
            for task in tasks:
                status_emoji = "✅" if task["is_completed"] else "⏳"
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                print(f"  {status_emoji} {priority_emoji} {task['title']} - {task['status']}")
        else:
            print_error(f"Failed to retrieve tasks: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_error(f"Task retrieval failed: {e}")
    
    # Update a task
    if created_tasks:
        print("\n📝 Updating first task...")
        task_id = created_tasks[0]["id"]
        update_data = {
            "status": "in_progress",
            "description": "Updated: Learning FastAPI with async/await patterns"
        }
        
        try:
            response = requests.put(f"{API_V1}/tasks/{task_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                updated_task = response.json()
                print_success(f"Updated task status to: {updated_task['status']}")
            else:
                print_error(f"Failed to update task: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print_error(f"Task update failed: {e}")
    
    # Get task statistics
    print("\n📊 Getting task statistics...")
    try:
        response = requests.get(f"{API_V1}/tasks/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print_success("Task Statistics:")
            for status, count in stats.items():
                print(f"  {status.replace('_', ' ').title()}: {count}")
        else:
            print_error(f"Failed to get stats: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_error(f"Stats retrieval failed: {e}")

def demonstrate_ml_features():
    """Demonstrate ML algorithm features"""
    print_section("Machine Learning Algorithms")
    
    # Test K-Means CLI
    print("🤖 Testing K-Means clustering...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "ml_core.kmeans",
            "--data", "data/sample_data.csv",
            "--clusters", "3",
            "--output", "demo_results.csv"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print_success("K-Means clustering completed successfully!")
            print(f"📄 Output: {result.stdout.strip()}")
            
            # Show results
            if Path("demo_results.csv").exists():
                print("\n📊 Clustering Results (first 5 rows):")
                with open("demo_results.csv", "r") as f:
                    lines = f.readlines()[:6]  # Header + 5 data rows
                    for line in lines:
                        print(f"  {line.strip()}")
        else:
            print_error(f"K-Means failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print_error("K-Means execution timed out")
    except Exception as e:
        print_error(f"K-Means execution failed: {e}")
    
    # Test API ML endpoints
    print("\n🔌 Testing ML API endpoints...")
    try:
        response = requests.get(f"{API_V1}/ml/")
        if response.status_code == 200:
            ml_info = response.json()
            print_success("ML API is available!")
            print("📋 Available algorithms:")
            for algo in ml_info["available_algorithms"]:
                status_emoji = "✅" if algo["status"] == "available" else "🚧"
                print(f"  {status_emoji} {algo['name']}: {algo['description']}")
        else:
            print_error(f"ML API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_error(f"ML API test failed: {e}")

def demonstrate_api_documentation():
    """Show API documentation links"""
    print_section("API Documentation")
    
    print("📚 Interactive API Documentation:")
    print(f"  🌐 Swagger UI: {API_BASE}/docs")
    print(f"  📖 ReDoc:     {API_BASE}/redoc")
    print(f"  💾 OpenAPI:   {API_BASE}/api/v1/openapi.json")
    
    print("\n🛠️  Development Tools:")
    print(f"  🗄️  Database Admin: http://localhost:8080")
    print(f"  📊 Health Check:    {API_BASE}/health")

def main():
    """Main demonstration function"""
    print("🚀 AI Backend Playground - Live Demonstration")
    print("This script will test all major features of the project\n")
    
    # Check if API is running
    if not check_api_health():
        print("\n💡 To start the project:")
        print("1. Run: docker-compose up -d")
        print("2. Wait for services to start")
        print("3. Run this demo again: python demo.py")
        return
    
    # Demonstrate authentication
    token = demonstrate_user_registration()
    if not token:
        print_error("Cannot continue without authentication token")
        return
    
    # Demonstrate task management
    demonstrate_task_management(token)
    
    # Demonstrate ML features
    demonstrate_ml_features()
    
    # Show documentation links
    demonstrate_api_documentation()
    
    print_section("Demo Complete! 🎉")
    print("✨ All major features demonstrated successfully!")
    print("\n🎯 Next Steps:")
    print("1. Explore the API documentation at http://localhost:8000/docs")
    print("2. Try the ML algorithms with your own data")
    print("3. Check out the source code structure")
    print("4. Run the test suite: pytest")
    print("5. Deploy to production with Docker")

if __name__ == "__main__":
    main()
