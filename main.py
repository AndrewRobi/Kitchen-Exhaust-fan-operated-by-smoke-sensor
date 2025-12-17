"""
Kitchen Exhaust Fan Controller with Smoke Sensor
For Raspberry Pi Pico with MicroPython

Hardware:
- Raspberry Pi Pico
- Flying Fish MQ Smoke Sensor (Digital output)
- 5VDC/120VAC Relay Module
- 120VAC Kitchen Exhaust Fan

Pin Configuration:
- GPIO 15: Smoke Sensor Digital Output (INPUT)
- GPIO 14: Relay Control (OUTPUT)
"""

import machine
import time

try:
    from config import (
        SMOKE_SENSOR_PIN, 
        RELAY_PIN, 
        SMOKE_CLEAR_DELAY_MINUTES,
        CHECK_INTERVAL_SECONDS,
        SMOKE_DETECTED_HIGH,
        RELAY_ACTIVE_HIGH,
        VERBOSE_LOGGING
    )
    SMOKE_CLEAR_DELAY = SMOKE_CLEAR_DELAY_MINUTES * 60
    CHECK_INTERVAL = CHECK_INTERVAL_SECONDS
except ImportError:
    # Use default values if config.py is not found
    SMOKE_SENSOR_PIN = 15
    RELAY_PIN = 14
    SMOKE_CLEAR_DELAY = 600  # 10 minutes in seconds
    CHECK_INTERVAL = 0.5
    SMOKE_DETECTED_HIGH = True
    RELAY_ACTIVE_HIGH = True
    VERBOSE_LOGGING = True
    print("Warning: config.py not found, using default configuration")

# Initialize GPIO pins
smoke_sensor = machine.Pin(SMOKE_SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)

# Initialize relay to OFF state (fan off)
relay.value(0 if RELAY_ACTIVE_HIGH else 1)

# State variables
fan_running = False
last_smoke_time = 0
last_minute_printed = -1  # Track last printed minute to avoid duplicates

print("Kitchen Exhaust Fan Controller Started")
print(f"Smoke Sensor Pin: GPIO{SMOKE_SENSOR_PIN}")
print(f"Relay Control Pin: GPIO{RELAY_PIN}")
print(f"Smoke Clear Delay: {SMOKE_CLEAR_DELAY} seconds ({SMOKE_CLEAR_DELAY // 60} minutes)")
print("System ready. Monitoring for smoke...")

def turn_fan_on():
    """Turn the fan ON by activating the relay"""
    global fan_running, last_minute_printed
    if not fan_running:
        relay.value(1 if RELAY_ACTIVE_HIGH else 0)
        fan_running = True
        last_minute_printed = -1  # Reset minute tracking
        print("SMOKE DETECTED! Fan turned ON")

def turn_fan_off():
    """Turn the fan OFF by deactivating the relay"""
    global fan_running
    if fan_running:
        relay.value(0 if RELAY_ACTIVE_HIGH else 1)
        fan_running = False
        print("Fan turned OFF")

def read_smoke_sensor():
    """
    Read the smoke sensor digital output.
    Returns True if smoke is detected, False otherwise.
    
    Note: MQ sensors typically output HIGH (1) when smoke is detected,
    but this may vary by sensor module. Adjust in config.py if needed.
    """
    sensor_value = smoke_sensor.value()
    if SMOKE_DETECTED_HIGH:
        return sensor_value == 1
    else:
        return sensor_value == 0

def main_loop():
    """Main control loop for monitoring smoke and controlling fan"""
    global fan_running, last_smoke_time, last_minute_printed
    
    while True:
        # Read the smoke sensor
        smoke_detected = read_smoke_sensor()
        
        if smoke_detected:
            # Smoke detected - turn fan on and update timestamp
            turn_fan_on()
            last_smoke_time = time.time()
        else:
            # No smoke detected
            if fan_running:
                # Fan is running - check if delay period has elapsed
                time_since_smoke = time.time() - last_smoke_time
                
                if time_since_smoke >= SMOKE_CLEAR_DELAY:
                    # Delay period elapsed - turn fan off
                    print(f"No smoke for {SMOKE_CLEAR_DELAY // 60} minutes. Turning fan off...")
                    turn_fan_off()
                else:
                    # Still within delay period - keep fan running
                    if VERBOSE_LOGGING:
                        remaining = SMOKE_CLEAR_DELAY - time_since_smoke
                        minutes_remaining = int(remaining // 60)
                        # Print once per minute when the minute changes
                        # Also print when reaching 0 minutes (< 60 seconds remaining)
                        if minutes_remaining != last_minute_printed:
                            last_minute_printed = minutes_remaining
                            if minutes_remaining > 0:
                                print(f"Fan still running. Time remaining: {minutes_remaining} minutes")
                            elif minutes_remaining == 0 and remaining > 0:
                                print(f"Fan still running. Time remaining: <1 minute")
        
        # Wait before next check
        time.sleep(CHECK_INTERVAL)

# Main control loop
try:
    main_loop()
except KeyboardInterrupt:
    print("\nShutting down...")
    turn_fan_off()
    print("System stopped")
