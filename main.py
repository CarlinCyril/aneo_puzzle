import sys
import math
from typing import List


def err(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def to_km(meters: int) -> float:
    return meters / 1000


def to_hours(seconds: int) -> float:
    return seconds / 3600


def to_km_hr(mps: int) -> float:
    err("mps = {}".format(mps))
    return math.floor(mps * 3.6)


def to_mps(kmh: int) -> float:
    res = "{:.6f}".format((kmh / 3.6))
    return float(res)


class Interval:
    def __init__(self, lower: float, upper: float) -> None:
        self.lower = lower
        self.upper = upper
    
    def intersect(self, interval: ()) -> ():
        assert isinstance(interval, Interval)
        if self._overlap(interval):
            return Interval(max(self.lower, interval.lower),
                min(self.upper, interval.upper))
        else:
            return Interval(0, 0)
    
    def _overlap(self, interval) -> float:
        assert isinstance(interval, Interval)
        res = max(0, min(self.upper, interval.upper) - max(self.lower, interval.lower))
        #err("Overlap? {}".format(res))
        return max(0, min(self.upper, interval.upper) - max(self.lower, interval.lower))
    
    def __repr__(self) -> str:
        return "[{}, {}]".format(self.lower, self.upper)


class Stoplight:
    def __init__(self, distance: int, duration: int) -> None:
        self.distance = distance
        self.duration = duration
    
    def can_pass(self, speed: int) -> bool:
        res = round(self.distance / speed) // self.duration % 2 == 0
        #err("Can pass? {}".format(res))
        return res 
    
    def max_speed(self, speed_limit: int) -> Interval:
        cycle_number = round(self.distance / speed_limit) // self.duration
        #err("Cycle = {}".format(cycle_number))
        padding = 0 if (cycle_number % 2 == 0) else 1
        
        min_time_to_light = self.duration * (cycle_number + padding)
        max_time_to_light = self.duration * (cycle_number + 1 + padding) - 1
        #err("Min time = {}".format(min_time_to_light))
        #err("Max time = {}".format(max_time_to_light))
        
        min_speed = self.distance / max_time_to_light
        max_speed = self.distance / min_time_to_light if min_time_to_light > 0 else speed_limit
        
        return Interval(min_speed, max_speed)
    
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
        for sl in self.list_stoplights:
            err("Stoplight:\n{}".format(sl))
            #pass

        interval_speeds = list(map(lambda x: x.max_speed(self.speed_limit), self.list_stoplights))
        err("Speeds = {}".format(list(interval_speeds)))

        best_interval = Interval(0, self.speed_limit)
        for interval in interval_speeds:
            new_interval = best_interval.intersect(interval)
            if new_interval.upper:
                best_interval = new_interval
            else:
                Interval(0, min(best_interval.upper, interval.upper))
                break

        optimized_speed = best_interval.upper if best_interval.upper \
            else interval_speeds[0].upper
        err("Best speed bisous = {}".format(optimized_speed))
        # return optimized_speed

        err(list(map(lambda x: x.can_pass(optimized_speed), self.list_stoplights)))

        counter = 0

        while counter < 50 and not all(map(lambda x: x.can_pass(optimized_speed), self.list_stoplights)):
            err("~~~~~~~~~~~~~~~~~~~~~~~~~~")
            counter += 1
            self.speed_limit = optimized_speed
            interval_speeds = list(map(lambda x: x.max_speed(self.speed_limit), self.list_stoplights))
            err("Speeds = {}".format(list(interval_speeds)))

            best_interval = Interval(0, self.speed_limit)
            for interval in interval_speeds:
                new_interval = best_interval.intersect(interval)
                #err("New interval = {}".format(new_interval))
                #err("Best interval = {}".format(best_interval))
                #err("Current interval = {}".format(interval))
                if new_interval.upper:
                    best_interval = new_interval
                else:
                    err("Best interval = {}".format(best_interval))
                    err("Current interval bisous = {}".format(interval))
                    best_interval = Interval(0, min(best_interval.upper, interval.upper))
                    break

            optimized_speed = best_interval.upper
            err("Best speed = {}".format(optimized_speed))
        return optimized_speed


road = Road()
road.parse()
result = road.get_optimized_speed()

print(to_km_hr(result))
