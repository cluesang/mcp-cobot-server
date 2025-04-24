import time
from command_queue import CommandQueue
from pymycobot.mycobot280 import MyCobot280

# Create a real MyCobot280 object (update the port as needed)
mc = MyCobot280("/dev/tty.usbserial-588D0016561", 115200)

# Create the command queue
queue = CommandQueue()

# Print initial state
def print_state(label):
    state = queue.get_state()
    print(f"{label} | State: running={state['running']}, paused={state['paused']}, queue_length={state['queue_length']}")

print_state("Initial")

# Define angles and speed
angles1 = [10, -10, 10, -10, 10, -10]
angles2 = [-10, 10, -10, 10, -10, 10]
speed = 50

# Add the move_angles command to the queue
print("Adding move_angles command to the queue...")
queue.add_command(mc.send_angles, angles1, speed)
queue.add_command(mc.send_angles, angles2, speed)
print_state("After adding move_angles")

# Allow some time for the queue to process
print("Waiting for the command to be processed...")
time.sleep(2)
print_state("After processing")

print("If your cobot moved, the command was executed.")

try:
    print("Script running. Press Ctrl+C to exit.")
    while True:
        print_state("While running")
        time.sleep(1)
        queue.add_command(mc.send_angles, angles1, speed)
        queue.add_command(mc.send_angles, angles2, speed)
        time.sleep(3)
except KeyboardInterrupt:
    print("\nExiting on user request.")
finally:
    queue.stop()
    print_state("After stop")
    print("Queue stopped.")
