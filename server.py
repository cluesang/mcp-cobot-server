# server.py
import sys
from mcp.server.fastmcp import Context, FastMCP
from pymycobot.mycobot280 import MyCobot280
from command_queue import CommandQueue

work_queue = CommandQueue()

# Create a named server
mcp = FastMCP("Cobot")
mc = MyCobot280("/dev/tty.usbserial-588D0016561", 115200)
home_angles = [0,0,0,0,0,0]

work_queue.add_command(mc.)

@mcp.tool()
def get_angles() -> str:
    """Get the current angle of each servo."""
    angles = mc.get_angles()
    return ", ".join([str(angle) for angle in angles])

@mcp.tool()
def move_angle(servo_id: int, angle: float, speed: int) -> str:
    """Move one joint of the cobot by selecting the servo id and target angle."""
    mc.send_angle(servo_id, angle, speed)
    return f"OK"

@mcp.tool()
def move_angles(angles: list[float], speed: int) -> str:
    """Move all joints of the cobot by sending angles to all the servos."""
    mc.send_angles(angles,speed)
    work_queue.add_command(lambda mc_obj, angles: mc.send_angles(angles,speed), mc, [0,0,0,0,0,0])
    return f"OK"

@mcp.tool()
def go_home(speed: int) -> str:
    """Move the servos to a home position for all joints of the cobot by sending angles to all the servos."""
    mc.send_angles(home_angles,speed)
    return f"OK"

@mcp.tool()
def set_home(speed: int) -> str:
    """Use the current servo angles to set as home position for all joints of the cobot."""
    home_angles = mc.get_angles()
    return f"OK"

@mcp.tool()
def change_color(r: int, g: int, b: int) -> str:
    """Change the LED Matric color"""
    result = mc.set_color(r,g,b)
    print(result)
    return f"{result}"

@mcp.tool()
def relax() -> str:
    """Release all robot arms"""
    result = mc.release_all_servos()
    print(result)
    return f"{result}"


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


if __name__ == "__main__":
    mc.send_angles(home_angles,50)
    mc.close()