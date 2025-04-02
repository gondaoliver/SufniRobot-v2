from time import sleep
import RPi.GPIO as GPIO
from dualsense_controller import DualSenseController
from adafruit_servokit import ServoKit

# Initialize servo driver (3 servos: 0-Shoulder, 1-Elbow, 2-Gripper)
#kit = ServoKit(channels=16)
#servo_positions = [90, 90, 90]  # Initial positions [Shoulder, Elbow, Gripper]

# Motor control setup (unchanged)
# 1.x front 2.x back
RIGHT1.1 = 24
RIGHT1.2 = 23
RIGHT2.1 = 25
RIGHT2.2 = 27 
LEFT1.1 = 13
LEFT1.2 = 19
LEFT2.1 = 5
LEFT2.2 = 6

ENA = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(RIGHT1.1, GPIO.OUT)
GPIO.setup(RIGHT1.2, GPIO.OUT)
GPIO.setup(RIGHT2.1, GPIO.OUT)
GPIO.setup(RIGHT2.2, GPIO.OUT) 
GPIO.setup(LEFT1.1, GPIO.OUT)
GPIO.setup(LEFT1.2, GPIO.OUT)
GPIO.setup(LEFT2.1, GPIO.OUT)
GPIO.setup(LEFT2.2, GPIO.OUT)

GPIO.setup(ENA, GPIO.OUT)
GPIO.output(ENA, GPIO.HIGH)

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
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    p.stop()
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
    GPIO.output(RIGHT1.1, GPIO.HIGH)
    GPIO.output(RIGHT1.2, GPIO.LOW)
    GPIO.output(RIGHT2.1, GPIO.HIGH)
    GPIO.output(RIGHT2.2, GPIO.LOW)
    GPIO.output(LEFT1.1, GPIO.HIGH)
    GPIO.output(LEFT1.2, GPIO.LOW)
    GPIO.output(LEFT2.1, GPIO.HIGH)
    GPIO.output(LEFT2.2, GPIO.LOW)

def on_R2_btn_released():
    GPIO.output(RIGHT1.1, GPIO.LOW)
    GPIO.output(RIGHT1.2, GPIO.LOW)
    GPIO.output(RIGHT2.1, GPIO.LOW)
    GPIO.output(RIGHT2.2, GPIO.LOW)
    GPIO.output(LEFT1.1, GPIO.LOW)
    GPIO.output(LEFT1.2, GPIO.LOW)
    GPIO.output(LEFT2.1, GPIO.LOW)
    GPIO.output(LEFT2.2, GPIO.LOW)


def on_L2_btn_pressed():
    GPIO.output(RIGHT1.1, GPIO.LOW)
    GPIO.output(RIGHT1.2, GPIO.HIGH)
    GPIO.output(RIGHT2.1, GPIO.LOW)
    GPIO.output(RIGHT2.2, GPIO.HIGH)
    GPIO.output(LEFT1.1, GPIO.LOW)
    GPIO.output(LEFT1.2, GPIO.HIGH)
    GPIO.output(LEFT2.1, GPIO.LOW)
    GPIO.output(LEFT2.2, GPIO.HIGH)

def on_L2_btn_released():
    GPIO.output(RIGHT1.1, GPIO.LOW)
    GPIO.output(RIGHT1.2, GPIO.LOW)
    GPIO.output(RIGHT2.1, GPIO.LOW)
    GPIO.output(RIGHT2.2, GPIO.LOW)
    GPIO.output(LEFT1.1, GPIO.LOW)
    GPIO.output(LEFT1.2, GPIO.LOW)
    GPIO.output(LEFT2.1, GPIO.LOW)
    GPIO.output(LEFT2.2, GPIO.LOW)

def on_left_stick_moved(joystick):
    duty_cycle = 7.5 + (joystick.x * -2.5)
    duty_cycle = max(5, min(10, duty_cycle))
    p.ChangeDutyCycle(duty_cycle)

# Event bindings
controller.btn_ps.on_down(lambda: stop())
controller.btn_r2.on_down(on_R2_btn_pressed)
controller.btn_r2.on_up(on_R2_btn_released)
controller.btn_l2.on_down(on_L2_btn_pressed)
controller.btn_l2.on_up(on_L2_btn_released)
controller.left_stick.on_change(on_left_stick_moved)
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
