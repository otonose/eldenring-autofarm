import keyboard
import time
from PySide6.QtWidgets import QApplication


def start_timer(int):
    for i in reversed(range(int)):
        print(i + 1)
        time.sleep(1)
    print("start!")


class Shell:
    def __init__(self):
        pass

    def register_callback(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func()
        count = 0
        while input("start or stop:") == "start":
            count += 1
            self.func(*self.args, **self.kwargs)
        print("shell stopped")
        print(f"called {count}")


class Player:
    def __init__(self):
        self.is_alive = False
        keyboard.add_hotkey("f1", self.kill)
        self.move_direction_mapping = {
            "left": "a",
            "right": "d",
            "forward": "w",
            "backward": "s",
        }
        self.rotate_direction_mapping = {
            "left": "j",
            "right": "l",
            "up": "i",
            "down": "k",
        }

    def kill(self):
        print("player is killed")
        self.is_alive = False

    def press_until(self, key: str, duration: int):
        if duration > 0:
            keyboard.press(key)
            time.sleep(duration)
            keyboard.release(key)
        else:
            self.press(key)

    def press(self, key: str):
        self.press_until(key, 0.15)

    def move(self, direction: str, duration: int):
        key = self.move_direction_mapping[direction]
        self.press_until(key, duration)

    def rotate(self, direction: str, duration: int):
        key = self.rotate_direction_mapping[direction]
        self.press_until(key, duration)

    # Move methods
    def move_left(self, duration: int):
        self.move("left", duration)

    def move_right(self, duration: int):
        self.move("right", duration)

    def move_forward(self, duration: int):
        self.move("forward", duration)

    def move_backward(self, duration: int):
        self.move("backward", duration)

    # Rotate methods
    def rotate_left(self, duration: int):
        self.rotate("left", duration)

    def rotate_right(self, duration: int):
        self.rotate("right", duration)

    def rotate_up(self, duration: int):
        self.rotate("up", duration)

    def rotate_down(self, duration: int):
        self.rotate("down", duration)

    # Preset methods
    def preset_morg(self):
        # Go to position
        self.move_forward(2.65)
        self.rotate_left(0.24)
        self.move_forward(2.3)

        # Use skill and wait for delay
        self.press("f")
        time.sleep(5)

        # Go to spawn
        self.press("g")
        time.sleep(0.4)
        self.press("f")
        time.sleep(0.4)
        self.press("e")
        time.sleep(0.4)
        self.press("e")

        # Wait for loading
        time.sleep(6)

    def farm(self, preset):
        ans = input("money before: ")
        money_before = int(ans)

        print("----------------")
        print("go back to game screen")
        time.sleep(2)
        start_timer(3)

        self.is_alive = True
        count = 0

        t1 = time.time()
        while self.is_alive:
            preset()
            count += 1
        print("stopped!")
        print("----------------")

        if not count:
            print("there was no try")
            return

        t2 = time.time()
        td = t2 - t1
        print(f"tried: {count}")
        print(f"time took: {td:.2f} sec(s)")
        ans = input("money after: ")
        money_after = int(ans)
        earned = money_after - money_before
        print(f"you earned: {earned}")
        print(f"money per count: {earned / count:.2f}")
        print(f"money per second: {earned / td:.2f}")

    def farm_morg(self):
        self.farm(self.preset_morg)


if __name__ == "__main__":
    shell = Shell()
    player = Player()
    shell.register_callback(player.farm_morg)
    shell.run()
