import math
from typing import Tuple, List

def dist_of_2_points(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def verify_points(data: Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]) -> bool:
    if len(data[0]) != len(data[1]):
        return False
    dists = []
    for i in range(len(data[0])):
        p1 = data[0][i]
        p2 = data[1][i]
        dists.append(dist_of_2_points(p1, p2))
    avg_dist = sum(dists)/len(dists)
    for dist in dists:
        if abs(dist-avg_dist) > avg_dist*0.05:
            return False
    return True

def sort_points(keypoints) -> Tuple:
    points = []
    for point in keypoints:
        points.append((point.pt[0], point.pt[1]))
    points.sort(key=lambda x: x[0])
    return tuple(points)

def ensure_count(keypoints, wanted) -> bool:
    if len(keypoints) > wanted:
        print(f"too many points {len(keypoints)}")
        return False
    if len(keypoints) < wanted:
        print(f"not enough points {len(keypoints)}")
        return False
    return True

class MovingAveragePoint:
    def __init__(self, entries) -> None:
        self.entries = entries
        self.points = []

    def add_point(self, point):
        self.points.append(point)
        if len(self.points) > self.entries:
            self.points.pop(0)

    def get_average(self):
        return (sum([x[0] for x in self.points])/len(self.points), sum([x[1] for x in self.points])/len(self.points))

    def get_average_int(self):
        return (int(sum([x[0] for x in self.points])/len(self.points)), int(sum([x[1] for x in self.points])/len(self.points)))

    def debounce(self, point):
        if abs(point[0] - self.points[-1][0]) < 0.01 and abs(point[1] - self.points[-1][1]) < 0.01:
            return True
        return False

    def clear(self):
        self.points = []

    def samples(self):
        return len(self.points)

# def normalize_point(point: tuple[int, int]) -> tuple[float, float]:
#     return (point[0]/SCREEN_WIDTH_PX, point[1]/SCREEN_HEIGHT_PX)
# def normalize_points(points: tuple[tuple[int, int]]) -> tuple[tuple[float, float]]:
#     return tuple([normalize_point(point) for point in points])