import sqlite3
import os
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP(name="SQL Database Server")

# Database configuration
DB_PATH = Path(__file__).parent / "sample_db.db"

def initialize_database():
    """Initialize database if it doesn't exist, otherwise connect to existing one."""
    db_exists = DB_PATH.exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    if not db_exists:
        # Create sample table if database is new
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print(f"[OK] New database created at: {DB_PATH}")
    else:
        print(f"[OK] Connected to existing database at: {DB_PATH}")
    
    conn.close()

# Initialize database on startup
initialize_database()

@mcp.tool
def execute_query(query: str) -> dict:
    """Execute a SELECT query and return results."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "data": [dict(row) for row in results],
            "row_count": len(results)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def insert_user(name: str, email: str, age: int = None) -> dict:
    """Insert a new user into the users table."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return {
            "success": True,
            "message": f"User inserted successfully",
            "user_id": user_id
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def insert_product(name: str, price: float, quantity: int = 0) -> dict:
    """Insert a new product into the products table."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            (name, price, quantity)
        )
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        
        return {
            "success": True,
            "message": f"Product inserted successfully",
            "product_id": product_id
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def get_all_users() -> dict:
    """Retrieve all users from the database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "users": [dict(user) for user in users],
            "count": len(users)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def get_all_products() -> dict:
    """Retrieve all products from the database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        
        return {
            "success": True,
            "products": [dict(p) for p in products],
            "count": len(products)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def update_user(user_id: int, name: str = None, email: str = None, age: int = None) -> dict:
    """Update a user record in the database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        if age is not None:
            updates.append("age = ?")
            params.append(age)
        
        if not updates:
            conn.close()
            return {"success": False, "error": "No fields to update"}
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"User {user_id} updated successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def delete_user(user_id: int) -> dict:
    """Delete a user from the database."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"User {user_id} deleted successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def custom_sql(sql_query: str) -> dict:
    """Execute a custom SQL query (SELECT, INSERT, UPDATE, or DELETE)."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        
        # Check if it's a SELECT query
        if sql_query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            conn.close()
            return {
                "success": True,
                "data": [dict(row) for row in results],
                "row_count": len(results)
            }
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            conn.close()
            return {
                "success": True,
                "message": "Query executed successfully",
                "rows_affected": cursor.rowcount
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool
def get_database_info() -> dict:
    """Get information about the database and its tables."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        table_info = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            table_info[table] = [dict(col) for col in columns]
        
        conn.close()
        
        return {
            "success": True,
            "database_path": str(DB_PATH),
            "tables": tables,
            "table_info": table_info
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run()