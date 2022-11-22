import utm
import numpy as np


# Without a reference/origin x, y
def convert_latlng2xy(lat, lng):
    u = utm.from_latlon(lat, lng)
    x = u[0]
    y = u[1]
    return x, y


# Convert back to lng lat so it can be used in mission planner
def convert_xy2latlng(x_drone_new, y_drone_new, lat_ref, lng_ref):
    u_o = utm.from_latlon(lat_ref, lng_ref)  # Use lat and lng coordinates to get the right zone and letter
    zone_nr = u_o[2]
    zone_ltr = u_o[3]
    lat, lng = utm.conversion.to_latlon(x_drone_new, y_drone_new, zone_nr, zone_ltr)
    return lat, lng


# perform the rotation from 0 deg, depending on angle
def rotate_x_y(x_line, y_line, deg):

    r = np.sqrt(x_line*x_line + y_line*y_line)
    x_line = r * np.sin(np.deg2rad(deg))
    y_line = r * np.cos(np.deg2rad(deg))

    return x_line, y_line


# All encompassing function
def update_lat_lon_along_circle(lat, lng, lat_circle_center, lng_circle_center, deg):

    x_drone, y_drone = convert_latlng2xy(lat, lng)
    x_circlecenter, y_circlecenter = convert_latlng2xy(lat_circle_center, lng_circle_center)

    x_drone_wrt_circle_center = x_drone - x_circlecenter
    y_drone_wrt_circlecenter = y_drone - y_circlecenter

    x_drone_wrt_circle_center, y_drone_wrt_circlecenter = rotate_x_y(x_drone_wrt_circle_center, y_drone_wrt_circlecenter, deg)

    x_drone_new = x_drone_wrt_circle_center + x_circlecenter
    y_drone_new = y_drone_wrt_circlecenter + y_circlecenter

    lat, lng = convert_xy2latlng(x_drone_new, y_drone_new, lat_circle_center, lng_circle_center)

    return lat, lng
