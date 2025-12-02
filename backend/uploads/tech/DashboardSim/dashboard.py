import tkinter as tk
import math
import time
from simulator import Simulator

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard Simulator")
        self.root.geometry("1280x720") # HD Resolution
        self.root.configure(bg="#2a2a2a")

        # Initialize Simulator
        self.sim = Simulator()
        self.last_time = time.time()
        self.last_screen_update = time.time() # Timer for the center screen
        
        # --- MFD (Multi-Function Display) State ---
        self.page_index = 0
        self.pages = ["MAIN", "TRIP", "PERFORMANCE", "DIAGNOSTICS"]
        
        # --- Needle Smoothing State ---
        self.needle_values = {
            'rpm': 0.8, 'speed': 0.0, 'oil': 15.0, 
            'coolant': 20.0, 'fuel': 1.0, 'batt': 12.0
        }

        # Canvas Setup
        self.canvas = tk.Canvas(root, width=1280, height=550, bg="#2a2a2a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Pedal UI
        self.pedal_frame = tk.Frame(root, bg="#151515", height=170)
        self.pedal_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Container for centering pedals
        self.pedal_container = tk.Frame(self.pedal_frame, bg="#151515")
        self.pedal_container.pack(side=tk.TOP, pady=15)
        
        # --- Pedal Controls ---
        self.brake_canvas = tk.Canvas(self.pedal_container, width=120, height=140, bg="#151515", highlightthickness=0)
        self.brake_canvas.pack(side=tk.LEFT, padx=20)
        self.draw_pedal(self.brake_canvas, "BRAKE\n(Down Arrow)", "#882222")
        self.brake_mouse_active = False

        self.gas_canvas = tk.Canvas(self.pedal_container, width=100, height=140, bg="#151515", highlightthickness=0)
        self.gas_canvas.pack(side=tk.LEFT, padx=20)
        self.draw_pedal(self.gas_canvas, "GAS\n(Up Arrow)", "#228822")
        self.gas_mouse_active = False

        # --- Input State ---
        self.key_gas = False
        self.key_brake = False

        # Bindings
        self.brake_canvas.bind("<ButtonPress-1>", lambda e: self.set_mouse_pedal('brake', True))
        self.brake_canvas.bind("<ButtonRelease-1>", lambda e: self.set_mouse_pedal('brake', False))
        self.gas_canvas.bind("<ButtonPress-1>", lambda e: self.set_mouse_pedal('gas', True))
        self.gas_canvas.bind("<ButtonRelease-1>", lambda e: self.set_mouse_pedal('gas', False))

        self.root.bind("<KeyPress-Up>", lambda e: self.set_key_pedal('gas', True))
        self.root.bind("<KeyRelease-Up>", lambda e: self.set_key_pedal('gas', False))
        self.root.bind("<KeyPress-Down>", lambda e: self.set_key_pedal('brake', True))
        self.root.bind("<KeyRelease-Down>", lambda e: self.set_key_pedal('brake', False))
        
        self.root.bind("<space>", self.toggle_page)
        self.root.focus_force()

        self.update_loop()

    def toggle_page(self, event):
        self.page_index = (self.page_index + 1) % len(self.pages)

    def set_mouse_pedal(self, pedal, state):
        if pedal == 'brake': self.brake_mouse_active = state
        elif pedal == 'gas': self.gas_mouse_active = state
        self.update_pedal_visuals()

    def set_key_pedal(self, pedal, state):
        if pedal == 'brake': self.key_brake = state
        elif pedal == 'gas': self.key_gas = state
        self.update_pedal_visuals()

    def update_pedal_visuals(self):
        is_brake = self.brake_mouse_active or self.key_brake
        color_b = "#ff4444" if is_brake else "#882222"
        self.draw_pedal(self.brake_canvas, "BRAKE\n(Down Arrow)", color_b)

        is_gas = self.gas_mouse_active or self.key_gas
        color_g = "#44ff44" if is_gas else "#228822"
        self.draw_pedal(self.gas_canvas, "GAS\n(Up Arrow)", color_g)

    def draw_pedal(self, canvas, text, color):
        canvas.delete("all")
        w = int(canvas.cget("width"))
        h = int(canvas.cget("height"))
        canvas.create_rectangle(5, 5, w-5, h-5, fill=color, outline="#aaaaaa", width=2)
        canvas.create_text(w/2, h/2, text=text, fill="white", font=("Arial", 10, "bold"), justify=tk.CENTER)

    # --- Icon Drawing Methods ---
    def draw_oil_icon(self, x, y, size=24, color="#888"):
        self.canvas.create_polygon(x-size/2, y+size/2, x+size/2, y+size/2, x+size/2, y-size/4, x-size/2, y-size/4, fill=color, outline=color)
        self.canvas.create_line(x+size/2, y-size/5, x+size, y-size/2, width=2, fill=color)
        self.canvas.create_line(x-size/2, y, x-size, y-size/2, x-size/2, y-size/4, width=2, fill=color)
        self.canvas.create_oval(x+size, y-size/2, x+size+4, y-size/2+4, fill=color, outline="")

    def draw_temp_icon(self, x, y, size=24, color="#888"):
        self.canvas.create_line(x, y-size/2, x, y+size/4, width=5, fill=color, capstyle=tk.ROUND)
        self.canvas.create_oval(x-5, y+size/4-5, x+5, y+size/4+5, fill=color, outline="")
        self.canvas.create_line(x+5, y-6, x+10, y-6, fill=color, width=2)
        self.canvas.create_line(x+5, y+2, x+10, y+2, fill=color, width=2)

    def draw_fuel_icon(self, x, y, size=24, color="#888"):
        self.canvas.create_rectangle(x-6, y-10, x+6, y+10, outline=color, width=2)
        self.canvas.create_rectangle(x-4, y-8, x+4, y-3, fill=color, outline="")
        self.canvas.create_line(x+6, y, x+10, y, x+10, y+12, x-10, y+12, x-10, y-10, width=2, fill=color)
        self.canvas.create_line(x-10, y-10, x-6, y-10, width=2, fill=color)

    def draw_battery_icon(self, x, y, size=24, color="#888"):
        self.canvas.create_rectangle(x-10, y-6, x+10, y+6, outline=color, width=2)
        self.canvas.create_rectangle(x-5, y-9, x-3, y-6, fill=color, outline="")
        self.canvas.create_rectangle(x+3, y-9, x+5, y-6, fill=color, outline="")
        self.canvas.create_text(x-6, y, text="-", fill=color, font=("Arial", 10, "bold"))
        self.canvas.create_text(x+6, y, text="+", fill=color, font=("Arial", 8, "bold"))

    def draw_gauge_background(self, x, y, r, min_val, max_val, title, major_ticks, unit="", icon_type=None):
        self.canvas.create_oval(x-r-2, y-r-2, x+r+2, y+r+2, outline="#888888", width=3)
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="#555555", width=5)
        self.canvas.create_oval(x-r+5, y-r+5, x+r-5, y+r-5, fill="#050505", outline="")
        
        for i in range(major_ticks + 1):
            val = min_val + (max_val - min_val) * (i / major_ticks)
            sim_angle = 225 - (270 * (i / major_ticks))
            rad = math.radians(sim_angle)
            
            tick_r_out = r - 10
            tick_r_in = r - 25
            
            tx1 = x + tick_r_in * math.cos(rad)
            ty1 = y - tick_r_in * math.sin(rad)
            tx2 = x + tick_r_out * math.cos(rad)
            ty2 = y - tick_r_out * math.sin(rad)
            
            self.canvas.create_line(tx1, ty1, tx2, ty2, fill="white", width=2)
            
            text_r = r - 40
            tx = x + text_r * math.cos(rad)
            ty = y - text_r * math.sin(rad)
            font_size = 10 if r > 80 else 8
            self.canvas.create_text(tx, ty, text=str(int(val)), fill="white", font=("Arial", font_size))

        if icon_type:
            if icon_type == "oil": self.draw_oil_icon(x, y - r/2.5)
            elif icon_type == "temp": self.draw_temp_icon(x, y - r/2.5)
            elif icon_type == "fuel": self.draw_fuel_icon(x, y - r/2.5)
            elif icon_type == "batt": self.draw_battery_icon(x, y - r/2.5)
        else:
            self.canvas.create_text(x, y + r/2 + 5, text=title, fill="#aaaaaa", font=("Arial", 12, "bold"))
            self.canvas.create_text(x, y + r/2 + 25, text=unit, fill="#888888", font=("Arial", 10))

    def update_needle(self, tag, x, y, r, val, min_val, max_val):
        self.canvas.delete(tag)
        val = max(min_val, min(max_val, val))
        pct = (val - min_val) / (max_val - min_val)
        angle_deg = 225 - (270 * pct)
        rad = math.radians(angle_deg)
        
        tip_r = r - 15
        tx = x + tip_r * math.cos(rad)
        ty = y - tip_r * math.sin(rad)
        
        self.canvas.create_line(x, y, tx, ty, fill="#ff2222", width=4, tags=tag, capstyle=tk.ROUND)
        self.canvas.create_oval(x-7, y-7, x+7, y+7, fill="#111", outline="#555", tags=tag)

    def draw_center_screen_static(self):
        # 200px wide screen
        x1, y1 = 540, 150
        x2, y2 = 740, 350
        
        self.canvas.create_rectangle(x1-4, y1-4, x2+4, y2+4, outline="#444", width=3)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="")
        
        self.canvas.create_text(640, y1+20, text="PRNDS", fill="#555", font=("Courier", 12, "bold"))
        self.canvas.create_line(x1+10, y1+35, x2-10, y1+35, fill="#333")
        self.canvas.create_text(640, y2+15, text="[SPACE] Change Page", fill="#555", font=("Arial", 8))

    def update_center_screen(self, stats):
        self.canvas.delete("screen_data")
        
        page = self.pages[self.page_index]
        self.canvas.create_text(640, 150 + 45, text=f"- {page} -", fill="#888", font=("Arial", 9, "bold"), tags="screen_data")

        if page == "MAIN":
            self.canvas.create_text(640, 230, text=str(stats['gear']), fill="orange", font=("Courier", 45, "bold"), tags="screen_data")
            self.canvas.create_text(640, 205, text="GEAR", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(640, 280, text=f"{stats['speed_kmh']}", fill="white", font=("Courier", 26, "bold"), tags="screen_data")
            self.canvas.create_text(640, 300, text="km/h", fill="#aaa", font=("Arial", 8), tags="screen_data")
            cons = f"{stats['fuel_usage_l_100km']} L/100" if stats['speed_kmh'] > 5 else "--.- L/100"
            self.canvas.create_text(640, 330, text=cons, fill="#aaa", font=("Courier", 10), tags="screen_data")

        elif page == "TRIP":
            self.canvas.create_text(640, 215, text="RANGE", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(640, 230, text=f"{stats['range_km']} km", fill="#4f4", font=("Courier", 16, "bold"), tags="screen_data")
            self.canvas.create_text(640, 260, text="ODOMETER", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(640, 275, text=f"{int(stats['odometer_km'])} km", fill="white", font=("Courier", 12), tags="screen_data")
            self.canvas.create_text(640, 305, text="AFR", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(640, 320, text=f"{stats['afr']}:1", fill="cyan", font=("Courier", 12), tags="screen_data")

        elif page == "PERFORMANCE":
            self.canvas.create_text(600, 220, text="HP", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(600, 235, text=f"{stats['power_hp']}", fill="orange", font=("Courier", 14, "bold"), tags="screen_data")
            self.canvas.create_text(680, 220, text="TRQ", fill="#555", font=("Arial", 8), tags="screen_data")
            self.canvas.create_text(680, 235, text=f"{stats['torque_nm']}", fill="orange", font=("Courier", 14, "bold"), tags="screen_data")
            self.canvas.create_text(640, 265, text=f"G-FORCE: {stats['accel_g']} G", fill="white", font=("Courier", 12), tags="screen_data")
            self.canvas.create_text(640, 300, text="0-100 km/h", fill="#555", font=("Arial", 8), tags="screen_data")
            timer_col = "red" if stats['timer_0_100'] > 0 else "#444"
            if stats['best_0_100'] > 0: timer_col = "#4f4"
            disp_time = stats['timer_0_100'] if stats['timer_0_100'] > 0 else stats['best_0_100']
            self.canvas.create_text(640, 315, text=f"{disp_time} s", fill=timer_col, font=("Courier", 14, "bold"), tags="screen_data")

        elif page == "DIAGNOSTICS":
            self.canvas.create_text(590, 220, text="TRANS TEMP", fill="#555", font=("Arial", 7), tags="screen_data")
            self.canvas.create_text(590, 235, text=f"{stats['trans_temp']}°C", fill="white", font=("Courier", 11), tags="screen_data")
            self.canvas.create_text(690, 220, text="INTAKE AIR", fill="#555", font=("Arial", 7), tags="screen_data")
            self.canvas.create_text(690, 235, text=f"{stats['iat_temp']}°C", fill="white", font=("Courier", 11), tags="screen_data")
            self.canvas.create_text(590, 270, text="CONV. SLIP", fill="#555", font=("Arial", 7), tags="screen_data")
            self.canvas.create_text(590, 285, text=f"{stats['slip_rpm']}", fill="orange", font=("Courier", 11), tags="screen_data")
            self.canvas.create_text(690, 270, text="LOCKUP", fill="#555", font=("Arial", 7), tags="screen_data")
            status = "CLOSED" if stats['lockup'] else "OPEN"
            col = "#4f4" if stats['lockup'] else "#f44"
            self.canvas.create_text(690, 285, text=status, fill=col, font=("Courier", 10, "bold"), tags="screen_data")
            self.canvas.create_text(640, 315, text=f"OIL P: {stats['oil_pressure']} bar", fill="#aaa", font=("Courier", 10), tags="screen_data")

    def smooth_value(self, key, target, max_change_rate, dt):
        current = self.needle_values.get(key, target)
        diff = target - current
        max_step = max_change_rate * dt
        if abs(diff) <= max_step: self.needle_values[key] = target
        else: self.needle_values[key] += math.copysign(max_step, diff)
        return self.needle_values[key]

    def update_loop(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        throttle_input = 1.0 if (self.gas_mouse_active or self.key_gas) else 0.0
        brake_input = 1.0 if (self.brake_mouse_active or self.key_brake) else 0.0
        
        self.sim.set_inputs(throttle_input, brake_input)
        stats = self.sim.update(dt)
        
        if not hasattr(self, 'gauges_initialized'):
            self.canvas.delete("all")
            self.draw_gauge_background(360, 280, 140, 0, 8, "x1000", 8, unit="RPM")
            self.draw_gauge_background(920, 280, 140, 0, 320, "km/h", 8)
            self.draw_gauge_background(140, 360, 75, 50, 150, "OIL", 2, unit="°C", icon_type="oil")
            self.draw_gauge_background(1140, 360, 75, 8, 16, "BATT", 2, unit="V", icon_type="batt")
            self.draw_gauge_background(570, 430, 45, 50, 130, "ENGINE", 2, icon_type="temp")
            self.draw_gauge_background(710, 430, 45, 0, 1, "FUEL", 2, icon_type="fuel")
            self.draw_center_screen_static()
            self.gauges_initialized = True

        # Needles Smooth Logic
        val_rpm = self.smooth_value('rpm', stats['rpm']/1000, 8.0, dt)
        val_speed = self.smooth_value('speed', stats['speed_kmh'], 160.0, dt)
        val_oil = self.smooth_value('oil', stats['oil_temp'], 10.0, dt)
        val_coolant = self.smooth_value('coolant', stats['engine_temp'], 10.0, dt)
        val_fuel = self.smooth_value('fuel', stats['fuel_ltr']/90.0, 0.05, dt)
        target_volts = 11.5 + (stats['battery_pct']/100 * 3.0)
        val_batt = self.smooth_value('batt', target_volts, 2.0, dt)

        self.update_needle("needle_rpm", 360, 280, 140, val_rpm, 0, 8)
        self.update_needle("needle_speed", 920, 280, 140, val_speed, 0, 320)
        self.update_needle("needle_oil", 140, 360, 75, val_oil, 50, 150)
        self.update_needle("needle_batt", 1140, 360, 75, val_batt, 8, 16)
        self.update_needle("needle_coolant", 570, 430, 45, val_coolant, 50, 130)
        self.update_needle("needle_fuel", 710, 430, 45, val_fuel, 0, 1)

        # Update center screen only 4 times per second (every 0.25s)
        if current_time - self.last_screen_update >= 0.25:
             self.update_center_screen(stats)
             self.last_screen_update = current_time

        self.root.after(30, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()