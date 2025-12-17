# Example Usage and Testing Guide

## Quick Start

1. **Upload Files**: Copy `main.py` and `config.py` to your Raspberry Pi Pico
2. **Connect Hardware**: Wire the smoke sensor and relay as described in README.md
3. **Power On**: The system starts automatically

## Testing Without Hardware

You can simulate the behavior using a test script on your computer to understand the logic:

```python
import time

# Simulated sensor that returns smoke detection status
def simulated_sensor():
    """Simulate smoke detection for testing"""
    current_time = time.time()
    # Simulate smoke for first 30 seconds of each 2-minute cycle
    return (int(current_time) % 120) < 30

# Test parameters
SMOKE_CLEAR_DELAY = 600  # 10 minutes
fan_running = False
last_smoke_time = 0

print("Starting simulation...")
print("Simulating smoke for 30 seconds every 2 minutes")

for i in range(180):  # Run for 3 minutes
    smoke_detected = simulated_sensor()
    
    if smoke_detected:
        if not fan_running:
            print(f"[{i}s] SMOKE DETECTED! Fan turned ON")
            fan_running = True
        last_smoke_time = time.time()
    else:
        if fan_running:
            time_since_smoke = time.time() - last_smoke_time
            if time_since_smoke >= SMOKE_CLEAR_DELAY:
                print(f"[{i}s] No smoke for 10 minutes. Fan turned OFF")
                fan_running = False
            elif int(time_since_smoke) % 10 == 0:
                remaining = SMOKE_CLEAR_DELAY - time_since_smoke
                print(f"[{i}s] Fan running. {int(remaining)}s remaining")
    
    time.sleep(1)
```

## Hardware Testing Steps

### Step 1: Test Sensor Only
```python
# Save this as test_sensor.py
import machine
import time

SMOKE_SENSOR_PIN = 15
smoke_sensor = machine.Pin(SMOKE_SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)

print("Testing smoke sensor...")
print("Expose sensor to smoke to test")

while True:
    value = smoke_sensor.value()
    print(f"Sensor value: {value}")
    time.sleep(1)
```

### Step 2: Test Relay Only
```python
# Save this as test_relay.py
import machine
import time

RELAY_PIN = 14
relay = machine.Pin(RELAY_PIN, machine.Pin.OUT)

print("Testing relay...")
print("Relay will turn ON for 3 seconds, then OFF for 3 seconds")

while True:
    print("Relay ON")
    relay.value(1)
    time.sleep(3)
    
    print("Relay OFF")
    relay.value(0)
    time.sleep(3)
```

### Step 3: Full System Test
1. Run `main.py`
2. Safely create smoke near the sensor (use incense or a match)
3. Verify fan turns on
4. Remove smoke source
5. Wait and verify fan turns off after 10 minutes

## Expected Console Output

```
Kitchen Exhaust Fan Controller Started
Smoke Sensor Pin: GPIO15
Relay Control Pin: GPIO14
Smoke Clear Delay: 600 seconds (10 minutes)
System ready. Monitoring for smoke...
SMOKE DETECTED! Fan turned ON
Fan still running. Time remaining: 9 minutes
Fan still running. Time remaining: 8 minutes
Fan still running. Time remaining: 7 minutes
...
Fan still running. Time remaining: 1 minute
No smoke for 10 minutes. Turning fan off...
Fan turned OFF
```

## Customization Examples

### Change to 15-minute delay
Edit `config.py`:
```python
SMOKE_CLEAR_DELAY_MINUTES = 15
```

### Use different GPIO pins
Edit `config.py`:
```python
SMOKE_SENSOR_PIN = 16  # Changed from 15
RELAY_PIN = 17         # Changed from 14
```

### Invert relay logic (for active-low relays)
Edit `config.py`:
```python
RELAY_ACTIVE_HIGH = False
```

### Reduce console messages
Edit `config.py`:
```python
VERBOSE_LOGGING = False
```

## Common Modifications

### Add LED indicator
```python
# Add to main.py after imports
led = machine.Pin(25, machine.Pin.OUT)  # Built-in LED on Pico

# In turn_fan_on():
led.value(1)  # LED on when fan is on

# In turn_fan_off():
led.value(0)  # LED off when fan is off
```

### Add debouncing for sensor
```python
# Add to main.py
DEBOUNCE_COUNT = 3
smoke_count = 0

# In main loop, replace smoke_detected = read_smoke_sensor() with:
if read_smoke_sensor():
    smoke_count += 1
else:
    smoke_count = 0

smoke_detected = smoke_count >= DEBOUNCE_COUNT
```

### Log to file
```python
# Add to main.py
def log_event(message):
    with open("fan_log.txt", "a") as f:
        timestamp = time.localtime()
        f.write(f"{timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d} - {message}\n")

# Use in turn_fan_on() and turn_fan_off()
log_event("Fan turned ON - smoke detected")
log_event("Fan turned OFF - no smoke for 10 minutes")
```
