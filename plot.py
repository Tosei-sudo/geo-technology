
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

def are_points_inside_polygon_index(point, polygon_index):
    return (point[0] >= polygon_index[0][0] and point[0] <= polygon_index[1][0] and point[1] >= polygon_index[0][1] and point[1] <= polygon_index[1][1])

def are_points_inside_polygon(point, polygon):
    
    num = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    x, y = point
    for i in range(1, num + 1):
        p2x, p2y = polygon[i % num]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x) and p1y != p2y:
            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if x <= xinters:
                inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def create_polygon_index(polygon):
    # return circumscription rectangle np array
    polygon_index = np.array([np.min(polygon, axis=0), np.max(polygon, axis=0)])

    return polygon_index

def get_center_point_by_polygon(polygon):
    x, y = zip(*polygon)
    return np.array([np.mean(x), np.mean(y)])

# pol = np.array([[0,0], [1.5,1], [1.5,2], [0,1] ,[0,0]])
# plt.plot(pol[:,0], pol[:,1], "r-")

import json

with open('prefectures.geojson') as f:
    data = json.load(f)
    
prefectures = []

features = data['features']

for feature in features:
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    properties = feature['properties']
    
    if geometry['type'] == 'Polygon':
        for polygon in coordinates:
            
            polygon_index = create_polygon_index(polygon)
            
            prefectures.append((polygon_index, polygon, properties))
            
            x, y = zip(*polygon)
            plt.plot(x, y, "b-")
            
            polygon_index_polygon = [polygon_index[0], [polygon_index[1][0], polygon_index[0][1]], polygon_index[1], [polygon_index[0][0], polygon_index[1][1]], polygon_index[0]]
            x, y = zip(*polygon_index_polygon)
            plt.plot(x, y, "y-")
                
            plt.plot(center[0], center[1], "y^")
            
    elif geometry['type'] == 'MultiPolygon':
        for polygons in coordinates:
            for polygon in polygons:
                
                polygon_index = create_polygon_index(polygon)
                center =  get_center_point_by_polygon(polygon)
                
                prefectures.append((polygon_index, polygon, properties, center))
                
                x, y = zip(*polygon)
                plt.plot(x, y, "b-")
                
                polygon_index_polygon = [polygon_index[0], [polygon_index[1][0], polygon_index[0][1]], polygon_index[1], [polygon_index[0][0], polygon_index[1][1]], polygon_index[0]]
                x, y = zip(*polygon_index_polygon)
                plt.plot(x, y, "y-")
                
                plt.plot(center[0], center[1], "y^")

points = []

random_seeds = np.random.rand(100, 2)
for seed in random_seeds:
    point = [120 + (30 * seed[0]), 25 + (20 * seed[1])]
    points.append(point)

cnt = 0

for point in points:
    flag = False
    min_distance = 100000000
    min_distance_prefecture = ""
    min_distance_center = []
    
    for polygon_index, polygon, properties, center in prefectures:
        if are_points_inside_polygon_index(point, polygon_index):
            if are_points_inside_polygon(point, polygon):
                flag = True
                break
        else:
            flag = False
            distance = np.linalg.norm(point - center)
            if min_distance > distance:
                min_distance = distance
                min_distance_prefecture = properties['name'] + u"付近"
                min_distance_center = center
    if flag:
        print str(properties['name'].encode('utf-8')).decode('utf-8')
        
        plt.plot(point[0], point[1], "ro")
    else:
        print str(min_distance_prefecture.encode('utf-8')).decode('utf-8')
        plt.plot([point[0], min_distance_center[0]], [point[1], min_distance_center[1]], "y-")
        plt.plot(point[0], point[1], "go")

plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Point in Polygon Test")
plt.grid(True)
plt.show()
