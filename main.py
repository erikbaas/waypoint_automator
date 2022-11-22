#!/usr/bin/env python
# -- coding: utf-8 --

"""
*******************************************************************
  WAYPOINT GENERATOR

  Copyright (c) 2022, Aerospace Engineering, TU Delft & Royal NLR.
  All rights reserved. This program and the accompanying materials
  are meant solely for educative purposes.
  Author: Erik van Baasbank @erikbaas

  This program is meant to automate changes to the .waypoints files.
  In this case, the waypoints are moved along a circle, and the
  heading is changed accordingly. The only thing incremented is deg.
*******************************************************************
"""


from utility_functions import *


# Adjust the waypoints file
def adjust_waypoints_file(filename_, deg):
    with open(filename_) as f:

        # Add file-format information to the output file
        output = 'QGC WPL 110\n'

        # Adjust lines from input file and add back to output
        for i, line in enumerate(f):
            if i == 0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                lines = line.split('\t')

                real_lines = lines  # replace by real_lines = lines[0].split() if you using Python 2.7 (for eg dronekit)

                # EXTRACT FROM WAYPOINTS IN FILE
                ln_index = int(real_lines[0])
                ln_currentwp = int(real_lines[1])
                ln_frame = int(real_lines[2])
                ln_command = int(real_lines[3])
                ln_param1 = float(real_lines[4])
                ln_param2 = float(real_lines[5])
                ln_param3 = float(real_lines[6])
                ln_param4 = float(real_lines[7])
                ln_param5 = float(real_lines[8])
                ln_param6 = float(real_lines[9])
                ln_param7 = float(real_lines[10])
                ln_autocontinue = int(real_lines[11].strip())

                # # ################# ALTER STUFF HERE #####################
                # note that indexes start at 1 (because 0 represents H)

                # Retrieve the circle center from the center of the circle
                if ln_index == 1:
                    lat_circlecenter, lng_circlecenter = ln_param5, ln_param6

                # Adjust waypoint 3's location
                if ln_index == 3:
                    lat, lng = ln_param5, ln_param6
                    lat, lng = update_lat_lon_along_circle(lat, lng, lat_circlecenter, lng_circlecenter, deg)
                    ln_param5, ln_param6 = lat, lng

                # Adjust the CONDITION_YAW degree
                if ln_index == 2:
                    ln_param1 += deg

                if ln_index == 4:
                    ln_param1 += deg

                #
                # ##############################################################

                # PASTE BACK TO TXT FILE
                commandline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    ln_index, ln_currentwp, ln_frame, ln_command,
                    ln_param1, ln_param2, ln_param3, ln_param4,
                    ln_param5, ln_param6, ln_param7, ln_autocontinue)

                output += commandline
    return output


if __name__ == "__main__":

    # 1) Set how you want to automate the file writing
    min_degree = 0
    max_degree = 360
    increment = 10

    # 2) Select the file you want to work from
    filename = "waypoints_in/120m_wind0deg.waypoints"

    # 3) Per degree, make adjustments and save
    for deg in range(min_degree, max_degree, increment):

        output = adjust_waypoints_file(filename, deg)

        filename_out = f"waypoints_out/120m_wind{deg}deg.waypoints"
        with open(filename_out, 'w') as file_:
            file_.write(output)
            print(f"Mission written: {filename_out}")



