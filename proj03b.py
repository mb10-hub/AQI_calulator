"""
Program: CS115 Project 3
Author: Marco Barragan
Description: *** TBD ***
"""


def get_concentration(m):
    """Prompts the user for the reading from monitor m, then returns
    the concentration as an integer or float, rounding it according to the
    following conventions:
        PM-2.5: round to 1 decimal place (ug/m3)
        PM-10: round to integer (ug/m3)
        NO2: round to integer (ppb)
        SO2: round to integer (ppb)
        CO: round to 1 decimal place (ppm)
        O3: round to integer (ppb)

    Args:
        m (str): The type of monitor.

    Returns:
        int or float: The concentration.
    """

    a = float(input('    -> ' + m + ': '))
    if a == -1:
        return -1
    if m == 'PM-2.5 [ug/m3, 24-hr avg]' or m == 'CO [ppm, 8-hr avg]':
        a = round(float(a), 1)
    else:
        a = int(a)

    return a


def get_per_pollutant_index(breakpoints, monitors, m, c):
    """Generates the per-pollutant index using the AQI formula for
    the concentration 'c' associated with pollutant monitor 'm'. The
    calculation makes use of the EPA breakpoint table. If the concentration
    is out of range or should be ignored, returns -1; otherwise, returns
    the index that was calculated.

    Each row of 'breakpoints' has the following format:
       [category, [index_low, index_high], p_bounds_list]
    Where p_bounds_list is a 2D list of pollution concentration bounds; each
    row holds the bounds [c_low, c_high] for a particular monitor.

    Args:
        breakpoints (list):  A list of rows comprising the EPA breakpoint table.
        monitors (list): A list of monitors in the same order as p_bounds_list.
        c (str): The monitor originating the concentration.
        c (float or int): The concentration.

    Returns:
        int: The per-pollutant index or -1
    """
    i_min = -1
    i_max = -1
    con_min = -1
    con_max = -1

    for i in range(len(monitors)):
        if monitors[i] == m:
            x = i

    for j in range(len(breakpoints)):
        c = float(c)
        if breakpoints[j][2][x][0] <= c <= breakpoints[j][2][x][1]:
            i_min = breakpoints[j][1][0]
            i_max = breakpoints[j][1][1]
            con_min = breakpoints[j][2][x][0]
            con_max = breakpoints[j][2][x][1]
    if i_min == -1 and i_max == -1 and con_min == -1 and con_max == -1:
        return -1
    if 0 < c < 1:
        return 0
    ans = round((i_max - i_min) / (con_max - con_min) * (c - con_min) + i_min)
    return ans


def per_pollutant_concentration(m):
    """This function turns the list of concentrations into strings so that we can print them out
    Args:
        m : is the concentration m from the list of concentrations.
    returns:
        str: the concentration m in monitors.
    """
    concentrations = m
    concentrations_s = ''
    for concentration in concentrations:
        concentration = str(concentration)
        concentrations_s = ''
        concentrations_s += concentration
    return concentrations_s


def summary_report(l):
    """This function turns the pm25_readings list and turns it into a string then it calculates the average of the
    overall average of pm25_readings.
    args:
        l: list of all pm25_readings
    returns:
        float: average pm25_readings.
    """
    pm25_readings = l
    if pm25_readings == []:
        return 'No Data'
    else:
        total_readings = 0
        for readings in pm25_readings:
            total_readings += readings
        return total_readings / len(pm25_readings)

def get_condition(aqi):
    """This function gets the correct condition type by checking the AQI
    args: an int
    returns:
        str: condition type
    """
    aqi = int(aqi)
    if 0 <= aqi <= 50:
        return 'Good'
    elif 51 <= aqi <= 100:
        return 'Moderate'
    elif 101 <= aqi <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif 151 <= aqi <= 200:
        return 'Unhealthy'
    elif 201 <= aqi <= 300:
        return 'Very Unhealthy'
    elif 301 <= aqi <= 500:
        return'Hazardous'

def main():
    # The monitors that measure different pollutant concentrations
    monitors = ['PM-2.5 [ug/m3, 24-hr avg]', 'PM-10 [ug/m3, 24-hr avg]',
                'NO2 [ppb, 1-hr avg]', 'SO2 [ppb, 1-hr avg]', 'CO [ppm, 8-hr avg]',
                'O3 [ppb, 8-hr avg]', 'O3 [ppb, 1-hr avg]']

    ignore = [float('inf'), float('-inf')]

    # EPA breakpoint table.
    # Every row looks like:
    #   ['Condition', AQI-bound, [
    #      PM-2.5-bound,   PM-10-bound,    NO2-bound,
    #      SO2-bound,      CO-bound,       O3-8-hr-bound,  O3-1-hr-bound
    #    ]]
    epa_table = [
        ['Good', [0, 50], [
            [0, 12.0], [0, 54], [0, 53],
            [0, 35], [0, 4.4], [0, 54], ignore
        ]],
        ['Moderate', [51, 100], [
            [12.1, 35.4], [55, 154], [54, 100],
            [36, 75], [4.5, 9.4], [55, 70], ignore
        ]],
        ['Unhealthy for Sensitive Groups', [101, 150], [
            [35.5, 55.4], [155, 254], [101, 360],
            [76, 185], [9.5, 12.4], [71, 85], [125, 164]
        ]],
        ['Unhealthy', [151, 200], [
            [55.5, 150.4], [255, 354], [361, 649],
            [186, 304], [12.5, 15.4], [86, 105], [165, 204]
        ]],
        ['Very Unhealthy', [201, 300], [
            [150.5, 250.4], [355, 424], [650, 1249],
            [305, 604], [15.5, 30.4], [106, 200], [205, 404]
        ]],
        ['Hazardous', [301, 500], [
            [250.5, 500.4], [425, 604], [1250, 2049],
            [605, 1004], [30.5, 50.4], ignore, [405, 604]
        ]]
    ]

    locations = []  # all locations
    aqi_indices = []  # the AQI reading for each location
    pm25_readings = []  # all PM-2.5 readings

    con_maxt = []
    print('=== Air Quality Index (AQI) Calculator ===')

    loc = input('\nEnter name of ** Location **: ')
    max_location = 0
    min_location = 1000000

    while loc != '':
        locations.append(loc)

        concentrations = []  # monitor readings for loc
        ppi = []  # per-pollutant indices for loc

        for m in monitors:
            c = get_concentration(m)
            concentrations.append(c)

            index = get_per_pollutant_index(epa_table, monitors, m, c)
            ppi.append(index)

            # TODO (Final Code): print the per-pollutant concentration (write a new function)

            con_names = ['PM-2.5 ', 'PM-10 ', 'NO2 ', 'SO2', 'CO ', 'O3 ', 'O3 ']
            for i in range(len(monitors)):
                if monitors[i] == m:
                    con_names_r = ''
                    con_names_r = str(con_names[i])

            concentration = per_pollutant_concentration(concentrations)
            if c != -1 and index != -1:
                print('      ', con_names_r, 'concentration', concentration, 'yields', index, 'index')

            if 'PM-2.5' in m and index != -1:
                pm25_readings.append(c)

            if index > max_location:
                max_location = index
                max_location_s = loc

            if index != -1 and index != 0:
                if index < min_location:
                    min_location = index
                    min_location_s = loc


        aqi = max(ppi)  # TODO (Part A): calculate AQI
        aqi_indices.append(aqi)

        # TODO (Final Code): print both the aqi and condition

        s_aqi1 = max(aqi_indices)
        min_location = s_aqi1
        condition_type = get_condition(s_aqi1)
        print('    AQI for', loc, 'is ', s_aqi1)
        print('    Condition:', condition_type)
        con_maxt.append(s_aqi1) # put all the max AQI in a list for later use
        aqi_indices = []  # reset the list for every location
        loc = input('\nEnter name of ** Location **: ')



    # TODO (Final Code): print the summary report (write a new function)
    max_cont = max(con_maxt)
    min_cont = min(con_maxt)

    print()
    print('Summary Report')
    print('\t', ' Location with max AQI is ', max_location_s, ' (', max_cont, ')', sep='')
    print('\t', ' Location with min AQI is ', min_location_s, ' (', min_cont, ')', sep='')
    print('\t', 'Avg PM-2.5 concentration reading:', round(summary_report(pm25_readings), 1))

main()