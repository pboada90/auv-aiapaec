from pymavlink import mavutil
import time

# Connect to the Pixhawk via USB (change the port if necessary)
master = mavutil.mavlink_connection('COM4', baud=115200)  # Replace 'COM3' with your USB port on Windows or '/dev/ttyUSB0' on Linux/Mac

# Wait until receiving a heartbeat from the Pixhawk
print("Waiting for connection to Pixhawk...")
try:
    master.wait_heartbeat(timeout=5)  # Increase timeout if necessary
    print("Connected to Pixhawk")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)  # Exit the script if connection fails

# Change flight mode to "MANUAL"
def set_mode(mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    print(f"Mode changed to {mode}")

# Change to MANUAL mode to control the AUV
set_mode("MANUAL")

# Monitor the status of the vehicle
def monitor_status():
    while True:
        msg = master.recv_match(type='STATUSTEXT', blocking=True)
        print(f"Status: {msg.text}")
        time.sleep(1)

# Start monitoring in a separate thread if needed
import threading
status_thread = threading.Thread(target=monitor_status)
status_thread.start()

# Arm the vehicle
print("Arming the vehicle...")
master.arducopter_arm()
start_time = time.time()

# Wait for the vehicle to arm
while time.time() - start_time < 10:  # Wait for 10 seconds
    if master.motors_armed():
        print("Vehicle armed successfully")
        break
    time.sleep(1)
else:
    print("Failed to arm the vehicle. Check conditions.")

# Send throttle commands to the motors (channels 1 and 2, corresponding to MAIN1 and MAIN2)
def set_throttle(throttle_value):
    # throttle_value ranges from 0 to 1000 (0 is no movement, 1000 is full power)
    pwm_signal = int(1100 + (throttle_value * 0.8))  # Adjust the PWM range (usually 1100-1900)
    
    # Send PWM signal to the motor channels
    master.mav.rc_channels_override_send(
        master.target_system,  # target_system
        master.target_component,  # target_component
        pwm_signal,  # Channel 1 (Motor 1 - Thruster 0)
        pwm_signal,  # Channel 2 (Motor 2 - Thruster 1)
        0, 0, 0, 0, 0, 0  # Remaining channels not used
    )
    print(f"Signal sent with throttle: {throttle_value}")

# Test turning on the motors for 5 seconds with 50% throttle
set_throttle(500)  # 50% of maximum throttle
time.sleep(5)

# Stop the motors
set_throttle(0)

# Disarm the vehicle
master.arducopter_disarm()
print("Vehicle disarmed")