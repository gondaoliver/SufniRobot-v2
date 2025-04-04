import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import pyautogui
import threading

# Initialize servo driver (3 servos: 0-Shoulder, 1-Elbow, 2-Gripper)
#kit = ServoKit(channels=16)
#servo_positions = [90, 90, 90]  # Initial positions [Shoulder, Elbow, Gripper]

# Motor control setup (unchanged)
# 1.x front 2.x back x.1 forward x.2 backwarde

RIGHT11 = 24
RIGHT12 = 23
RIGHT21 = 25
RIGHT22 = 27 
LEFT11 = 13
LEFT12 = 16
LEFT21 = 6
LEFT22 = 5


GPIO.setmode(GPIO.BCM)

GPIO.setup(RIGHT11, GPIO.OUT)
GPIO.setup(RIGHT12, GPIO.OUT)
GPIO.setup(RIGHT21, GPIO.OUT)
GPIO.setup(RIGHT22, GPIO.OUT) 
GPIO.setup(LEFT11, GPIO.OUT)
GPIO.setup(LEFT12, GPIO.OUT)
GPIO.setup(LEFT21, GPIO.OUT)
GPIO.setup(LEFT22, GPIO.OUT)

# Steering servo setup (unchanged)
# p = GPIO.PWM(SERVO_Steering, 50)
# p.start(0)

# Controller setup
is_running = True

def stop():
    global is_running
    is_running = False
    
    # # Stop all servos
    # for i in range(3):
    #     kit.servo[i].angle = None  # Release servo motor
        
    # Stop vehicle motor and clean up
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)

    print("All motors stopped and cleaned up")

# def move_servo(index, step):
#     """Move specified servo with angle clamping"""
#     new_angle = max(0, min(180, servo_positions[index] + step))
#     servo_positions[index] = new_angle
#     kit.servo[index].angle = new_angle
#     print(f"Servo {['Shoulder', 'Elbow', 'Gripper'][index]} moved to {new_angle}°")

# # Shoulder control (△/× buttons)
# def on_triangle_btn_pressed():
#     move_servo(0, 5)  # Shoulder up

# def on_cross_btn_pressed():
#     move_servo(0, -5)  # Shoulder down

# # Elbow control (L1/R1)
# def on_L1_btn_pressed():
#     move_servo(1, 5)   # Elbow up

# def on_R1_btn_pressed():
#     move_servo(1, -5)  # Elbow down

# # Gripper control (L3/R3)
# def on_L3_btn_pressed():
#     move_servo(2, 10)  # Open gripper

# def on_R3_btn_pressed():
#     move_servo(2, -10)  # Close gripper

# Original vehicle controls (unchanged)
def on_W_pressed():
    GPIO.output(RIGHT11, GPIO.HIGH)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.HIGH)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.HIGH)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.HIGH)
    GPIO.output(LEFT22, GPIO.LOW)

def on_W_released():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    time.sleep(0.1)


def on_S_pressed():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.HIGH)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.HIGH)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.HIGH)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.HIGH)

def on_S_released():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    time.sleep(0.1)

def on_A_pressed():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.HIGH)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.HIGH)
    GPIO.output(RIGHT11, GPIO.HIGH)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.HIGH)
    GPIO.output(RIGHT22, GPIO.LOW)

def on_A_released():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    time.sleep(0.1)

def on_D_pressed():
    GPIO.output(LEFT11, GPIO.HIGH)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.HIGH)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.HIGH)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.HIGH)

def on_D_released():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    time.sleep(0.1)


def key_listener():
    """Listen for keyboard events and trigger corresponding functions."""
    while is_running:
        if pyautogui.keyDown('w'):
            on_W_pressed()
        else:
            on_W_released()

        if pyautogui.keyDown('s'):
            on_S_pressed()
        else:
            on_S_released()

        if pyautogui.keyDown('a'):
            on_A_pressed()
        else:
            on_A_released()

        if pyautogui.keyDown('d'):
            on_D_pressed()
        else:
            on_D_released()

listener_thread = threading.Thread(target=key_listener, daemon=True)
listener_thread.start()


try:
    while is_running:
        time.sleep(0.001)
        time.sleep(0.001)
finally:
    stop()  # Ensure cleanup even if error occurs
    controller.deactivate()