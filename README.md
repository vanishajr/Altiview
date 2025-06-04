# React + Flask Web Application

This is a full-stack web application using React (TypeScript) for the frontend and Flask for the backend.

## Project Structure
- `frontend/` - React TypeScript application
- `backend/` - Flask Python application

## Running the Application

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
   The backend will run on http://localhost:5000

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on http://localhost:5173

## Features
- React frontend with TypeScript
- Flask backend with CORS support
- Hot reloading for both frontend and backend
- Environment variable support 