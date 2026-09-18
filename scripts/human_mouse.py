import math
import pyautogui
import time

pyautogui.FAILSAFE = False


class HumanMouse:
    @staticmethod
    def move_to(loc, x_off=0, y_off=0):
        pyautogui.moveTo(loc, duration=0.1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveRel(x_off, y_off, duration=0.05, tween=pyautogui.easeInOutQuad)

    @staticmethod
    def click():
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.mouseUp()
        time.sleep(0.05)

    @staticmethod
    def locate_on_screen(template_path, confidence=0.8, region=None):
        return pyautogui.locateCenterOnScreen(
            template_path, confidence=confidence, region=region
        )

    @staticmethod
    def locate_all_on_screen(template_path, min_distance=60, confidence=0.8, region=None):
        matches = list(pyautogui.locateAllOnScreen(
            template_path, confidence=confidence, region=region
        ))
        centers = [pyautogui.center(match) for match in matches]
        unique_centers = []

        for center in centers:
            if all(math.dist(center, existing) > min_distance
                   for existing in unique_centers):
                unique_centers.append(center)

        return unique_centers

    @staticmethod
    def smooth_drag(start_pos, offset_x, offset_y):
        x_start, y_start = start_pos
        x_end = x_start + offset_x
        y_end = y_start + offset_y

        pyautogui.moveTo(x_start, y_start, duration=0.01, tween=pyautogui.easeInOutQuad)
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.moveTo(x_end, y_end, duration=0.01, tween=pyautogui.easeInOutQuad)
        pyautogui.mouseUp()

    @staticmethod
    def smooth_drag_to(start_pos, end_pos):
        x_start, y_start = start_pos
        x_end, y_end = end_pos

        pyautogui.moveTo(x_start, y_start, duration=0.01, tween=pyautogui.easeInOutQuad)
        pyautogui.mouseDown()
        time.sleep(0.01)
        pyautogui.moveTo(x_end, y_end, duration=0.01, tween=pyautogui.easeInOutQuad)
        pyautogui.mouseUp()
