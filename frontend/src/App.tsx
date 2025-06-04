import { useState } from 'react'
import { Login } from './components/Login'
import { Signup } from './components/Signup'
import { RiskAnalysis } from './components/RiskAnalysis'
import './App.css'

function App() {
  const [isLogin, setIsLogin] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [userType, setUserType] = useState('')

  const handleAuthSuccess = (type: string) => {
    setIsAuthenticated(true)
    setUserType(type)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setUserType('')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Flight Management System</h1>
        {isAuthenticated && (
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        )}
      </header>

      <div className="app-container">
        {!isAuthenticated ? (
          <>
            {isLogin ? (
              <Login onAuthSuccess={handleAuthSuccess} />
            ) : (
              <Signup onAuthSuccess={handleAuthSuccess} />
            )}
            <p className="switch-auth">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                className="switch-button"
                onClick={() => setIsLogin(!isLogin)}
              >
                {isLogin ? 'Sign up' : 'Login'}
              </button>
            </p>
          </>
        ) : (
          <RiskAnalysis userType={userType} />
        )}
      </div>
    </div>
  )
}

export default App
