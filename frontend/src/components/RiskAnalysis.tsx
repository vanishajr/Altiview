import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface RiskAnalysisProps {
  userType: string;
}

interface Conditions {
  temperature: number;
  humidity: number;
  wind_speed: number;
  visibility: number;
}

interface RiskData {
  takeoff_risk: number;
  landing_risk: number;
  conditions: Conditions;
}

export function RiskAnalysis({ userType }: RiskAnalysisProps) {
  const [conditions, setConditions] = useState<Conditions>({
    temperature: 25,
    humidity: 50,
    wind_speed: 15,
    visibility: 8
  });
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [error, setError] = useState('');

  const fetchRiskAnalysis = async (newConditions?: Conditions) => {
    try {
      const response = await fetch('http://localhost:5000/api/risk-analysis', {
        method: newConditions ? 'POST' : 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: newConditions ? JSON.stringify(newConditions) : undefined,
      });

      if (!response.ok) {
        throw new Error('Failed to fetch risk analysis');
      }

      const data = await response.json();
      setRiskData(data);
      if (!newConditions) {
        setConditions(data.conditions);
      }
    } catch (err) {
      setError('Failed to fetch risk analysis');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchRiskAnalysis();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setConditions(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchRiskAnalysis(conditions);
  };

  const chartData = {
    labels: ['Takeoff Risk', 'Landing Risk'],
    datasets: [
      {
        label: 'Risk Percentage',
        data: riskData ? [riskData.takeoff_risk, riskData.landing_risk] : [0, 0],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        fill: false,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Flight Risk Analysis',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Risk Percentage'
        }
      }
    }
  };

  return (
    <div className="risk-analysis">
      <h2>Flight Risk Analysis</h2>
      {error && <p className="error">{error}</p>}
      
      {userType === 'pilot' ? (
        <form onSubmit={handleSubmit} className="conditions-form">
          <div>
            <label htmlFor="temperature">Temperature (°C)</label>
            <input
              type="number"
              id="temperature"
              name="temperature"
              value={conditions.temperature}
              onChange={handleInputChange}
              min="0"
              max="50"
              step="0.1"
            />
          </div>
          <div>
            <label htmlFor="humidity">Humidity (%)</label>
            <input
              type="number"
              id="humidity"
              name="humidity"
              value={conditions.humidity}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="1"
            />
          </div>
          <div>
            <label htmlFor="wind_speed">Wind Speed (km/h)</label>
            <input
              type="number"
              id="wind_speed"
              name="wind_speed"
              value={conditions.wind_speed}
              onChange={handleInputChange}
              min="0"
              max="100"
              step="1"
            />
          </div>
          <div>
            <label htmlFor="visibility">Visibility (km)</label>
            <input
              type="number"
              id="visibility"
              name="visibility"
              value={conditions.visibility}
              onChange={handleInputChange}
              min="0"
              max="10"
              step="0.1"
            />
          </div>
          <button type="submit">Update Analysis</button>
        </form>
      ) : (
        <div className="conditions-display">
          <h3>Current Conditions</h3>
          <p>Temperature: {conditions.temperature}°C</p>
          <p>Humidity: {conditions.humidity}%</p>
          <p>Wind Speed: {conditions.wind_speed} km/h</p>
          <p>Visibility: {conditions.visibility} km</p>
        </div>
      )}

      {riskData && (
        <div className="risk-display">
          <div className="risk-chart">
            <Line data={chartData} options={chartOptions} />
          </div>
          <div className="risk-percentages">
            <div className="risk-item">
              <h3>Takeoff Risk</h3>
              <p className={`risk-value ${riskData.takeoff_risk > 70 ? 'high-risk' : riskData.takeoff_risk > 30 ? 'medium-risk' : 'low-risk'}`}>
                {riskData.takeoff_risk}%
              </p>
            </div>
            <div className="risk-item">
              <h3>Landing Risk</h3>
              <p className={`risk-value ${riskData.landing_risk > 70 ? 'high-risk' : riskData.landing_risk > 30 ? 'medium-risk' : 'low-risk'}`}>
                {riskData.landing_risk}%
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 