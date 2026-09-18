import math
import os
import random
import time
from dataclasses import dataclass

from human_mouse import HumanMouse


@dataclass(frozen=True)
class EnvironmentTarget:
    x: int
    y: int
    kind: str
    confidence: float


class EnvironmentScanner:
    """Find encounter objects without knowing which Miscrit will spawn."""

    def __init__(
        self,
        templates=None,
        confidence=0.72,
        min_distance=55,
        scan_region=(0, 0, 1366, 670),
        encounter_timeout=8.0,
    ):
        self.templates = templates or {
            "tree": [
                "templates/environment/tree_01.jpg",
                "templates/environment/tree_02.jpg",
            ],
            "grass": [
                "templates/environment/grass_01.jpg",
                "templates/environment/grass_02.jpg",
            ],
        }
        self.confidence = confidence
        self.min_distance = min_distance
        self.scan_region = scan_region
        self.encounter_timeout = encounter_timeout
        self.visited = []

    def scan(self):
        found = []

        for kind, paths in self.templates.items():
            for path in paths:
                if not os.path.exists(path):
                    print(f"[SCAN] Missing template: {path}")
                    continue

                try:
                    matches = HumanMouse.locate_all_on_screen(
                        path,
                        min_distance=self.min_distance,
                        confidence=self.confidence,
                        region=self.scan_region,
                    )
                except Exception as exc:
                    print(f"[SCAN] Template error for {path}: {exc}")
                    continue

                for point in matches:
                    found.append(
                        EnvironmentTarget(
                            int(point[0]),
                            int(point[1]),
                            kind,
                            self.confidence,
                        )
                    )

        unique = []
        for target in found:
            if all(
                math.dist((target.x, target.y), (other.x, other.y))
                > self.min_distance
                for other in unique
            ):
                unique.append(target)

        print(f"[SCAN] Found {len(unique)} environment targets.")
        return unique

    def _was_visited(self, target):
        return any(
            math.dist((target.x, target.y), point) <= self.min_distance
            for point in self.visited
        )

    def next_target(self):
        targets = self.scan()
        candidates = [target for target in targets if not self._was_visited(target)]

        if not candidates and targets:
            print("[SCAN] All visible targets checked; resetting scan cycle.")
            self.visited.clear()
            candidates = targets

        if not candidates:
            return None

        cx = self.scan_region[0] + self.scan_region[2] / 2
        cy = self.scan_region[1] + self.scan_region[3] / 2

        target = min(
            candidates,
            key=lambda item: math.dist((item.x, item.y), (cx, cy)),
        )

        self.visited.append((target.x, target.y))
        print(f"[SCAN] Selected {target.kind} at ({target.x}, {target.y}).")
        return target

    def interact(self, target):
        """Interact with a map object and wait for a battle/search UI."""
        HumanMouse.move_to(
            (target.x, target.y),
            random.randint(-4, 4),
            random.randint(-4, 4),
        )
        HumanMouse.click()

        print(f"[SCAN] Interacted with {target.kind}; waiting for encounter...")

        deadline = time.time() + self.encounter_timeout

        while time.time() < deadline:
            try:
                search = HumanMouse.locate_on_screen(
                    "photos/fight/common/search_for_miscrit.png",
                    0.78,
                )
                if search:
                    HumanMouse.move_to(search, 0, 0)
                    HumanMouse.click()
                    print("[SCAN] Search-for-Miscrit prompt clicked.")
                    time.sleep(1.2)
                    return True

                for path in (
                    "photos/fight/common/items.png",
                    "photos/fight/common/capture.png",
                ):
                    if HumanMouse.locate_on_screen(path, 0.78):
                        print(f"[SCAN] Battle UI detected via {path}.")
                        return True

            except Exception as exc:
                print(f"[SCAN] Encounter detection error: {exc}")
                return False

            time.sleep(0.2)

        print("[SCAN] No encounter detected; trying another object.")
        return False
