# server.py
import sys, time
from mcp.server.fastmcp import Context, FastMCP
from pymycobot.mycobot280 import MyCobot280
from command_queue import CommandQueue, task_one, task_two

# Create a named server
mcp = FastMCP("Cobot")
# mc = MyCobot280("/dev/tty.usbserial-588D0016561", 115200)
mc = MyCobot280("/dev/ttyACM0", 115200)
home_angles = [0,0,0,0,0,0]

work_queue = CommandQueue()

@mcp.tool()
def get_angles() -> str:
    """Get the current angle of each servo."""
    angles = mc.get_angles()
    return ", ".join([str(angle) for angle in angles])

@mcp.tool()
def move_angle(servo_id: int, angle: float, speed: int) -> str:
    """Move one joint of the cobot by selecting the servo id and target angle."""
    work_queue.add_command(mc.send_angle, servo_id, angle, speed)
    return f"OK"

@mcp.tool()
def move_angles(angles: list[float], speed: int) -> str:
    """Move all joints of the cobot by sending angles to all the servos."""
    work_queue.add_command(mc.send_angles, angles, speed)
    return f"OK"

@mcp.tool()
def go_home(speed: int) -> str:
    """Move the servos to a home position for all joints of the cobot by sending angles to all the servos."""
    work_queue.add_command(mc.send_angles, home_angles, speed)
    return f"OK"

@mcp.tool()
def set_home(speed: int) -> str:
    """Use the current servo angles to set as home position for all joints of the cobot."""
    global home_angles
    home_angles = mc.get_angles()
    return f"OK"

@mcp.tool()
def change_color(r: int, g: int, b: int) -> str:
    """Change the LED Matric color"""
    work_queue.add_command(mc.set_color, r, g, b)
    return f"OK"

@mcp.tool()
def relax() -> str:
    """Release all robot arms"""
    work_queue.add_command(mc.release_all_servos)
    return f"OK"


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    version = mc.get_system_version()
    basic_version = mc.get_basic_version()
    reboot_count = mc.get_reboot_count()
    return f"Hello, I'm cobot. \
            My version information is: {version}, {basic_version}, \
            rebooted {reboot_count} times!"

@mcp.tool()
def interpretive_dance_routine(description: str) -> str:
    """
    Perform an interpretive dance routine using creative joint angles and LED color changes.
    The routine is determined by the input description.
    """
    import time
    import hashlib
    import random

    # Use the description to seed the random generator deterministically
    seed = int(hashlib.sha256(description.encode('utf-8')).hexdigest(), 16) % (2**32)
    random.seed(seed)

    # Define dance moves as (angles, color) tuples
    dance_moves: list[tuple[list[int], tuple[int, int, int]]] = [
        ([0, 0, 0, 0, 0, 0], (255, 0, 0)),        # Center pose, Red
        ([90, -45, 60, -30, 45, 90], (0, 255, 0)), # Open arms, Green
        ([-90, 45, -60, 30, -45, -90], (0, 0, 255)), # Closed arms, Blue
        ([168, -135, 150, -145, 165, 180], (255, 255, 0)), # Max reach, Yellow
        ([-168, 135, -150, 145, -165, -180], (0, 255, 255)), # Min reach, Cyan
        ([0, 90, -90, 90, -90, 0], (255, 0, 255)), # Twisted pose, Magenta
    ]
    # Add a few random (but deterministic) freestyle moves
    for _ in range(3):
        angles = [random.randint(-168,168), random.randint(-135,135), random.randint(-150,150), random.randint(-145,145), random.randint(-165,165), random.randint(-180,180)]
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        dance_moves.append((angles, color))

    # Define speed pattern: fast, slow, fast, end slow
    num_moves = len(dance_moves)
    speeds = []
    for i in range(num_moves):
        if i == 0:
            speeds.append(random.randint(90, 100))  # Start fast
        elif i < num_moves // 2:
            speeds.append(random.randint(25, 35))   # Slow
        elif i < num_moves - 1:
            speeds.append(random.randint(90, 100))  # Fast again
        else:
            speeds.append(random.randint(25, 35))   # End slow

    for (angles, color), speed in zip(dance_moves, speeds):
        print(f"Moving to angles: {angles} with color: {color} at speed: {speed}")
        move_angles(angles, speed)
        change_color(*color)
        time.sleep(1.5)
    # End with a bow
    final_speed = speeds[-1]
    move_angles([0, -90, 90, 0, 0, 0], final_speed)
    change_color(128, 0, 128)  # Purple
    time.sleep(2)
    print("Dance routine complete!")
    return "Dance routine complete!"

if __name__ == "__main__":
    print("Server started. Press Ctrl+C to stop.")
    while True:
        try:
            time.sleep(3)
            work_queue.add_command(mc.send_angles, [-10,10,-10,10,-10,10],50)
            work_queue.add_command(mc.send_angles, [10,-10,10,-10,10,-10],50)
        except KeyboardInterrupt:
            print("Server stopped by user.")
            work_queue.clear()
            work_queue.stop()
            break