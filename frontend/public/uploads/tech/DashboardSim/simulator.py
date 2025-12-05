import time
import math

class Simulator:
    def __init__(self):
        # --- Inputs ---
        self.throttle = 0.0
        self.brake = 0.0
        self.prev_throttle = 0.0

        # --- State Variables ---
        self.speed_mps = 0.0
        self.rpm = 800.0
        self.gear = 1
        self.mode = 'DRIVE'
        
        # --- Consumables ---
        self.fuel_liters = 90.0
        self.battery_lvl = 100.0
        
        # --- Trip & Efficiency Data ---
        self.odometer_km = 0.0
        self.current_fuel_rate_l_h = 0.0
        self.avg_fuel_consumption = 15.0
        self.current_afr = 14.7
        self.range_km = 0.0
        
        # --- Performance Metrics ---
        self.torque_net_nm = 0.0
        self.power_hp = 0.0
        self.accel_g = 0.0
        self.timer_0_100 = 0.0
        self.best_0_100 = 0.0
        self.is_doing_0_100 = False
        
        # --- Advanced Thermodynamics State (Celsius) ---
        self.temp_coolant = 20.0
        self.temp_oil = 20.0
        self.temp_trans = 20.0
        self.temp_block = 20.0
        self.temp_cabin = 20.0
        self.temp_ambient = 15.0
        self.temp_intake = 15.0

        # --- Mechanics Constants (2005 VW Phaeton W12 LWB) ---
        self.mass_kg = 2450.0
        self.drag_coeff = 0.32
        self.frontal_area = 2.40
        self.tire_radius = 0.35
        self.tire_circumference = 2.0 * math.pi * self.tire_radius
        self.rolling_resistance_c = 0.012
        
        # --- Engine Constants ---
        self.displacement = 6.0
        self.idle_rpm = 600.0
        self.redline_rpm = 6200.0
        # INCREASED INERTIA: W12 Crank + Flywheel + Converter fluid mass is heavy.
        # This prevents the "wonky" oscillation at low gears.
        self.inertia_engine = 0.65 
        
        # --- Transmission Constants (ZF 5HP24A) ---
        self.gear_ratios = {1: 3.57, 2: 2.20, 3: 1.51, 4: 1.00, 5: 0.80}
        self.final_drive = 3.07
        self.shift_point_up = 5900
        self.shift_point_down = 1100
        self.lockup_active = False
        self.converter_slip_rpm = 0.0
        self.volumetric_efficiency = 0.0

    def set_inputs(self, throttle, brake):
        self.prev_throttle = self.throttle
        self.throttle = max(0.0, min(1.0, throttle))
        self.brake = max(0.0, min(1.0, brake))

    # =========================================================================
    # CORE PHYSICS MODULES
    # =========================================================================

    def _get_air_density(self):
        temp_kelvin = self.temp_intake + 273.15
        return 1.225 * (288.15 / temp_kelvin)

    def _get_torque_curve(self, rpm):
        if rpm < 600: return 200
        if rpm < 2750:
            factor = (rpm - 600) / (2750 - 600)
            return 300 + (260 * factor)
        elif rpm <= 5200:
            return 560
        elif rpm <= 6500:
            factor = (rpm - 5200) / (6500 - 5200)
            return 560 - (100 * factor)
        return 0

    def _get_volumetric_efficiency(self, rpm, throttle):
        ve_rpm = 0.85 + 0.15 * (1 - ((rpm - 4000)/3500)**2)
        ve_load = 0.15 + (0.85 * throttle)
        return max(0.1, ve_rpm * ve_load)

    # =========================================================================
    # DYNAMICS LOOPS
    # =========================================================================

    def _calculate_engine_kinetics(self, dt, load_torque_nm):
        # 1. Combustion Torque
        max_torque = self._get_torque_curve(self.rpm)
        actual_torque = max_torque * self.throttle
        
        # 2. Friction
        friction_torque = 20.0 + (self.rpm / 6000.0)**2 * 60.0
        if self.throttle < 0.05:
            vacuum_drag = (self.rpm / 3000.0) * 40.0
            friction_torque += vacuum_drag

        # 3. Net Torque & RPM
        self.torque_net_nm = actual_torque - friction_torque - load_torque_nm
        
        alpha = self.torque_net_nm / self.inertia_engine
        rpm_change = (alpha * dt) * (60.0 / (2.0 * math.pi))
        
        self.rpm += rpm_change
        self.rpm = max(0, min(self.rpm, self.redline_rpm + 200))
        
        self.power_hp = (actual_torque * self.rpm) / 7120.0

    def _calculate_chassis_kinetics(self, dt, drive_force_n):
        rho = self._get_air_density()
        f_aero = 0.5 * rho * self.drag_coeff * self.frontal_area * (self.speed_mps ** 2)
        f_roll = self.rolling_resistance_c * self.mass_kg * 9.81
        f_brake = self.brake * 18000.0
        f_mech = self.speed_mps * 10.0
        
        f_net = drive_force_n - f_aero - f_roll - f_brake - f_mech
        
        if self.speed_mps <= 0.01 and f_net < 0:
            f_net = 0
            self.speed_mps = 0
            
        accel = f_net / self.mass_kg
        self.speed_mps += accel * dt
        if self.speed_mps < 0: self.speed_mps = 0
        
        self.accel_g = accel / 9.81
        dist_km = (self.speed_mps * dt) / 1000.0
        self.odometer_km += dist_km
        
        # 0-100 Logic
        speed_kmh = self.speed_mps * 3.6
        if speed_kmh < 1.0:
            self.is_doing_0_100 = False
            self.timer_0_100 = 0.0
        elif speed_kmh > 1.0 and speed_kmh < 100.0:
            if not self.is_doing_0_100 and self.accel_g > 0.1:
                self.is_doing_0_100 = True
            if self.is_doing_0_100:
                self.timer_0_100 += dt
        elif speed_kmh >= 100.0 and self.is_doing_0_100:
            self.best_0_100 = self.timer_0_100
            self.is_doing_0_100 = False

    def _update_thermodynamics(self, dt):
        c_iron = 450; m_block = 200.0 
        c_water = 4184; m_coolant = 15.0
        c_oil = 1800; m_oil = 12.0
        c_atf = 2000; m_atf = 10.0
        
        heat_in_watts = self.current_fuel_rate_l_h * 150 
        
        k_block_coolant = 50.0 + (self.rpm / 6000.0) * 300.0
        q_block_coolant = k_block_coolant * (self.temp_block - self.temp_coolant)
        
        k_block_oil = 20.0 + (self.rpm / 6000.0) * 80.0
        q_block_oil = k_block_oil * (self.temp_block - self.temp_oil)
        
        airflow = 5.0 + (self.speed_mps * 2.0)
        thermostat = max(0.05, min(1.0, (self.temp_coolant - 82) / 10.0))
        k_radiator = thermostat * airflow * 50.0
        q_coolant_air = k_radiator * (self.temp_coolant - self.temp_ambient)
        
        q_oil_cooler = 15.0 * (self.temp_oil - self.temp_coolant)
        
        slip_rad_s = (self.converter_slip_rpm * 2 * math.pi) / 60.0
        q_trans_slip = abs(self.torque_net_nm * slip_rad_s) * 0.5
        q_trans_cool = 20.0 * (self.temp_trans - self.temp_ambient) * (1 + self.speed_mps/10)
        
        target_iat = self.temp_ambient + (self.temp_block - self.temp_ambient) * 0.15
        cooling_iat = (self.speed_mps + 1.0) * 0.1
        self.temp_intake += (target_iat - self.temp_intake - cooling_iat) * 0.1 * dt
        self.temp_intake = max(self.temp_ambient, self.temp_intake)

        self.temp_block += ((heat_in_watts - q_block_coolant - q_block_oil) / (m_block * c_iron)) * dt
        self.temp_coolant += ((q_block_coolant + q_oil_cooler - q_coolant_air) / (m_coolant * c_water)) * dt
        self.temp_oil += ((q_block_oil - q_oil_cooler) / (m_oil * c_oil)) * dt
        self.temp_trans += ((q_trans_slip - q_trans_cool) / (m_atf * c_atf)) * dt

        viscosity = 100 * math.exp(-0.03 * (self.temp_oil - 20))
        raw_pressure = (self.rpm * 0.002) * (viscosity * 0.05)
        self.oil_pressure_bar = min(7.0, max(0.5, raw_pressure)) if self.rpm > 300 else 0
        self.temp_cabin += (22.0 - self.temp_cabin) * 0.05 * dt

    def _calculate_fuel(self, dt):
        rho_air = self._get_air_density()
        self.volumetric_efficiency = self._get_volumetric_efficiency(self.rpm, self.throttle)
        
        intake_flow_l_s = (self.rpm / 120.0) * self.displacement * self.volumetric_efficiency
        air_mass_s = (intake_flow_l_s / 1000.0) * rho_air
        
        self.current_afr = 14.7
        if self.throttle > 0.7: self.current_afr = 12.5
        
        if self.throttle < 0.01 and self.rpm > 1200:
            fuel_mass_s = 0.0
            self.current_afr = 99.9
        else:
            fuel_mass_s = air_mass_s / self.current_afr
            
        if (self.throttle - self.prev_throttle) > 0.1:
            fuel_mass_s *= 1.5
            
        fuel_l_s = fuel_mass_s / 0.74
        self.current_fuel_rate_l_h = fuel_l_s * 3600.0
        self.fuel_liters = max(0, self.fuel_liters - (fuel_l_s * dt))
        
        speed_kmh = self.speed_mps * 3.6
        if speed_kmh > 10 and fuel_l_s > 0:
            current_l_100 = (self.current_fuel_rate_l_h / speed_kmh) * 100.0
            self.avg_fuel_consumption = (self.avg_fuel_consumption * 0.995) + (current_l_100 * 0.005)
            
        if self.avg_fuel_consumption > 0.1:
            self.range_km = (self.fuel_liters / self.avg_fuel_consumption) * 100.0
        else:
            self.range_km = 999.0
            
        draw = 0.02 * dt
        gen = 0.06 * dt if self.rpm > 800 else 0
        self.battery_lvl = min(100, max(0, self.battery_lvl - draw + gen))

    # =========================================================================
    # MAIN LOOP
    # =========================================================================

    def update(self, dt):
        total_ratio = self.gear_ratios[self.gear] * self.final_drive
        trans_out_rpm = (self.speed_mps / self.tire_circumference) * 60.0 * total_ratio
        
        # Torque Converter Physics
        self.lockup_active = (self.gear >= 3 and self.speed_mps > 15)
        
        if self.lockup_active:
            # Locked
            target_rpm = max(self.idle_rpm, trans_out_rpm)
            self.rpm = target_rpm
            self.converter_slip_rpm = 0.0
            
            eng_torque = self._get_torque_curve(self.rpm) * self.throttle
            if self.throttle < 0.01: eng_torque = -40.0 - (self.rpm/100)
            drive_force = (eng_torque * total_ratio) / self.tire_radius
            
            self._calculate_engine_kinetics(dt, 0)
            
        else:
            # Slipping
            self.converter_slip_rpm = self.rpm - trans_out_rpm
            
            # Slightly softer coupling to prevent oscillation
            k_converter = 0.0045 
            
            transfer_torque = math.copysign(1.0, self.converter_slip_rpm) * (self.converter_slip_rpm ** 2) * k_converter
            max_transfer = self._get_torque_curve(self.rpm) * 2.5
            load_torque = max(-max_transfer, min(max_transfer, transfer_torque))
            
            drive_force = (load_torque * total_ratio) / self.tire_radius
            
            self._calculate_engine_kinetics(dt, load_torque)
            
            # Idle Governor (Smoother P-Control)
            if self.rpm < self.idle_rpm:
                self.rpm += (self.idle_rpm - self.rpm) * 2.0 * dt

        self._calculate_chassis_kinetics(dt, drive_force)
        
        if self.rpm > self.shift_point_up and self.gear < 5:
            self.gear += 1
        elif self.rpm < self.shift_point_down and self.gear > 1:
            self.gear -= 1
            self.rpm += 500
            
        self._update_thermodynamics(dt)
        self._calculate_fuel(dt)
        
        speed_kmh = self.speed_mps * 3.6
        fuel_100km = (self.current_fuel_rate_l_h / speed_kmh * 100.0) if speed_kmh > 1 else 0.0

        return {
            "rpm": int(self.rpm),
            "speed_kmh": int(speed_kmh),
            "gear": self.gear,
            "engine_temp": round(self.temp_coolant, 1),
            "oil_temp": round(self.temp_oil, 1),
            "oil_pressure": round(self.oil_pressure_bar, 2),
            "trans_temp": round(self.temp_trans, 1),
            "fuel_ltr": round(self.fuel_liters, 2),
            "battery_pct": round(self.battery_lvl, 1),
            "fuel_usage_l_100km": round(min(99.9, fuel_100km), 1),
            "range_km": int(self.range_km),
            "odometer_km": round(self.odometer_km, 1),
            "afr": round(self.current_afr, 1),
            "power_hp": int(self.power_hp),
            "torque_nm": int(self.torque_net_nm),
            "accel_g": round(self.accel_g, 2),
            "timer_0_100": round(self.timer_0_100, 1),
            "best_0_100": round(self.best_0_100, 2),
            "iat_temp": round(self.temp_intake, 1),
            "ve_pct": int(self.volumetric_efficiency * 100),
            "slip_rpm": int(self.converter_slip_rpm),
            "lockup": self.lockup_active
        }