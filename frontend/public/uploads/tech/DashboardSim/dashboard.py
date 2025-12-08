import tkinter as tk # Import the tkinter library for creating the GUI
import math # Import the math library for trigonometric functions
import time # Import the time library for handling simulation timing
from simulator import Simulator # Import the Simulator class from the simulator module

class DashboardApp: # Define the main Dashboard Application class
    def __init__(self, root): # Constructor to initialize the dashboard
        self.root = root # Save the root window object
        self.root.title("Dashboard Simulator") # Set the window title
        self.root.geometry("1280x720") # Set the window resolution to 1280x720
        self.root.configure(bg="#2a2a2a") # Set the background color to dark gray

        self.sim = Simulator() # Create an instance of the Simulator
        self.last_time = time.time() # Initialize the time tracker with current time
        self.last_screen_update = time.time() # Initialize the screen update timer
        
        self.page_index = 0 # Initialize the page index for the center display
        self.pages = ["MAIN", "TRIP", "PERFORMANCE", "DIAGNOSTICS"] # Define the available display pages
        
        self.needle_values = { # Initialize the gauge smoothing dictionary
            'rpm': 0.8, 'speed': 0.0, 'oil': 15.0, # Initial values for RPM, speed, oil
            'coolant': 20.0, 'fuel': 1.0, 'batt': 12.0 # Initial values for coolant, fuel, battery
        }

        self.canvas = tk.Canvas(root, width=1280, height=550, bg="#2a2a2a", highlightthickness=0) # Create the main drawing canvas
        self.canvas.pack(fill=tk.BOTH, expand=True) # Pack the canvas to fill the window

        self.pedal_frame = tk.Frame(root, bg="#151515", height=170) # Create a frame for the pedals
        self.pedal_frame.pack(fill=tk.X, side=tk.BOTTOM) # Pack the frame at the bottom

        self.pedal_container = tk.Frame(self.pedal_frame, bg="#151515") # Create a container to center the pedals
        self.pedal_container.pack(side=tk.TOP, pady=15) # Pack the container with padding
        
        self.brake_canvas = tk.Canvas(self.pedal_container, width=120, height=140, bg="#151515", highlightthickness=0) # Create canvas for brake pedal
        self.brake_canvas.pack(side=tk.LEFT, padx=20) # Pack brake pedal to the left
        self.draw_pedal(self.brake_canvas, "BRAKE\n(Down Arrow)", "#882222") # Draw the initial brake pedal state
        self.brake_mouse_active = False # Initialize brake mouse interaction state

        self.gas_canvas = tk.Canvas(self.pedal_container, width=100, height=140, bg="#151515", highlightthickness=0) # Create canvas for gas pedal
        self.gas_canvas.pack(side=tk.LEFT, padx=20) # Pack gas pedal to the left
        self.draw_pedal(self.gas_canvas, "GAS\n(Up Arrow)", "#228822") # Draw the initial gas pedal state
        self.gas_mouse_active = False # Initialize gas mouse interaction state

        self.key_gas = False # Initialize keyboard gas input state
        self.key_brake = False # Initialize keyboard brake input state

        self.brake_canvas.bind("<ButtonPress-1>", lambda e: self.set_mouse_pedal('brake', True)) # Bind mouse press to brake
        self.brake_canvas.bind("<ButtonRelease-1>", lambda e: self.set_mouse_pedal('brake', False)) # Bind mouse release to brake
        self.gas_canvas.bind("<ButtonPress-1>", lambda e: self.set_mouse_pedal('gas', True)) # Bind mouse press to gas
        self.gas_canvas.bind("<ButtonRelease-1>", lambda e: self.set_mouse_pedal('gas', False)) # Bind mouse release to gas

        self.root.bind("<KeyPress-Up>", lambda e: self.set_key_pedal('gas', True)) # Bind Up arrow press to gas
        self.root.bind("<KeyRelease-Up>", lambda e: self.set_key_pedal('gas', False)) # Bind Up arrow release to gas
        self.root.bind("<KeyPress-Down>", lambda e: self.set_key_pedal('brake', True)) # Bind Down arrow press to brake
        self.root.bind("<KeyRelease-Down>", lambda e: self.set_key_pedal('brake', False)) # Bind Down arrow release to brake
        
        self.root.bind("<space>", self.toggle_page) # Bind Spacebar to page toggle
        self.root.focus_force() # Force focus on the main window

        self.update_loop() # Start the main update loop

    def toggle_page(self, event): # Method to cycle through display pages
        self.page_index = (self.page_index + 1) % len(self.pages) # Increment and wrap page index

    def set_mouse_pedal(self, pedal, state): # Method to handle mouse pedal input
        if pedal == 'brake': self.brake_mouse_active = state # Update brake state
        elif pedal == 'gas': self.gas_mouse_active = state # Update gas state
        self.update_pedal_visuals() # Redraw pedals

    def set_key_pedal(self, pedal, state): # Method to handle keyboard pedal input
        if pedal == 'brake': self.key_brake = state # Update brake key state
        elif pedal == 'gas': self.key_gas = state # Update gas key state
        self.update_pedal_visuals() # Redraw pedals

    def update_pedal_visuals(self): # Method to update pedal colors based on state
        is_brake = self.brake_mouse_active or self.key_brake # Check if brake is active
        color_b = "#ff4444" if is_brake else "#882222" # Determine brake color (bright if active)
        self.draw_pedal(self.brake_canvas, "BRAKE\n(Down Arrow)", color_b) # Redraw brake pedal

        is_gas = self.gas_mouse_active or self.key_gas # Check if gas is active
        color_g = "#44ff44" if is_gas else "#228822" # Determine gas color (bright if active)
        self.draw_pedal(self.gas_canvas, "GAS\n(Up Arrow)", color_g) # Redraw gas pedal

    def draw_pedal(self, canvas, text, color): # Method to draw a pedal on a canvas
        canvas.delete("all") # Clear the canvas
        w = int(canvas.cget("width")) # Get canvas width
        h = int(canvas.cget("height")) # Get canvas height
        canvas.create_rectangle(5, 5, w-5, h-5, fill=color, outline="#aaaaaa", width=2) # Draw pedal rectangle
        canvas.create_text(w/2, h/2, text=text, fill="white", font=("Arial", 10, "bold"), justify=tk.CENTER) # Draw pedal text

    def draw_oil_icon(self, x, y, size=24, color="#888"): # Method to draw the oil can icon
        self.canvas.create_polygon(x-size/2, y+size/2, x+size/2, y+size/2, x+size/2, y-size/4, x-size/2, y-size/4, fill=color, outline=color) # Draw base
        self.canvas.create_line(x+size/2, y-size/5, x+size, y-size/2, width=2, fill=color) # Draw spout
        self.canvas.create_line(x-size/2, y, x-size, y-size/2, x-size/2, y-size/4, width=2, fill=color) # Draw handle
        self.canvas.create_oval(x+size, y-size/2, x+size+4, y-size/2+4, fill=color, outline="") # Draw drop

    def draw_temp_icon(self, x, y, size=24, color="#888"): # Method to draw the thermometer icon
        self.canvas.create_line(x, y-size/2, x, y+size/4, width=5, fill=color, capstyle=tk.ROUND) # Draw tube
        self.canvas.create_oval(x-5, y+size/4-5, x+5, y+size/4+5, fill=color, outline="") # Draw bulb
        self.canvas.create_line(x+5, y-6, x+10, y-6, fill=color, width=2) # Draw mark 1
        self.canvas.create_line(x+5, y+2, x+10, y+2, fill=color, width=2) # Draw mark 2

    def draw_fuel_icon(self, x, y, size=24, color="#888"): # Method to draw the fuel pump icon
        self.canvas.create_rectangle(x-6, y-10, x+6, y+10, outline=color, width=2) # Draw pump body
        self.canvas.create_rectangle(x-4, y-8, x+4, y-3, fill=color, outline="") # Draw screen
        self.canvas.create_line(x+6, y, x+10, y, x+10, y+12, x-10, y+12, x-10, y-10, width=2, fill=color) # Draw hose
        self.canvas.create_line(x-10, y-10, x-6, y-10, width=2, fill=color) # Draw nozzle

    def draw_battery_icon(self, x, y, size=24, color="#888"): # Method to draw the battery icon
        self.canvas.create_rectangle(x-10, y-6, x+10, y+6, outline=color, width=2) # Draw battery shape
        self.canvas.create_rectangle(x-5, y-9, x-3, y-6, fill=color, outline="") # Draw negative terminal
        self.canvas.create_rectangle(x+3, y-9, x+5, y-6, fill=color, outline="") # Draw positive terminal
        self.canvas.create_text(x-6, y, text="-", fill=color, font=("Arial", 10, "bold")) # Draw minus sign
        self.canvas.create_text(x+6, y, text="+", fill=color, font=("Arial", 8, "bold")) # Draw plus sign

    def draw_gauge_background(self, x, y, r, min_val, max_val, title, major_ticks, unit="", icon_type=None): # Method to draw gauge background
        self.canvas.create_oval(x-r-2, y-r-2, x+r+2, y+r+2, outline="#888888", width=3) # Draw outer ring
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="#555555", width=5) # Draw inner bezel
        self.canvas.create_oval(x-r+5, y-r+5, x+r-5, y+r-5, fill="#050505", outline="") # Draw face background
        
        for i in range(major_ticks + 1): # specific loop to draw tick marks
            val = min_val + (max_val - min_val) * (i / major_ticks) # Calculate tick value
            sim_angle = 225 - (270 * (i / major_ticks)) # Calculate tick angle
            rad = math.radians(sim_angle) # Convert to radians
            
            tick_r_out = r - 10 # Outer radius of tick
            tick_r_in = r - 25 # Inner radius of tick
            
            tx1 = x + tick_r_in * math.cos(rad) # Calculate x1
            ty1 = y - tick_r_in * math.sin(rad) # Calculate y1
            tx2 = x + tick_r_out * math.cos(rad) # Calculate x2
            ty2 = y - tick_r_out * math.sin(rad) # Calculate y2
            
            self.canvas.create_line(tx1, ty1, tx2, ty2, fill="white", width=2) # Draw tick line
            
            text_r = r - 40 # Radius for text label
            tx = x + text_r * math.cos(rad) # Calculate text x
            ty = y - text_r * math.sin(rad) # Calculate text y
            font_size = 10 if r > 80 else 8 # Determine font size
            self.canvas.create_text(tx, ty, text=str(int(val)), fill="white", font=("Arial", font_size)) # Draw label

        if icon_type: # Draw icon if specified
            if icon_type == "oil": self.draw_oil_icon(x, y - r/2.5) # Draw oil icon
            elif icon_type == "temp": self.draw_temp_icon(x, y - r/2.5) # Draw temp icon
            elif icon_type == "fuel": self.draw_fuel_icon(x, y - r/2.5) # Draw fuel icon
            elif icon_type == "batt": self.draw_battery_icon(x, y - r/2.5) # Draw battery icon
        else: # Draw title text if no icon
            self.canvas.create_text(x, y + r/2 + 5, text=title, fill="#aaaaaa", font=("Arial", 12, "bold")) # Draw title
            self.canvas.create_text(x, y + r/2 + 25, text=unit, fill="#888888", font=("Arial", 10)) # Draw unit

    def update_needle(self, tag, x, y, r, val, min_val, max_val): # Method to update needle position
        self.canvas.delete(tag) # Remove old needle
        val = max(min_val, min(max_val, val)) # Clamp value
        pct = (val - min_val) / (max_val - min_val) # Calculate percentage
        angle_deg = 225 - (270 * pct) # Calculate angle
        rad = math.radians(angle_deg) # Convert to radians
        
        tip_r = r - 15 # Needle tip radius
        tx = x + tip_r * math.cos(rad) # Calculate tip x
        ty = y - tip_r * math.sin(rad) # Calculate tip y
        
        self.canvas.create_line(x, y, tx, ty, fill="#ff2222", width=4, tags=tag, capstyle=tk.ROUND) # Draw new needle
        self.canvas.create_oval(x-7, y-7, x+7, y+7, fill="#111", outline="#555", tags=tag) # Draw needle center cap

    def draw_center_screen_static(self): # Draw static elements of center screen
        x1, y1 = 540, 150 # Top-left coords
        x2, y2 = 740, 350 # Bottom-right coords
        
        self.canvas.create_rectangle(x1-4, y1-4, x2+4, y2+4, outline="#444", width=3) # Draw bezel
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="") # Draw screen area
        
        self.canvas.create_text(640, y1+20, text="PRNDS", fill="#555", font=("Courier", 12, "bold")) # Draw gear indicator static text
        self.canvas.create_line(x1+10, y1+35, x2-10, y1+35, fill="#333") # Draw separator line
        self.canvas.create_text(640, y2+15, text="[SPACE] Change Page", fill="#555", font=("Arial", 8)) # Draw help text

    def update_center_screen(self, stats): # Method to update dynamic center screen content
        self.canvas.delete("screen_data") # Clear old data
        
        page = self.pages[self.page_index] # Get current page
        self.canvas.create_text(640, 150 + 45, text=f"- {page} -", fill="#888", font=("Arial", 9, "bold"), tags="screen_data") # Draw page title

        if page == "MAIN": # Render MAIN page
            self.canvas.create_text(640, 230, text=str(stats['gear']), fill="orange", font=("Courier", 45, "bold"), tags="screen_data") # Show Gear
            self.canvas.create_text(640, 205, text="GEAR", fill="#555", font=("Arial", 8), tags="screen_data") # Label Gear
            self.canvas.create_text(640, 280, text=f"{stats['speed_kmh']}", fill="white", font=("Courier", 26, "bold"), tags="screen_data") # Show Speed
            self.canvas.create_text(640, 300, text="km/h", fill="#aaa", font=("Arial", 8), tags="screen_data") # Label Speed
            cons = f"{stats['fuel_usage_l_100km']} L/100" if stats['speed_kmh'] > 5 else "--.- L/100" # Format consumption
            self.canvas.create_text(640, 330, text=cons, fill="#aaa", font=("Courier", 10), tags="screen_data") # Show consumption

        elif page == "TRIP": # Render TRIP page
            self.canvas.create_text(640, 215, text="RANGE", fill="#555", font=("Arial", 8), tags="screen_data") # Label Range
            self.canvas.create_text(640, 230, text=f"{stats['range_km']} km", fill="#4f4", font=("Courier", 16, "bold"), tags="screen_data") # Show Range
            self.canvas.create_text(640, 260, text="ODOMETER", fill="#555", font=("Arial", 8), tags="screen_data") # Label Odometer
            self.canvas.create_text(640, 275, text=f"{int(stats['odometer_km'])} km", fill="white", font=("Courier", 12), tags="screen_data") # Show Odometer
            self.canvas.create_text(640, 305, text="AFR", fill="#555", font=("Arial", 8), tags="screen_data") # Label AFR
            self.canvas.create_text(640, 320, text=f"{stats['afr']}:1", fill="cyan", font=("Courier", 12), tags="screen_data") # Show AFR

        elif page == "PERFORMANCE": # Render PERFORMANCE page
            self.canvas.create_text(600, 220, text="HP", fill="#555", font=("Arial", 8), tags="screen_data") # Label HP
            self.canvas.create_text(600, 235, text=f"{stats['power_hp']}", fill="orange", font=("Courier", 14, "bold"), tags="screen_data") # Show HP
            self.canvas.create_text(680, 220, text="TRQ", fill="#555", font=("Arial", 8), tags="screen_data") # Label TRQ
            self.canvas.create_text(680, 235, text=f"{stats['torque_nm']}", fill="orange", font=("Courier", 14, "bold"), tags="screen_data") # Show TRQ
            self.canvas.create_text(640, 265, text=f"G-FORCE: {stats['accel_g']} G", fill="white", font=("Courier", 12), tags="screen_data") # Show G-Force
            self.canvas.create_text(640, 300, text="0-100 km/h", fill="#555", font=("Arial", 8), tags="screen_data") # Label 0-100
            timer_col = "red" if stats['timer_0_100'] > 0 else "#444" # Determine color for timer
            if stats['best_0_100'] > 0: timer_col = "#4f4" # Green if completed
            disp_time = stats['timer_0_100'] if stats['timer_0_100'] > 0 else stats['best_0_100'] # Choose time to display
            self.canvas.create_text(640, 315, text=f"{disp_time} s", fill=timer_col, font=("Courier", 14, "bold"), tags="screen_data") # Show Time

        elif page == "DIAGNOSTICS": # Render DIAGNOSTICS page
            self.canvas.create_text(590, 220, text="TRANS TEMP", fill="#555", font=("Arial", 7), tags="screen_data") # Label Trans Temp
            self.canvas.create_text(590, 235, text=f"{stats['trans_temp']}°C", fill="white", font=("Courier", 11), tags="screen_data") # Show Trans Temp
            self.canvas.create_text(690, 220, text="INTAKE AIR", fill="#555", font=("Arial", 7), tags="screen_data") # Label IAT
            self.canvas.create_text(690, 235, text=f"{stats['iat_temp']}°C", fill="white", font=("Courier", 11), tags="screen_data") # Show IAT
            self.canvas.create_text(590, 270, text="CONV. SLIP", fill="#555", font=("Arial", 7), tags="screen_data") # Label Slip
            self.canvas.create_text(590, 285, text=f"{stats['slip_rpm']}", fill="orange", font=("Courier", 11), tags="screen_data") # Show Slip
            self.canvas.create_text(690, 270, text="LOCKUP", fill="#555", font=("Arial", 7), tags="screen_data") # Label Lockup
            status = "CLOSED" if stats['lockup'] else "OPEN" # Describe status
            col = "#4f4" if stats['lockup'] else "#f44" # Status color
            self.canvas.create_text(690, 285, text=status, fill=col, font=("Courier", 10, "bold"), tags="screen_data") # Show Status
            self.canvas.create_text(640, 315, text=f"OIL P: {stats['oil_pressure']} bar", fill="#aaa", font=("Courier", 10), tags="screen_data") # Show Oil Pressure

    def smooth_value(self, key, target, max_change_rate, dt): # Helper method to smooth gauge movement
        current = self.needle_values.get(key, target) # Get current value
        diff = target - current # Calculate difference
        max_step = max_change_rate * dt # Calculate max step allowed
        if abs(diff) <= max_step: self.needle_values[key] = target # If close, snap to target
        else: self.needle_values[key] += math.copysign(max_step, diff) # Else move towards target
        return self.needle_values[key] # Return new value

    def update_loop(self): # Main application loop
        current_time = time.time() # Get current time
        dt = current_time - self.last_time # Calculate delta time
        self.last_time = current_time # Update last time
        
        throttle_input = 1.0 if (self.gas_mouse_active or self.key_gas) else 0.0 # Calculate throttle input
        brake_input = 1.0 if (self.brake_mouse_active or self.key_brake) else 0.0 # Calculate brake input
        
        self.sim.set_inputs(throttle_input, brake_input) # Send inputs to simulator
        stats = self.sim.update(dt) # Tick the simulator
        
        if not hasattr(self, 'gauges_initialized'): # Check if gauges are drawn
            self.canvas.delete("all") # Clear canvas
            self.draw_gauge_background(360, 280, 140, 0, 8, "x1000", 8, unit="RPM") # Draw RPM gauge
            self.draw_gauge_background(920, 280, 140, 0, 320, "km/h", 8) # Draw Speedometer
            self.draw_gauge_background(140, 360, 75, 50, 150, "OIL", 2, unit="°C", icon_type="oil") # Draw Oil gauge
            self.draw_gauge_background(1140, 360, 75, 8, 16, "BATT", 2, unit="V", icon_type="batt") # Draw Battery gauge
            self.draw_gauge_background(570, 430, 45, 50, 130, "ENGINE", 2, icon_type="temp") # Draw Temp gauge
            self.draw_gauge_background(710, 430, 45, 0, 1, "FUEL", 2, icon_type="fuel") # Draw Fuel gauge
            self.draw_center_screen_static() # Draw screen background
            self.gauges_initialized = True # Mark initialized

        val_rpm = self.smooth_value('rpm', stats['rpm']/1000, 8.0, dt) # Smooth RPM
        val_speed = self.smooth_value('speed', stats['speed_kmh'], 160.0, dt) # Smooth Speed
        val_oil = self.smooth_value('oil', stats['oil_temp'], 10.0, dt) # Smooth Oil
        val_coolant = self.smooth_value('coolant', stats['engine_temp'], 10.0, dt) # Smooth Coolant
        val_fuel = self.smooth_value('fuel', stats['fuel_ltr']/90.0, 0.05, dt) # Smooth Fuel
        target_volts = 11.5 + (stats['battery_pct']/100 * 3.0) # Calculate target voltage
        val_batt = self.smooth_value('batt', target_volts, 2.0, dt) # Smooth Battery

        self.update_needle("needle_rpm", 360, 280, 140, val_rpm, 0, 8) # Update RPM needle
        self.update_needle("needle_speed", 920, 280, 140, val_speed, 0, 320) # Update Speed needle
        self.update_needle("needle_oil", 140, 360, 75, val_oil, 50, 150) # Update Oil needle
        self.update_needle("needle_batt", 1140, 360, 75, val_batt, 8, 16) # Update Battery needle
        self.update_needle("needle_coolant", 570, 430, 45, val_coolant, 50, 130) # Update Coolant needle
        self.update_needle("needle_fuel", 710, 430, 45, val_fuel, 0, 1) # Update Fuel needle

        if current_time - self.last_screen_update >= 0.25: # Check if screen update needed (4Hz)
             self.update_center_screen(stats) # Update center screen
             self.last_screen_update = current_time # Reset timer

        self.root.after(30, self.update_loop) # Schedule next frame (approx 30ms)

if __name__ == "__main__": # Entry point
    root = tk.Tk() # Create root window
    app = DashboardApp(root) # Create application instance
    root.mainloop() # Start main event loop