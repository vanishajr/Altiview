import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FlightRiskAnalyzer:
    def __init__(self):
        # Define universes
        self.temperature = np.arange(-20, 51, 1)
        self.humidity = np.arange(0, 101, 1)
        self.wind_speed = np.arange(0, 101, 1)
        self.visibility = np.arange(0, 10.1, 0.1)
        self.risk = np.arange(0, 101, 1)

        # Membership functions for temperature
        self.temp_very_low = fuzz.trimf(self.temperature, [-20, -10, 0])
        self.temp_low = fuzz.trimf(self.temperature, [-5, 5, 15])
        self.temp_medium = fuzz.trimf(self.temperature, [10, 20, 30])
        self.temp_high = fuzz.trimf(self.temperature, [25, 35, 42])
        self.temp_very_high = fuzz.trimf(self.temperature, [38, 45, 50])

        # Membership functions for humidity
        self.humidity_very_low = fuzz.trimf(self.humidity, [0, 10, 25])
        self.humidity_low = fuzz.trimf(self.humidity, [15, 30, 45])
        self.humidity_medium = fuzz.trimf(self.humidity, [40, 55, 70])
        self.humidity_high = fuzz.trimf(self.humidity, [65, 80, 90])
        self.humidity_very_high = fuzz.trimf(self.humidity, [85, 95, 100])

        # Membership functions for wind speed
        self.wind_calm = fuzz.trimf(self.wind_speed, [0, 5, 10])
        self.wind_light = fuzz.trimf(self.wind_speed, [8, 15, 25])
        self.wind_moderate = fuzz.trimf(self.wind_speed, [20, 35, 50])
        self.wind_strong = fuzz.trimf(self.wind_speed, [45, 60, 75])
        self.wind_severe = fuzz.trimf(self.wind_speed, [70, 85, 100])

        # Membership functions for visibility
        self.visibility_very_low = fuzz.trimf(self.visibility, [0, 0.5, 1.5])
        self.visibility_low = fuzz.trimf(self.visibility, [1, 2.5, 4])
        self.visibility_medium = fuzz.trimf(self.visibility, [3.5, 5.5, 7])
        self.visibility_good = fuzz.trimf(self.visibility, [6.5, 8, 9])
        self.visibility_excellent = fuzz.trimf(self.visibility, [8.5, 9.5, 10])

        # Membership functions for risk
        self.risk_very_low = fuzz.trimf(self.risk, [0, 10, 20])
        self.risk_low = fuzz.trimf(self.risk, [15, 30, 45])
        self.risk_medium = fuzz.trimf(self.risk, [40, 55, 70])
        self.risk_high = fuzz.trimf(self.risk, [65, 80, 90])
        self.risk_very_high = fuzz.trimf(self.risk, [85, 95, 100])

        # Setup control systems
        self.setup_fuzzy_system()

    def setup_fuzzy_system(self):
        temp = ctrl.Antecedent(self.temperature, 'temperature')
        humidity = ctrl.Antecedent(self.humidity, 'humidity')
        wind = ctrl.Antecedent(self.wind_speed, 'wind_speed')
        visibility = ctrl.Antecedent(self.visibility, 'visibility')
        risk = ctrl.Consequent(self.risk, 'risk')

        # Assign membership functions
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

        # Define rules for takeoff (slightly less strict than landing)
        takeoff_rules = [
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['very_low']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['good'], risk['low']),
            ctrl.Rule(temp['very_low'] | temp['very_high'], risk['medium']),
            ctrl.Rule(wind['moderate'] | wind['strong'], risk['high']),
            ctrl.Rule(wind['severe'] | visibility['very_low'], risk['very_high']),
            ctrl.Rule(visibility['low'] & wind['light'], risk['medium']),
            ctrl.Rule(temp['high'] & humidity['high'] & wind['moderate'], risk['high']),
            ctrl.Rule(temp['very_high'] & humidity['very_high'] & wind['severe'], risk['very_high']),
        ]

        # Define rules for landing (more strict)
        landing_rules = [
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['calm'] & visibility['excellent'], risk['very_low']),
            ctrl.Rule(temp['medium'] & humidity['medium'] & wind['light'] & visibility['good'], risk['low']),
            ctrl.Rule(temp['very_low'] | temp['very_high'], risk['high']),
            ctrl.Rule(wind['moderate'] & visibility['medium'], risk['high']),
            ctrl.Rule(wind['strong'] | wind['severe'], risk['very_high']),
            ctrl.Rule(visibility['very_low'] | visibility['low'], risk['very_high']),
            ctrl.Rule(humidity['very_high'] & temp['high'] & visibility['medium'], risk['very_high']),
        ]

        self.takeoff_ctrl = ctrl.ControlSystem(takeoff_rules)
        self.landing_ctrl = ctrl.ControlSystem(landing_rules)

        self.takeoff_sim = ctrl.ControlSystemSimulation(self.takeoff_ctrl)
        self.landing_sim = ctrl.ControlSystemSimulation(self.landing_ctrl)

    def calculate_risks(self, temperature, humidity, wind_speed, visibility):
        try:
            self.takeoff_sim.input['temperature'] = temperature
            self.takeoff_sim.input['humidity'] = humidity
            self.takeoff_sim.input['wind_speed'] = wind_speed
            self.takeoff_sim.input['visibility'] = visibility
            self.takeoff_sim.compute()
            takeoff_risk = float(self.takeoff_sim.output['risk']) if 'risk' in self.takeoff_sim.output else 50.0

            self.landing_sim.input['temperature'] = temperature
            self.landing_sim.input['humidity'] = humidity
            self.landing_sim.input['wind_speed'] = wind_speed
            self.landing_sim.input['visibility'] = visibility
            self.landing_sim.compute()
            landing_risk = float(self.landing_sim.output['risk']) if 'risk' in self.landing_sim.output else 50.0

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
            print(f"Error: {str(e)}")
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

# Optional: Default values for testing
if __name__ == "__main__":
    analyzer = FlightRiskAnalyzer()
    sample = analyzer.calculate_risks(temperature=22, humidity=50, wind_speed=20, visibility=6)
    print(sample)
