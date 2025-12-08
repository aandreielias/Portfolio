import time # Import the time module to track simulation time steps
import math # Import the math module for trigonometric and other calculations

class Simulator: # Define the main Simulator class that handles the vehicle physics
    def __init__(self): # Constructor method to initialize the state of the simulator
        self.throttle = 0.0 # Initialize the throttle input (gas pedal) to 0.0 (0% to 100%)
        self.brake = 0.0 # Initialize the brake input to 0.0 (0% to 100%)
        self.prev_throttle = 0.0 # Store the previous throttle value to detect rapid changes

        self.speed_mps = 0.0 # Initialize the vehicle speed in meters per second
        self.rpm = 800.0 # Initialize the engine RPM to a starting idle value
        self.gear = 1 # Start the vehicle in 1st gear
        self.mode = 'DRIVE' # Set the transmission mode to DRIVE

        self.fuel_liters = 90.0 # Set the fuel tank capacity/current level to 90 liters
        self.battery_lvl = 100.0 # Set the battery charge level to 100%

        self.odometer_km = 0.0 # Initialize the total distance traveled to 0.0 km
        self.current_fuel_rate_l_h = 0.0 # Initialize the current fuel consumption rate in liters per hour
        self.avg_fuel_consumption = 15.0 # Initialize average fuel consumption estimate to 15.0 L/100km
        self.current_afr = 14.7 # Set the initial Air-Fuel Ratio to the stoichiometric ratio
        self.range_km = 0.0 # Initialize the estimated driving range to 0.0 km

        self.torque_net_nm = 0.0 # Initialize the net torque output in Newton-meters
        self.power_hp = 0.0 # Initialize the power output in Horsepower
        self.accel_g = 0.0 # Initialize the acceleration G-force
        self.timer_0_100 = 0.0 # Initialize the 0-100 km/h acceleration timer
        self.best_0_100 = 0.0 # Initialize the record for the best 0-100 km/h time
        self.is_doing_0_100 = False # Flag to track if a 0-100 km/h run is currently active

        self.temp_coolant = 20.0 # Set initial coolant temperature to ambient (20°C)
        self.temp_oil = 20.0 # Set initial oil temperature to ambient (20°C)
        self.temp_trans = 20.0 # Set initial transmission fluid temperature to ambient (20°C)
        self.temp_block = 20.0 # Set initial engine block temperature to ambient (20°C)
        self.temp_cabin = 20.0 # Set initial cabin temperature to ambient (20°C)
        self.temp_ambient = 15.0 # Set the outside ambient air temperature to 15°C
        self.temp_intake = 15.0 # Set the intake air temperature to ambient (15°C)

        self.mass_kg = 2450.0 # Define the vehicle mass in kilograms (approx. VW Phaeton W12)
        self.drag_coeff = 0.32 # Define the aerodynamic drag coefficient
        self.frontal_area = 2.40 # Define the frontal area of the vehicle in square meters
        self.tire_radius = 0.35 # Define the tire radius in meters
        self.tire_circumference = 2.0 * math.pi * self.tire_radius # Calculate tire circumference from radius
        self.rolling_resistance_c = 0.012 # Define the coefficient of rolling resistance

        self.displacement = 6.0 # Define the engine displacement in liters (W12 engine)
        self.idle_rpm = 600.0 # Set the target idle RPM
        self.redline_rpm = 6200.0 # Set the maximum engine RPM (redline)
        self.inertia_engine = 0.65 # Set the engine rotational inertia (includes flywheel/crank)

        self.gear_ratios = {1: 3.57, 2: 2.20, 3: 1.51, 4: 1.00, 5: 0.80} # Define gear ratios for the 5-speed transmission
        self.final_drive = 3.07 # Define the final drive differential ratio
        self.shift_point_up = 5900 # RPM threshold to shift up
        self.shift_point_down = 1100 # RPM threshold to shift down
        self.lockup_active = False # Flag for torque converter lockup state
        self.converter_slip_rpm = 0.0 # Variable to track torque converter slip
        self.volumetric_efficiency = 0.0 # Variable to track volumetric efficiency

    def set_inputs(self, throttle, brake): # Method to update control inputs from the user
        self.prev_throttle = self.throttle # Save the current throttle as previous before updating
        self.throttle = max(0.0, min(1.0, throttle)) # Clamp throttle input between 0.0 and 1.0
        self.brake = max(0.0, min(1.0, brake)) # Clamp brake input between 0.0 and 1.0

    def _get_air_density(self): # Helper method to calculate air density based on intake temp
        temp_kelvin = self.temp_intake + 273.15 # Convert intake temperature to Kelvin
        return 1.225 * (288.15 / temp_kelvin) # Return air density using ideal gas law approximation

    def _get_torque_curve(self, rpm): # Helper to calculate engine torque based on RPM
        if rpm < 600: return 200 # Return base torque for very low RPM to prevent stalling
        if rpm < 2750: # Check if RPM is in the lower range
            factor = (rpm - 600) / (2750 - 600) # Calculate interpolation factor
            return 300 + (260 * factor) # Interpolate torque linearly
        elif rpm <= 5200: # Check if RPM is in the mid-range (peak torque band)
            return 560 # Return peak torque
        elif rpm <= 6500: # Check if RPM is in the high range
            factor = (rpm - 5200) / (6500 - 5200) # Calculate interpolation factor
            return 560 - (100 * factor) # Drop off torque linearly
        return 0 # Return 0 torque if above max RPM range

    def _get_volumetric_efficiency(self, rpm, throttle): # Calculate volumetric efficiency based on RPM and throttle
        ve_rpm = 0.85 + 0.15 * (1 - ((rpm - 4000)/3500)**2) # Approximate VE curve based on RPM (parabolic)
        ve_load = 0.15 + (0.85 * throttle) # Factor in throttle load effect
        return max(0.1, ve_rpm * ve_load) # Return combined VE, ensuring a minimum of 0.1

    def _calculate_engine_kinetics(self, dt, load_torque_nm): # Calculate engine physics (RPM change)
        max_torque = self._get_torque_curve(self.rpm) # Get theoretical max torque at current RPM
        actual_torque = max_torque * self.throttle # Scale torque by throttle input
        
        friction_torque = 20.0 + (self.rpm / 6000.0)**2 * 60.0 # Calculate internal friction torque
        if self.throttle < 0.05: # Add extra vacuum drag if throttle is closed
            vacuum_drag = (self.rpm / 3000.0) * 40.0 # Vacuum drag increases with RPM
            friction_torque += vacuum_drag # Add vacuum drag to total friction

        self.torque_net_nm = actual_torque - friction_torque - load_torque_nm # Calculate net torque acting on the crankshaft
        
        alpha = self.torque_net_nm / self.inertia_engine # Calculate angular acceleration (F=ma equivalent)
        rpm_change = (alpha * dt) * (60.0 / (2.0 * math.pi)) # Convert angular acceleration to RPM change
        
        self.rpm += rpm_change # Update engine RPM
        self.rpm = max(0, min(self.rpm, self.redline_rpm + 200)) # Clamp RPM between 0 and hard limit
        
        self.power_hp = (actual_torque * self.rpm) / 7120.0 # Calculate current power output in Horsepower

    def _calculate_chassis_kinetics(self, dt, drive_force_n): # Calculate vehicle movement physics
        rho = self._get_air_density() # Get current air density
        f_aero = 0.5 * rho * self.drag_coeff * self.frontal_area * (self.speed_mps ** 2) # Calculate aerodynamic drag force
        f_roll = self.rolling_resistance_c * self.mass_kg * 9.81 # Calculate rolling resistance force
        f_brake = self.brake * 18000.0 # Calculate braking force based on input
        f_mech = self.speed_mps * 10.0 # Calculate mechanical drivetrain loss force
        
        f_net = drive_force_n - f_aero - f_roll - f_brake - f_mech # Sum all forces acting on the vehicle
        
        if self.speed_mps <= 0.01 and f_net < 0: # Prevent backward movement from friction/brakes
            f_net = 0 # zero out net force
            self.speed_mps = 0 # zero out speed
            
        accel = f_net / self.mass_kg # Calculate acceleration (F=ma)
        self.speed_mps += accel * dt # Integrate acceleration to get speed
        if self.speed_mps < 0: self.speed_mps = 0 # Prevent negative speed
        
        self.accel_g = accel / 9.81 # Convert acceleration to G-force
        dist_km = (self.speed_mps * dt) / 1000.0 # Calculate distance traveled in this step
        self.odometer_km += dist_km # Update odometer
        
        speed_kmh = self.speed_mps * 3.6 # Convert speed to km/h
        if speed_kmh < 1.0: # Logic for resetting 0-100 timer
            self.is_doing_0_100 = False # Reset flag
            self.timer_0_100 = 0.0 # Reset timer
        elif speed_kmh > 1.0 and speed_kmh < 100.0: # Logic for active 0-100 run
            if not self.is_doing_0_100 and self.accel_g > 0.1: # Start run if accelerating
                self.is_doing_0_100 = True # Set flag to true
            if self.is_doing_0_100: # If run is valid
                self.timer_0_100 += dt # Increment timer
        elif speed_kmh >= 100.0 and self.is_doing_0_100: # Logic for completing 0-100 run
            self.best_0_100 = self.timer_0_100 # Save time
            self.is_doing_0_100 = False # Reset flag

    def _update_thermodynamics(self, dt): # Calculate heat transfer and temperatures
        c_iron = 450; m_block = 200.0 # specific heat and mass for engine block
        c_water = 4184; m_coolant = 15.0 # specific heat and mass for coolant
        c_oil = 1800; m_oil = 12.0 # specific heat and mass for oil
        c_atf = 2000; m_atf = 10.0 # specific heat and mass for transmission fluid
        
        heat_in_watts = self.current_fuel_rate_l_h * 150 # Estimate heat generation from fuel burn
        
        k_block_coolant = 50.0 + (self.rpm / 6000.0) * 300.0 # variable heat transfer coeff block->coolant
        q_block_coolant = k_block_coolant * (self.temp_block - self.temp_coolant) # calculate heat flow block->coolant
        
        k_block_oil = 20.0 + (self.rpm / 6000.0) * 80.0 # variable heat transfer coeff block->oil
        q_block_oil = k_block_oil * (self.temp_block - self.temp_oil) # calculate heat flow block->oil
        
        airflow = 5.0 + (self.speed_mps * 2.0) # calculate airflow speed over radiator
        thermostat = max(0.05, min(1.0, (self.temp_coolant - 82) / 10.0)) # calculate thermostat opening pct
        k_radiator = thermostat * airflow * 50.0 # calculate radiator efficiency
        q_coolant_air = k_radiator * (self.temp_coolant - self.temp_ambient) # calculate heat rejected to air
        
        q_oil_cooler = 15.0 * (self.temp_oil - self.temp_coolant) # calculate oil cooler heat exchange
        
        slip_rad_s = (self.converter_slip_rpm * 2 * math.pi) / 60.0 # calc slip speed in rad/s
        q_trans_slip = abs(self.torque_net_nm * slip_rad_s) * 0.5 # calc heat from converter slip
        q_trans_cool = 20.0 * (self.temp_trans - self.temp_ambient) * (1 + self.speed_mps/10) # calc trans cooling
        
        target_iat = self.temp_ambient + (self.temp_block - self.temp_ambient) * 0.15 # target intake temp
        cooling_iat = (self.speed_mps + 1.0) * 0.1 # cooling factor for intake
        self.temp_intake += (target_iat - self.temp_intake - cooling_iat) * 0.1 * dt # update intake temp
        self.temp_intake = max(self.temp_ambient, self.temp_intake) # ensure intake temp >= ambient
        
        self.temp_block += ((heat_in_watts - q_block_coolant - q_block_oil) / (m_block * c_iron)) * dt # update block temp
        self.temp_coolant += ((q_block_coolant + q_oil_cooler - q_coolant_air) / (m_coolant * c_water)) * dt # update coolant temp
        self.temp_oil += ((q_block_oil - q_oil_cooler) / (m_oil * c_oil)) * dt # update oil temp
        self.temp_trans += ((q_trans_slip - q_trans_cool) / (m_atf * c_atf)) * dt # update trans temp

        viscosity = 100 * math.exp(-0.03 * (self.temp_oil - 20)) # approximate oil viscosity
        raw_pressure = (self.rpm * 0.002) * (viscosity * 0.05) # calculate raw oil pressure
        self.oil_pressure_bar = min(7.0, max(0.5, raw_pressure)) if self.rpm > 300 else 0 # clamp pressure
        self.temp_cabin += (22.0 - self.temp_cabin) * 0.05 * dt # slowly normalize cabin temp

    def _calculate_fuel(self, dt): # Calculate fuel consumption
        rho_air = self._get_air_density() # Get air density
        self.volumetric_efficiency = self._get_volumetric_efficiency(self.rpm, self.throttle) # Get VE
        
        intake_flow_l_s = (self.rpm / 120.0) * self.displacement * self.volumetric_efficiency # Calc air flow volume
        air_mass_s = (intake_flow_l_s / 1000.0) * rho_air # Convert to mass flow
        
        self.current_afr = 14.7 # Target stoichiometric AFR
        if self.throttle > 0.7: self.current_afr = 12.5 # Enrich mixture at high load
        
        if self.throttle < 0.01 and self.rpm > 1200: # Deceleration fuel cutoff check
            fuel_mass_s = 0.0 # Cut fuel
            self.current_afr = 99.9 # Infinite AFR
        else: # Normal operation
            fuel_mass_s = air_mass_s / self.current_afr # Calculate fuel mass needed
            
        if (self.throttle - self.prev_throttle) > 0.1: # Acceleration enrichment
            fuel_mass_s *= 1.5 # Add extra fuel
            
        fuel_l_s = fuel_mass_s / 0.74 # Convert mass to volume (density approx)
        self.current_fuel_rate_l_h = fuel_l_s * 3600.0 # Convert to Liters/Hour
        self.fuel_liters = max(0, self.fuel_liters - (fuel_l_s * dt)) # Update fuel tank level
        
        speed_kmh = self.speed_mps * 3.6 # Get speed in km/h
        if speed_kmh > 10 and fuel_l_s > 0: # Calculate instantaneous MPGe equivalent
            current_l_100 = (self.current_fuel_rate_l_h / speed_kmh) * 100.0 # L/100km
            self.avg_fuel_consumption = (self.avg_fuel_consumption * 0.995) + (current_l_100 * 0.005) # Smooth average
            
        if self.avg_fuel_consumption > 0.1: # Calculate range
            self.range_km = (self.fuel_liters / self.avg_fuel_consumption) * 100.0 # Remaining range
        else: # Handle division by zero/low usage
            self.range_km = 999.0 # Max range display
            
        draw = 0.02 * dt # Base electrical draw
        gen = 0.06 * dt if self.rpm > 800 else 0 # Alternator generation
        self.battery_lvl = min(100, max(0, self.battery_lvl - draw + gen)) # Update battery level

    def update(self, dt): # Main update loop called every frame
        total_ratio = self.gear_ratios[self.gear] * self.final_drive # Calculate total gear reduction
        trans_out_rpm = (self.speed_mps / self.tire_circumference) * 60.0 * total_ratio # Calc logical transmission output RPM
        
        self.lockup_active = (self.gear >= 3 and self.speed_mps > 15) # Determine lockup state
        
        if self.lockup_active: # If torque converter is locked
            target_rpm = max(self.idle_rpm, trans_out_rpm) # Engine matches wheel speed (min idle)
            self.rpm = target_rpm # Set RPM
            self.converter_slip_rpm = 0.0 # No slip
            
            eng_torque = self._get_torque_curve(self.rpm) * self.throttle # Calculate engine torque
            if self.throttle < 0.01: eng_torque = -40.0 - (self.rpm/100) # Engine braking
            drive_force = (eng_torque * total_ratio) / self.tire_radius # Calculate wheel force
            
            self._calculate_engine_kinetics(dt, 0) # Update engine state
            
        else: # If torque converter is slipping
            self.converter_slip_rpm = self.rpm - trans_out_rpm # Calculate slip
            
            k_converter = 0.0045 # Fluid coupling constant
            
            transfer_torque = math.copysign(1.0, self.converter_slip_rpm) * (self.converter_slip_rpm ** 2) * k_converter # Torque transfer
            max_transfer = self._get_torque_curve(self.rpm) * 2.5 # Max torque limit
            load_torque = max(-max_transfer, min(max_transfer, transfer_torque)) # Clamp load torque
            
            drive_force = (load_torque * total_ratio) / self.tire_radius # Calculate wheel force
            
            self._calculate_engine_kinetics(dt, load_torque) # Update engine state with load
            
            if self.rpm < self.idle_rpm: # Idle control
                self.rpm += (self.idle_rpm - self.rpm) * 2.0 * dt # P-Controller for idle
        
        self._calculate_chassis_kinetics(dt, drive_force) # Update vehicle movement
        
        if self.rpm > self.shift_point_up and self.gear < 5: # Auto upshift logic
            self.gear += 1 # Increment gear
        elif self.rpm < self.shift_point_down and self.gear > 1: # Auto downshift logic
            self.gear -= 1 # Decrement gear
            self.rpm += 500 # Rev match bump
            
        self._update_thermodynamics(dt) # Update temps
        self._calculate_fuel(dt) # Update fuel
        
        speed_kmh = self.speed_mps * 3.6 # Get speed
        fuel_100km = (self.current_fuel_rate_l_h / speed_kmh * 100.0) if speed_kmh > 1 else 0.0 # Calc L/100km
        
        return { # Return current state dict
            "rpm": int(self.rpm), # Engine RPM
            "speed_kmh": int(speed_kmh), # Speed in km/h
            "gear": self.gear, # Current Gear
            "engine_temp": round(self.temp_coolant, 1), # Engine Temp
            "oil_temp": round(self.temp_oil, 1), # Oil Temp
            "oil_pressure": round(self.oil_pressure_bar, 2), # Oil Pressure
            "trans_temp": round(self.temp_trans, 1), # Trans Temp
            "fuel_ltr": round(self.fuel_liters, 2), # Fuel Level
            "battery_pct": round(self.battery_lvl, 1), # Battery Level
            "fuel_usage_l_100km": round(min(99.9, fuel_100km), 1), # Fuel Econ
            "range_km": int(self.range_km), # Range
            "odometer_km": round(self.odometer_km, 1), # Odometer
            "afr": round(self.current_afr, 1), # AFR
            "power_hp": int(self.power_hp), # Power
            "torque_nm": int(self.torque_net_nm), # Torque
            "accel_g": round(self.accel_g, 2), # Acceleration
            "timer_0_100": round(self.timer_0_100, 1), # 0-100 Time
            "best_0_100": round(self.best_0_100, 2), # Best 0-100
            "iat_temp": round(self.temp_intake, 1), # IAT
            "ve_pct": int(self.volumetric_efficiency * 100), # VE
            "slip_rpm": int(self.converter_slip_rpm), # TCC Slip
            "lockup": self.lockup_active # Lockup Status
        } # End of return dict