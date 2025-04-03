from time import sleep
import RPi.GPIO as GPIO
from dualsense_controller import DualSenseController
from adafruit_servokit import ServoKit

# Initialize servo driver (3 servos: 0-Shoulder, 1-Elbow, 2-Gripper)
#kit = ServoKit(channels=16)
#servo_positions = [90, 90, 90]  # Initial positions [Shoulder, Elbow, Gripper]

# Motor control setup (unchanged)
# 1.x front 2.x back
RIGHT11 = 24
RIGHT12 = 23
RIGHT21 = 25
RIGHT22 = 27 
LEFT11 = 13
LEFT12 = 19
LEFT21 = 5
LEFT22 = 26


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
controller = DualSenseController()
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

    GPIO.cleanup()
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
def on_R2_btn_pressed():
    GPIO.output(RIGHT11, GPIO.HIGH)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.HIGH)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.HIGH)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.HIGH)
    GPIO.output(LEFT22, GPIO.LOW)

def on_R2_btn_released():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)


def on_L2_btn_pressed():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.HIGH)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.HIGH)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.HIGH)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.HIGH)

def on_L2_btn_released():
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)

def on_L1_btn_pressed():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.HIGH)
    GPIO.output(RIGHT12, GPIO.HIGH)
    GPIO.output(RIGHT21, GPIO.HIGH)
    GPIO.output(RIGHT22, GPIO.HIGH)

def on_L1_btn_released():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)

def on_R1_btn_pressed():
    GPIO.output(LEFT11, GPIO.HIGH)
    GPIO.output(LEFT12, GPIO.HIGH)
    GPIO.output(LEFT21, GPIO.HIGH)
    GPIO.output(LEFT22, GPIO.HIGH)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)

def on_R1_btn_released():
    GPIO.output(LEFT11, GPIO.LOW)
    GPIO.output(LEFT12, GPIO.LOW)
    GPIO.output(LEFT21, GPIO.LOW)
    GPIO.output(LEFT22, GPIO.LOW)
    GPIO.output(RIGHT11, GPIO.LOW)
    GPIO.output(RIGHT12, GPIO.LOW)
    GPIO.output(RIGHT21, GPIO.LOW)
    GPIO.output(RIGHT22, GPIO.LOW)



# Event bindings
controller.btn_ps.on_down(lambda: stop())
controller.btn_r2.on_down(on_R2_btn_pressed)
controller.btn_r2.on_up(on_R2_btn_released)
controller.btn_l2.on_down(on_L2_btn_pressed)
controller.btn_l2.on_up(on_L2_btn_released)
controller.btn_l1.on_down(on_L1_btn_pressed)
controller.btn_l1.on_up(on_L1_btn_released)
controller.btn_r1.on_down(on_R1_btn_pressed)
controller.btn_r1.on_up(on_R1_btn_released)

# controller.btn_triangle.on_down(on_triangle_btn_pressed)
# controller.btn_cross.on_down(on_cross_btn_pressed)
# controller.btn_l1.on_down(on_L1_btn_pressed)
# controller.btn_r1.on_down(on_R1_btn_pressed)
# controller.btn_l3.on_down(on_L3_btn_pressed)
# controller.btn_r3.on_down(on_R3_btn_pressed)

controller.activate()

try:
    while is_running:
        sleep(0.001)
finally:
    stop()  # Ensure cleanup even if error occurs
    controller.deactivate()
