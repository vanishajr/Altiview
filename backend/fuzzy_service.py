import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json

class FlightRiskAnalyzer:
    def __init__(self):
        # Define the universe of variables
        self.temperature = np.arange(-20, 51, 1)  # Extended range to include cold temperatures, adjusted end for arange
        self.humidity = np.arange(0, 101, 1) # Adjusted end for arange
        self.wind_speed = np.arange(0, 101, 1) # Adjusted end for arange
        self.visibility = np.arange(0, 10.1, 0.1) # Adjusted end for arange
        self.risk = np.arange(0, 101, 1)

        # Define membership functions for temperature
        self.temp_very_low = fuzz.trimf(self.temperature, [-20, -10, 5]) # Extended range overlap
        self.temp_low = fuzz.trimf(self.temperature, [0, 10, 22]) # Adjusted range overlap
        self.temp_medium = fuzz.trimf(self.temperature, [18, 28, 38]) # Adjusted range overlap
        self.temp_high = fuzz.trimf(self.temperature, [35, 42, 50]) # Adjusted range overlap
        self.temp_very_high = fuzz.trimf(self.temperature, [40, 45, 50])

        # Define membership functions for humidity
        self.humidity_very_low = fuzz.trimf(self.humidity, [0, 10, 25]) # Extended range overlap
        self.humidity_low = fuzz.trimf(self.humidity, [20, 35, 50]) # Adjusted range overlap
        self.humidity_medium = fuzz.trimf(self.humidity, [45, 60, 75]) # Adjusted range overlap
        self.humidity_high = fuzz.trimf(self.humidity, [70, 85, 95]) # Adjusted range overlap
        self.humidity_very_high = fuzz.trimf(self.humidity, [90, 95, 100]) # Adjusted range overlap

        # Define membership functions for wind speed
        self.wind_calm = fuzz.trimf(self.wind_speed, [0, 5, 15]) # Extended range overlap
        self.wind_light = fuzz.trimf(self.wind_speed, [10, 25, 40]) # Adjusted range overlap
        self.wind_moderate = fuzz.trimf(self.wind_speed, [30, 50, 70]) # Adjusted range overlap
        self.wind_strong = fuzz.trimf(self.wind_speed, [60, 75, 90]) # Adjusted range overlap
        self.wind_severe = fuzz.trimf(self.wind_speed, [85, 95, 100]) # Adjusted range overlap

        # Define membership functions for visibility
        self.visibility_very_low = fuzz.trimf(self.visibility, [0, 1, 3]) # Extended range overlap
        self.visibility_low = fuzz.trimf(self.visibility, [2, 4, 6]) # Adjusted range overlap
        self.visibility_medium = fuzz.trimf(self.visibility, [5, 6.5, 8]) # Adjusted range overlap
        self.visibility_good = fuzz.trimf(self.visibility, [7, 8.5, 10]) # Adjusted range overlap
        self.visibility_excellent = fuzz.trimf(self.visibility, [9, 9.5, 10]) # Adjusted range overlap

        # Define membership functions for risk
        self.risk_very_low = fuzz.trimf(self.risk, [0, 10, 20])
        self.risk_low = fuzz.trimf(self.risk, [15, 25, 35])
        self.risk_medium = fuzz.trimf(self.risk, [30, 50, 70])
        self.risk_high = fuzz.trimf(self.risk, [65, 75, 85])
        self.risk_very_high = fuzz.trimf(self.risk, [80, 90, 100])

        # Create fuzzy control system
        self.setup_fuzzy_system()

    def setup_fuzzy_system(self):
        # Create fuzzy variables
        temp = ctrl.Antecedent(self.temperature, 'temperature')
        humidity = ctrl.Antecedent(self.humidity, 'humidity')
        wind = ctrl.Antecedent(self.wind_speed, 'wind_speed')
        visibility = ctrl.Antecedent(self.visibility, 'visibility')
        risk = ctrl.Consequent(self.risk, 'risk')

        # Define membership functions
        temp['very_low'] = self.temp_very_low
        temp['low'] = self.temp_low
        temp['medium'] = self.temp_medium
        temp['high'] = self.temp_high
        temp['very_high'] = self.temp_very_high

        humidity['very_low'] = self.humidity_very_low
        humidity['low'] = self.humidity_low
        humidity['medium'] = self.humidity_medium
        humidity['high'] = self.humidity_high
        humidity['very_high'] = self.humidity_very_high

        wind['calm'] = self.wind_calm
        wind['light'] = self.wind_light
        wind['moderate'] = self.wind_moderate
        wind['strong'] = self.wind_strong
        wind['severe'] = self.wind_severe

        visibility['very_low'] = self.visibility_very_low
        visibility['low'] = self.visibility_low
        visibility['medium'] = self.visibility_medium
        visibility['good'] = self.visibility_good
        visibility['excellent'] = self.visibility_excellent

        risk['very_low'] = self.risk_very_low
        risk['low'] = self.risk_low
        risk['medium'] = self.risk_medium
        risk['high'] = self.risk_high
        risk['very_high'] = self.risk_very_high

        # Define rules for takeoff
        takeoff_rules = [
            # Ideal conditions
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['very_low']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['good'], risk['low']),
            
            # Temperature variations
            ctrl.Rule(temp['very_low'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['medium']),
            ctrl.Rule(temp['high'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['medium']),
             ctrl.Rule(temp['very_high'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['high']),
            
            # Humidity variations
            ctrl.Rule(temp['medium'] & humidity['very_high'] & wind['calm'] & visibility['excellent'], risk['medium']),
            ctrl.Rule(temp['medium'] & humidity['very_low'] & wind['calm'] & visibility['excellent'], risk['low']),
            
            # Wind variations
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['medium'], risk['medium']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['moderate'] & visibility['good'], risk['medium']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['strong'] & visibility['medium'], risk['high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['severe'] & visibility['medium'], risk['very_high']),
            
            # Visibility variations
             ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['low'], risk['medium']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['very_low'], risk['high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['low'], risk['medium']),
            
            # Combined adverse conditions
            ctrl.Rule(temp['high'] & humidity['high'] & wind['moderate'] & visibility['medium'], risk['high']),
            ctrl.Rule(temp['very_high'] & humidity['very_high'] & wind['moderate'] & visibility['medium'], risk['very_high']),
            ctrl.Rule(temp['low'] & humidity['high'] & wind['strong'] & visibility['low'], risk['high']),
            ctrl.Rule(temp['very_low'] & humidity['very_high'] & wind['strong'] & visibility['low'], risk['very_high']),
            ctrl.Rule(temp['high'] & humidity['high'] & wind['severe'] & visibility['very_low'], risk['very_high']),
             ctrl.Rule(temp['very_high'] & humidity['very_high'] & wind['severe'] & visibility['very_low'], risk['very_high'])
        ]

        # Define rules for landing
        landing_rules = [
            # Ideal conditions
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['very_low']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['good'], risk['low']),
            
            # Temperature variations
            ctrl.Rule(temp['very_low'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['medium']),
            ctrl.Rule(temp['high'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['medium']),
             ctrl.Rule(temp['very_high'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['high']),
            
            # Humidity variations
            ctrl.Rule(temp['medium'] & humidity['very_high'] & wind['calm'] & visibility['excellent'], risk['medium']),
            ctrl.Rule(temp['medium'] & humidity['very_low'] & wind['calm'] & visibility['excellent'], risk['low']),
            
            # Wind variations (more strict for landing)
             ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['medium'], risk['high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['moderate'] & visibility['good'], risk['high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['strong'] & visibility['medium'], risk['very_high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['severe'] & visibility['medium'], risk['very_high']),
            
            # Visibility variations (more strict for landing)
             ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['low'], risk['high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['very_low'], risk['very_high']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['low'], risk['very_high']),
            
            # Combined adverse conditions
             ctrl.Rule(temp['high'] & humidity['high'] & wind['moderate'] & visibility['medium'], risk['very_high']),
            ctrl.Rule(temp['very_high'] & humidity['very_high'] & wind['moderate'] & visibility['medium'], risk['very_high']),
             ctrl.Rule(temp['low'] & humidity['high'] & wind['strong'] & visibility['low'], risk['very_high']),
            ctrl.Rule(temp['very_low'] & humidity['very_high'] & wind['strong'] & visibility['low'], risk['very_high']),
             ctrl.Rule(temp['high'] & humidity['high'] & wind['severe'] & visibility['very_low'], risk['very_high']),
            ctrl.Rule(temp['very_high'] & humidity['very_high'] & wind['severe'] & visibility['very_low'], risk['very_high'])
        ]

        # Create control systems
        self.takeoff_ctrl = ctrl.ControlSystem(takeoff_rules)
        self.landing_ctrl = ctrl.ControlSystem(landing_rules)

        # Create simulators
        self.takeoff_sim = ctrl.ControlSystemSimulation(self.takeoff_ctrl)
        self.landing_sim = ctrl.ControlSystemSimulation(self.landing_ctrl)

    def calculate_risks(self, temperature, humidity, wind_speed, visibility):
        try:
            # Calculate takeoff risk
            self.takeoff_sim.input['temperature'] = temperature
            self.takeoff_sim.input['humidity'] = humidity
            self.takeoff_sim.input['wind_speed'] = wind_speed
            self.takeoff_sim.input['visibility'] = visibility
            self.takeoff_sim.compute()
            # Check if 'risk' is in output and not NaN, otherwise return a default or handle
            takeoff_risk = float(self.takeoff_sim.output['risk']) if 'risk' in self.takeoff_sim.output and not np.isnan(self.takeoff_sim.output['risk']) else 50.0

            # Calculate landing risk
            self.landing_sim.input['temperature'] = temperature
            self.landing_sim.input['humidity'] = humidity
            self.landing_sim.input['wind_speed'] = wind_speed
            self.landing_sim.input['visibility'] = visibility
            self.landing_sim.compute()
            # Check if 'risk' is in output and not NaN, otherwise return a default or handle
            landing_risk = float(self.landing_sim.output['risk']) if 'risk' in self.landing_sim.output and not np.isnan(self.landing_sim.output['risk']) else 50.0

            return {
                'takeoff_risk': round(takeoff_risk, 2),
                'landing_risk': round(landing_risk, 2),
                'conditions': {
                    'temperature': temperature,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'visibility': visibility
                }
            }
        except Exception as e:
            print(f"Error in calculate_risks: {str(e)}")
            # Return default values if calculation fails
            return {
                'takeoff_risk': 50.0,
                'landing_risk': 50.0,
                'conditions': {
                    'temperature': temperature,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'visibility': visibility
                }
            }

# Create default values
DEFAULT_CONDITIONS = {
    'temperature': 25,
    'humidity': 50,
    'wind_speed': 15,
    'visibility': 8
}

# Create analyzer instance
analyzer = FlightRiskAnalyzer() 