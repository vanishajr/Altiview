import { useEffect, useState } from 'react';

interface DashboardProps {
  userType: string;
  onLogout: () => void;
}

export function Dashboard({ userType, onLogout }: DashboardProps) {
  const [userData, setUserData] = useState<{ email: string } | null>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/user', {
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        }
      } catch (err) {
        console.error('Failed to fetch user data:', err);
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5000/api/logout', {
        credentials: 'include',
      });
      onLogout();
    } catch (err) {
      console.error('Failed to logout:', err);
    }
  };

  return (
    <div className="dashboard">
      <h2>Welcome to your {userType} Dashboard</h2>
      {userData && <p>Logged in as: {userData.email}</p>}
      
      {userType === 'pilot' ? (
        <div className="pilot-dashboard">
          <h3>Pilot Features</h3>
          <ul>
            <li>View assigned flights</li>
            <li>Update flight status</li>
            <li>View passenger manifest</li>
          </ul>
        </div>
      ) : (
        <div className="passenger-dashboard">
          <h3>Passenger Features</h3>
          <ul>
            <li>Book flights</li>
            <li>View booking history</li>
            <li>Check flight status</li>
          </ul>
        </div>
      )}
      
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
} 