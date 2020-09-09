import sys
import math


def err(message) -> None:
    print(message, file=sys.stderr, flush=True)


def to_km(meters: int) -> float:
    return meters / 1000


def to_hours(seconds: int) -> float:
    return seconds / 3600


def to_km_hr(mps: float) -> float:
    err("mps = {}".format(mps))
    return math.floor(round(mps * 3.6, 5))


def to_mps(kmh: float) -> float:
    return kmh / 3.6


class Interval:
    def __init__(self, lower: float, upper: float) -> None:
        assert lower <= upper
        self.lower = lower
        self.upper = upper

    def intersect(self, interval: ()) -> ():
        assert isinstance(interval, Interval)
        if self._overlap(interval):
            return Interval(max(self.lower, interval.lower),
                            min(self.upper, interval.upper))
        else:
            return Interval(0, 0)

    def __eq__(self, other):
        assert isinstance(other, Interval)
        return self.lower == other.lower and self.upper == other.upper

    def _overlap(self, interval) -> float:
        assert isinstance(interval, Interval)
        res = max(0, min(self.upper, interval.upper) - max(self.lower, interval.lower))
        # err("Overlap? {}".format(res))
        return max(0, min(self.upper, interval.upper) - max(self.lower, interval.lower))

    def __repr__(self) -> str:
        return "[{}, {}]".format(self.lower, self.upper)


class Stoplight:
    def __init__(self, distance: int, duration: int) -> None:
        self.distance = distance
        self.duration = duration

    def can_pass(self, speed: int) -> bool:
        speed = to_mps(to_km_hr(speed))
        cycle_number = round(self.distance / speed, 5) // self.duration
        res = cycle_number % 2 == 0
        return res

    def best_speed_interval(self, speed_limit: int) -> Interval:
        cycle_number = round(self.distance / speed_limit, 5) // self.duration
        # err("Cycle = {}".format(cycle_number))
        padding = 0 if self.can_pass(speed_limit) else 1

        min_time_to_light = self.duration * (cycle_number + padding)
        max_time_to_light = self.duration * (cycle_number + 1 + padding)
        # err("Min time = {}".format(min_time_to_light))
        # err("Max time = {}".format(max_time_to_light))

        min_speed = self.distance / max_time_to_light
        max_speed = self.distance / min_time_to_light if min_time_to_light > 0 else speed_limit

        return Interval(min_speed, min(max_speed, speed_limit))

    def __repr__(self) -> str:
        return "Distance: {} || Duration: {}".format(self.distance, self.duration)


class Road:
    def __init__(self) -> None:
        self.list_stoplights = list()
        self.speed_limit = 0

    def parse(self) -> None:
        self.speed_limit = int(input())
        self.speed_limit = to_mps(self.speed_limit)
        err("Speed limit = {}".format(self.speed_limit))

        light_count = int(input())

        for i in range(light_count):
            distance, duration = [int(j) for j in input().split()]
            self.list_stoplights.append(Stoplight(distance, duration))

    def get_optimized_speed(self) -> int:
        # for sl in self.list_stoplights:
        #     err("Stoplight:\n{}".format(sl))
        optimized_speed = self.speed_limit

        err(list(map(lambda x: x.can_pass(optimized_speed), self.list_stoplights)))

        while not all(map(lambda x: x.can_pass(optimized_speed), self.list_stoplights)):
            err("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            self.speed_limit = optimized_speed
            interval_speeds = list(map(lambda x: x.best_speed_interval(optimized_speed), self.list_stoplights))
            err("Speeds = {}".format(list(interval_speeds)))

            best_interval = Interval(0, optimized_speed)
            for interval in interval_speeds:
                new_interval = best_interval.intersect(interval)
                err("New interval = {}".format(new_interval))
                err("Best interval = {}".format(best_interval))
                err("Current interval = {}".format(interval))
                if new_interval.upper:
                    best_interval = new_interval
                else:
                    best_interval = Interval(0, min(best_interval.upper, interval.upper))
                    break

            optimized_speed = best_interval.upper
            err("Best speed = {}".format(optimized_speed))
            err(list(map(lambda x: x.can_pass(optimized_speed), self.list_stoplights)))
        return optimized_speed


road = Road()
road.parse()
result = road.get_optimized_speed()

print(to_km_hr(result))
