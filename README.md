# SQL Database Server - MCP (Model Context Protocol)

A FastMCP server that provides comprehensive SQL tools for database operations using SQLite. This server allows Claude Desktop to execute database queries, manage records, and perform CRUD operations on a local SQLite database.

## Features

✨ **All-in-one SQL Database Tools:**
- Execute custom SQL queries
- Insert/Update/Delete records
- Retrieve user and product data
- Get database schema information
- Automatic database initialization

🗄️ **SQLite Database:**
- Local database file (`sample_db.db`) created automatically
- Pre-built sample tables (users, products)
- Persistent data storage

🔌 **MCP Integration:**
- Works seamlessly with Claude Desktop
- 9 powerful tools available via MCP protocol

---

## Installation

### Prerequisites
- Python 3.11 or higher
- `uv` package manager (or pip)

### Setup

1. **Clone or navigate to project:**
   ```bash
   cd c:\Users\******\Downloads\projects\first_MCP
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   Or if using pip:
   ```bash
   pip install fastmcp
   ```

---

## Running the Server

### Option 1: Development Mode (with Inspector)
```bash
uv run fastmcp dev inspector my_server.py
```
This opens an interactive inspector at `http://localhost:8000` where you can test tools directly.

### Option 2: Production Mode
```bash
uv run fastmcp run my_server.py
```

### Option 3: Direct Python
```bash
uv run my_server.py
```

---

## 🔧 Available Tools

### 1. **execute_query** (SELECT queries)
Execute SELECT queries and retrieve results.
```
Input: query (string)
Output: { success, data[], row_count }
```
Example: `SELECT * FROM users WHERE age > 18`

---

### 2. **insert_user**
Add a new user to the database.
```
Input: name (string), email (string), age (int, optional)
Output: { success, message, user_id }
```

---

### 3. **insert_product**
Add a new product to the database.
```
Input: name (string), price (float), quantity (int, optional)
Output: { success, message, product_id }
```

---

### 4. **get_all_users**
Retrieve all users from the database.
```
Output: { success, users[], count }
```

---

### 5. **get_all_products**
Retrieve all products from the database.
```
Output: { success, products[], count }
```

---

### 6. **update_user**
Update a user's information.
```
Input: user_id (int), name (optional), email (optional), age (optional)
Output: { success, message }
```

---

### 7. **delete_user**
Delete a user from the database.
```
Input: user_id (int)
Output: { success, message }
```

---

### 8. **custom_sql**
Execute any SQL query (SELECT, INSERT, UPDATE, DELETE).
```
Input: sql_query (string)
Output: { success, data/message, rows_affected }
```

---

### 9. **get_database_info**
View database structure, tables, and column information.
```
Output: { success, database_path, tables[], table_info }
```

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 🔗 Connecting with Claude Desktop

### Step 1: Locate Claude Desktop Config
The config file is located at:
```
Windows: C:\Users\{YourUsername}\AppData\Roaming\Claude\claude_desktop_config.json
macOS: ~/Library/Application\ Support/Claude/claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
```

### Step 2: Update Config File
Add or update the `SQL Database Server` entry in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "SQL Database Server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "C:\\Users\\**********\\Downloads\\projects\\first_MCP\\my_server.py"
      ],
      "env": {},
      "transport": "stdio",
      "cwd": "C:\\Users\\******\\Downloads\\projects\\first_MCP",
      "keep_alive": true,
      "description": "SQL Database Server with 9 tools for database operations"
    }
  }
}
```

**⚠️ Important:** Replace `C:\\Users\\******\\Downloads\\projects\\first_MCP` with your actual project path.

### Step 3: Restart Claude Desktop
1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. The SQL Database Server should now appear in the MCP tools list

### Step 4: Start Using the Tools
In Claude Desktop, ask about database operations and use any of the 9 tools:
- "Add a new user to the database"
- "Show me all products"
- "Update user 1's information"
- "Execute this SQL query..."
- "What tables are in the database?"

---

## 📁 Database File Location

The `sample_db.db` file is automatically created in the project root directory:
```
c:\Users\******\Downloads\projects\first_MCP\sample_db.db
```

**Auto-creation logic:**
- ✅ If `sample_db.db` doesn't exist → Creates new database with sample tables
- ✅ If `sample_db.db` exists → Connects to existing database (preserves data)

---

## 🧪 Testing Tools

### Test in Inspector (Recommended)
```bash
uv run fastmcp dev inspector my_server.py
```
Then visit `http://localhost:8000` and try each tool interactively.

### Test Tool Examples

**Get all users:**
```json
{
  "name": "get_all_users"
}
```

**Insert a new user:**
```json
{
  "name": "insert_user",
  "arguments": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

**Custom SQL query:**
```json
{
  "name": "custom_sql",
  "arguments": {
    "sql_query": "SELECT * FROM users WHERE age > 25"
  }
}
```

---

## 🚀 Quick Start Example

```bash
# 1. Navigate to project
cd c:\Users\kulde\Downloads\projects\first_MCP

# 2. Run the server
uv run fastmcp run my_server.py

# 3. In another terminal, or in Claude Desktop, execute a tool:
# Insert a user, get all products, update records, etc.
```

---

## 📝 Project Structure

```
first_MCP/
├── my_server.py          # MCP server with all tools
├── pyproject.toml        # Project configuration
├── README.md             # This file
├── main.py               # Helper script
└── sample_db.db          # SQLite database (auto-created)
```

---

## 🔧 Troubleshooting

### Issue: "charmap codec can't encode character"
**Solution:** Already fixed! The server now uses ASCII-safe output.

### Issue: Database file not created
**Solution:** Ensure the project directory has write permissions. The file will be created automatically on first server startup.

### Issue: Claude Desktop can't connect
**Solution:** 
1. Check the path is correct in `claude_desktop_config.json`
2. Restart Claude Desktop
3. Verify firewall isn't blocking local connections

### Issue: "sqlite3.IntegrityError: UNIQUE constraint failed: users.email"
**Solution:** Each email must be unique. Use a different email for new users.

---

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---


## License

This project is open source and available under the MIT License.

---




