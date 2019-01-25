import json
from pprint import pprint

global_error_stack = []

def openJSON(fileName):
    with open('input/' + fileName) as data_file:
        data = json.load(data_file)
    return data

def writeJSON(data):
    # Print the file as a JSON.
    with open('output/data.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False
            , sort_keys=False, indent=4, separators=(',', ': '))

def formatTimes(stringTime):
    # Function input is a string with a format like this 'HH:MM[PM/AM]'.
    # Returns Time in 24h format wo PM or AM.
    result = 0.0
    timeSplited = stringTime.split(':');

    # Check for correct format.
    if (len(timeSplited) != 2):
        # Format is wrong
        global_error_stack.append("Wrong format for: formatTimes("
        + stringTime + ").")
        result = -1.0
        return result
    else:
        timeSuffix = timeSplited[1][2:]
        # If no time sufix provided it's assumed to be 24hs format.
        hours = ((float(timeSplited[0]) + 12) if timeSuffix == "PM"
            else float(timeSplited[0]))
        hours = 12.0 if hours == 24.0 else hours
        minutes = float(timeSplited[1][:2])
        minutes = (100.0 * minutes) / 6000.0    # divie 60 divide 100.

        result = hours + minutes

        # Check if time makes sence
        if (result < 0.0 or result > 24.0):
            global_error_stack.append("Wrong value for: formatTimes("
            + stringTime + ").")
            result = -1.0
        return result

def deFortmatTime(floatTime):
    # This function converts output of formatTimes() to original.
    result = ""
    timeSplited = str(floatTime).split('.');

    timeSuffix = ("PM" if float(timeSplited[0]) > 11
        else "AM")
    hours = ((float(timeSplited[0]) - 12) if timeSuffix == "PM"
        else float(timeSplited[0]))
    hours = 12.0 if hours == 0.0 else hours
    minutes = float(timeSplited[1])
    minutes = (minutes * 60.00) / 1000.00

    result = ("{:.2f}".format(hours + minutes) + timeSuffix).replace('.', ':')

    return str(result)

def isEmployeeAvailable(key, employee):
    # This function check if the employee is available at that time.
    available = False if (key in employee) else True

    return available

def main():
    # Variables
    data = openJSON("schedule.json")     # Data from json.
    staff = data["staff"]   # Staff schedulesself.
    availableTimes = {}

    # Build a schedule dictionary and fill it with the data.
    # Initialize some important values.
    startTime = formatTimes(data["WorkHours"]["start"])
    endTime = formatTimes(data["WorkHours"]["end"])
    lunchStart = formatTimes(data["Lunch"]["start"])
    lunchEnd = formatTimes(data["Lunch"]["end"])
    try:
        meetDuration = (float(data["MeetDuration"]) * 100.0) / 6000.0
    except ValueError:
        meetDuration = -1;

    # Check that all this values are correct.
    if (startTime < 0 or endTime < 0 or lunchStart < 0 or lunchEnd < 0):
        global_error_stack.append("Wrong value on JSON 'WorkHours' or 'Lunch'.")
        return 0
    elif (lunchStart > lunchEnd or startTime > endTime):
        global_error_stack.append("Start times must be lower than end times " +
            "for WorkHours and Lunch.")
        return 0
    elif (meetDuration < 0 or meetDuration > 60):
        global_error_stack.append("Meet duration must be in minutes and " +
            "in the range of 0 to 60.\n" +
            "Given value is: " + str(meetDuration))
        return 0
    else:
        # If all the values are okay then
        time = startTime
        while (time <= endTime):
            # Build the dictionary empty.
            keyTime = deFortmatTime(time)
            availableEmployees = [
                employee
                for employee in data["staff"]
                if (isEmployeeAvailable(keyTime, data["staff"][employee]))
            ]
            if ((time < lunchStart or time > lunchEnd) and
                (len(availableEmployees) > 2)):
                # Ignore lunch times and times with less than 3
                availableTimes[keyTime] = availableEmployees
            time += meetDuration

        # Print the file as a JSON.
        writeJSON(availableTimes)

if __name__ == "__main__":
    main()
    # Check for errors.
    if (len(global_error_stack) > 0):
        print ("Errors found durring execution:")
        for msg in global_error_stack:
            print("-> " + msg)
