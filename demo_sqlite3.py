from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# Database setup
DATABASE = 'database.db'

# Function to get a database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows treating rows as dictionaries
    return conn

# Create table if it doesn't exist
def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE
                    );''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models for request and response validation
class User(BaseModel):
    name: str
    email: str

class UserResponse(User):
    id: int

# CREATE operation - Add a new user
@app.post("/users/", response_model=UserResponse)
def create_user(user: User):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (user.name, user.email))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return UserResponse(id=user_id, name=user.name, email=user.email)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")

# READ operation - Get all users
@app.get("/users/", response_model=List[UserResponse])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return [UserResponse(id=user['id'], name=user['name'], email=user['email']) for user in users]

# READ operation - Get a single user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return UserResponse(id=user['id'], name=user['name'], email=user['email'])
    else:
        raise HTTPException(status_code=404, detail="User not found")

# UPDATE operation - Update user information
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (user.name, user.email, user_id))
        conn.commit()
        conn.close()
        return UserResponse(id=user_id, name=user.name, email=user.email)
    else:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

# DELETE operation - Delete a user by ID
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return {"message": "User deleted successfully"}
    else:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

# Start FastAPI application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
