# Kitchen Exhaust Fan Operated by Smoke Sensor

This project uses a Raspberry Pi Pico W, a 5VDC/120VAC relay, a Flying Fish MQ smoke sensor, and a 120VAC kitchen exhaust fan. The fan automatically turns on when the MQ sensor detects smoke and turns off 10 minutes after smoke is no longer sensed.

## Hardware Requirements

- **Raspberry Pi Pico W** - Microcontroller board
- **Flying Fish MQ Smoke Sensor** - Digital smoke detection sensor (MQ-2, MQ-135, or similar)
- **5VDC/120VAC Relay Module** - To control the high voltage fan
- **120VAC Kitchen Exhaust Fan** - The fan to be controlled
- **Power Supply** - 5V USB power for Pico W (relay may need separate 5V supply)
- **Jumper Wires** - For connections

## Software Requirements

- **Thonny IDE** - For programming the Pico
- **MicroPython** - Firmware for Raspberry Pi Pico W

## Pin Connections

### Default Pin Configuration

| Component | Pin | GPIO | Description |
|-----------|-----|------|-------------|
| MQ Smoke Sensor (DO) | Pin 20 | GPIO 15 | Digital output from sensor |
| Relay Control (IN) | Pin 19 | GPIO 14 | Control signal to relay |
| MQ Sensor VCC | VBUS (Pin 40) | - | 5V power |
| MQ Sensor GND | GND | - | Ground |
| Relay VCC | VBUS (Pin 40) | - | 5V power |
| Relay GND | GND | - | Ground |

### Wiring Diagram (Text)

```
Raspberry Pi Pico W:
  GPIO 15 (Pin 20) -----> MQ Sensor Digital Out (DO)
  GPIO 14 (Pin 19) -----> Relay Control (IN)
  VBUS (Pin 40)     -----> MQ Sensor VCC & Relay VCC
  GND               -----> MQ Sensor GND & Relay GND

Relay Module:
  COM (Common)      -----> 120VAC Hot Line from wall
  NO (Normally Open)-----> Fan Hot Wire
  
Fan:
  Hot Wire          -----> Relay NO (Normally Open)
  Neutral Wire      -----> 120VAC Neutral (direct connection)
  Ground Wire       -----> 120VAC Ground (direct connection)
```

⚠️ **SAFETY WARNING**: Working with 120VAC can be DANGEROUS and potentially FATAL. If you are not experienced with electrical wiring, consult a licensed electrician. Always disconnect power before making any connections.

## Installation

### 1. Install MicroPython on Raspberry Pi Pico W

1. Download the latest MicroPython firmware for Pico W from [micropython.org](https://micropython.org/download/rp2-pico-w/)
2. Hold the BOOTSEL button on the Pico W and connect it to your computer via USB
3. The Pico will appear as a USB mass storage device
4. Copy the `.uf2` firmware file to the Pico W
5. The Pico will automatically reboot with MicroPython installed

### 2. Install Thonny IDE

1. Download and install Thonny from [thonny.org](https://thonny.org/)
2. Open Thonny and go to Tools > Options > Interpreter
3. Select "MicroPython (Raspberry Pi Pico)" as the interpreter
4. Select the correct COM port for your Pico W

### 3. Upload the Code

1. Clone or download this repository
2. Open `main.py` in Thonny
3. (Optional) Modify `config.py` to customize pin assignments and timing
4. Save `main.py` to the Raspberry Pi Pico W (File > Save as... > Raspberry Pi Pico)
5. Save `config.py` to the Raspberry Pi Pico W (if customized)
6. The program will start automatically when the Pico is powered on

## Configuration

Edit `config.py` to customize the behavior:

```python
# GPIO Pin Configuration
SMOKE_SENSOR_PIN = 15  # Change if using different GPIO pin
RELAY_PIN = 14         # Change if using different GPIO pin

# Timing Configuration
SMOKE_CLEAR_DELAY_MINUTES = 10  # Minutes to wait after smoke clears
CHECK_INTERVAL_SECONDS = 0.5    # Sensor polling interval

# Sensor Configuration
SMOKE_DETECTED_HIGH = True  # True if sensor outputs HIGH when smoke detected

# Relay Configuration
RELAY_ACTIVE_HIGH = True  # True if relay activates with HIGH signal

# Debug Configuration
VERBOSE_LOGGING = True  # Set to False to reduce console output
```

## Operation

1. **Power On**: When the Pico W is powered, the program starts automatically
2. **Monitoring**: The system continuously monitors the smoke sensor
3. **Smoke Detected**: When smoke is detected:
   - The relay activates
   - The exhaust fan turns ON
   - A message is printed to the console
4. **Smoke Clears**: When smoke is no longer detected:
   - The fan continues running for 10 minutes (configurable)
   - Progress messages are printed every minute
5. **Fan Off**: After 10 minutes without smoke detection:
   - The relay deactivates
   - The fan turns OFF

## Testing

### Test the Sensor
1. Connect only the sensor first
2. Run the program and monitor the console
3. Expose the sensor to smoke (safely - try a match or incense)
4. Verify that "SMOKE DETECTED!" appears in the console

### Test the Relay
1. Connect the relay (without 120VAC initially)
2. Test with smoke to verify the relay clicks ON
3. Verify the relay turns OFF after 10 minutes

### Full System Test
1. With 120VAC properly connected by a qualified electrician
2. Test with real smoke to verify fan operation
3. Verify 10-minute delay before fan turns off

## Troubleshooting

### Fan doesn't turn on
- Check all wiring connections
- Verify GPIO pins in `config.py` match your wiring
- Check if relay LED lights up when smoke is detected
- Try setting `RELAY_ACTIVE_HIGH = False` in config.py

### Fan doesn't turn off
- Check console for error messages
- Verify sensor returns to normal state when smoke clears
- Adjust sensor sensitivity potentiometer on MQ module

### False triggers
- Adjust the sensitivity potentiometer on the MQ sensor module
- Increase `CHECK_INTERVAL_SECONDS` in config.py
- Ensure sensor has proper warm-up time (MQ sensors need ~24-48 hours for best accuracy)

## Safety Notes

- ⚠️ **HIGH VOLTAGE**: This project involves 120VAC which can be lethal. Use extreme caution.
- Always disconnect power before working on connections
- Use proper electrical boxes and conduit as required by electrical code
- Have a qualified electrician perform the 120VAC wiring
- Test the smoke sensor regularly to ensure proper operation
- Consider adding a manual override switch for the fan
- This is a supplemental system and should not replace proper kitchen ventilation or smoke detectors

## License

This project is open source. Use at your own risk.

## Contributing

Feel free to open issues or submit pull requests with improvements.
 
