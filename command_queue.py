import threading
import time
import logging
import sys
from collections import deque
from typing import Callable, Any, Deque, Tuple

LOG_FILE = 'mcp_work_queue_client.log'

# Configure logging to a file
# TODO: This doesn't seem to populate with all the log info we're looking for.
logging.basicConfig(
    level=logging.DEBUG,  # Adjust as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    filename=LOG_FILE,
    filemode='w'  # 'w' overwrites the file on each run, use 'a' to append
)

logger = logging.getLogger(__name__)


class CommandQueue:
    def __init__(self) -> None:
        self._queue: Deque[Tuple[Callable[..., Any], tuple, dict]] = deque()
        self._processing_thread: threading.Thread = threading.Thread(target=self._process_commands, daemon=True)
        self._paused: threading.Event = threading.Event()
        self._running: threading.Event = threading.Event()
        self._running.set()
        self._queue_lock: threading.Lock = threading.Lock()
        self._processing_thread.start()
        logger.info("CommandQueue initialized.")

    def add_command(self, command: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Adds a command and its parameters to the queue."""
        logger.info(f"Adding command: {command.__name__} with args: {args}, kwargs: {kwargs}")
        if not callable(command):
            logger.error(f"Tried to add a non-callable command: {command!r} (type: {type(command)})")
            return
        command_name = getattr(command, "__name__", repr(command))
        self._queue.append((command, args, kwargs))
        logger.debug(f"Command added: {command_name} with args: {args}, kwargs: {kwargs}")

    def pause(self) -> None:
        """Pauses the processing of commands."""
        self._paused.set()
        logger.info("Command queue processing paused.")

    def resume(self) -> None:
        """Resumes the processing of commands."""
        self._paused.clear()
        logger.info("Command queue processing resumed.")

    def clear(self) -> None:
        """Clears all commands from the queue and signals the processing thread."""
        with self._queue_lock:
            queue_size = len(self._queue)
            self._queue.clear()
        logger.info(f"Command queue cleared. {queue_size} commands removed.")
        self._paused.set()  # Briefly set the paused event to potentially unblock the worker
        self._paused.clear() # Then clear it to allow processing to continue

    def stop(self) -> None:
        """Stops the background processing thread."""
        self._running.clear()
        self._paused.set()  # Ensure the worker thread isn't blocked on pause
        self._processing_thread.join()
        logger.info("Command queue processing stopped.")

    def get_state(self) -> dict:
        """Returns the current state of the command queue."""
        return {
            'running': self._running.is_set(),
            'paused': self._paused.is_set(),
            'queue_length': len(self._queue)
        }

    def _process_commands(self) -> None:
        """Processes commands from the queue in a loop."""
        while self._running.is_set():
            if self._paused.is_set():
                self._paused.wait()  # Block until unpaused
            with self._queue_lock:
                if self._queue:
                    command, args, kwargs = self._queue.popleft()
                    logger.debug(f"Processing command: {command.__name__} with args: {args}, kwargs: {kwargs}")
                    try:
                        logger.info(f"Executing: {command.__name__}(*{args}, **{kwargs})")
                        command(*args, **kwargs)
                    except Exception as e:
                        logger.error(f"Error executing command {command.__name__}(*{args}, **{kwargs}): {e}", exc_info=True)
                else:
                    logger.debug("Command queue is empty.")
            time.sleep(0.1) # Don't hog the CPU

# Example usage (no changes needed here for the fix):
def task_one(message: str) -> None:
    time.sleep(1)
    logger.info(f"Task One: {message}")

def task_two(value: int, multiplier: int = 2) -> None:
    time.sleep(0.5)
    result = value * multiplier
    logger.info(f"Task Two: {value} * {multiplier} = {result}")

if __name__ == "__main__":
    work_queue = CommandQueue()

    work_queue.add_command(task_one, "Hello from task one!")
    work_queue.add_command(task_two, 5)
    work_queue.add_command(task_two, 10, multiplier=3)

    time.sleep(3)
    work_queue.pause()
    work_queue.add_command(task_one, "This won't be processed immediately.")
    time.sleep(2)
    work_queue.resume()
    time.sleep(3)
    work_queue.clear()
    work_queue.add_command(task_two, 7)
    time.sleep(2)
    work_queue.stop()

    logger.info("Done with the example.")