# Configuration file for Kitchen Exhaust Fan Controller

# GPIO Pin Configuration
SMOKE_SENSOR_PIN = 15  # GPIO pin connected to MQ smoke sensor digital output
RELAY_PIN = 14         # GPIO pin connected to relay control input

# Timing Configuration
SMOKE_CLEAR_DELAY_MINUTES = 10  # Minutes to wait after smoke clears before turning off fan
CHECK_INTERVAL_SECONDS = 0.5    # How often to check the smoke sensor (in seconds)

# Sensor Configuration
# Set to True if your MQ sensor outputs HIGH (1) when smoke is detected
# Set to False if your MQ sensor outputs LOW (0) when smoke is detected
SMOKE_DETECTED_HIGH = True

# Relay Configuration
# Set to True if relay activates with HIGH signal (most common)
# Set to False if relay activates with LOW signal
RELAY_ACTIVE_HIGH = True

# Debug Configuration
VERBOSE_LOGGING = True  # Set to False to reduce console output
