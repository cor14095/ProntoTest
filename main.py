import json
import sys
import getopt

global_error_stack = []

def open_json(fileName):
    with open('input/' + fileName) as data_file:
        data = json.load(data_file)
    return data

def write_json(data, filename):
    # Print the file as a JSON.
    with open('output/output_' + filename, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False
            , sort_keys=False, indent=4, separators=(',', ': '))

def format_time(stringTime):
    # Function input is a string with a format like this 'HH:MM[PM/AM]'.
    # Returns Time in 24h format wo PM or AM.
    result = 0.0
    stringTime = stringTime.upper()
    timeSplited = stringTime.split(':')

    # Check for correct format.
    if (len(timeSplited) != 2):
        # Format is wrong
        global_error_stack.append('Wrong format for: format_time({})'.
            format(stringTime))
        result = -1.0
        return result
    else:
        timeSuffix = timeSplited[1][-2:]
        # If no time sufix provided it's assumed to be 24hrs format.
        try:
            hours = ((float(timeSplited[0]) + 12) if timeSuffix == 'PM'
                else float(timeSplited[0]))
            hours = 12.0 if hours == 24.0 else hours
            minutes = float(timeSplited[1][:2])
        except ValueError:
            global_error_stack.append('Wrong value for: format_time({})'.
                format(stringTime))
            hours = -1.0
            minutes = -1.0

        minutes = (100.0 * minutes) / 6000.0    # divide 60 divide 100.

        result = hours + minutes

        # Check if time makes sense
        if (result < 0.0 or result > 24.0):
            global_error_stack.append('Wrong value for: format_time({})'.
                format(stringTime))
            result = -1.0
        return result

def deformat_time(floatTime):
    # This function converts output of format_time() to original.
    result = ''
    timeSplited = str(floatTime).split('.');

    timeSuffix = ('PM' if float(timeSplited[0]) > 11
        else 'AM')
    hours = ((float(timeSplited[0]) - 12) if timeSuffix == 'PM'
        else float(timeSplited[0]))
    hours = 12.0 if hours == 0.0 else hours
    minutes = float(timeSplited[1])
    minutes = (minutes * 60.00) / 1000.00

    result = ("{:.2f}".format(hours + minutes) + timeSuffix).replace('.', ':')

    return str(result)

def is_employee_available(key, employee):
    # This function check if the employee is available at that time.
    available = False if (key in employee) else True
    return available

def print_results(data, filename):
    # This function prints the results in a pretty way.
    # To a file as JSON and as a text report.

    # Print the file as a JSON.
    write_json(data, filename)

    # Generate a nice string:
    text = "Employees availability:\n"
    for time in data:
        subText = "The employees: "
        for employee in data[time]:
            subText += '\n- ' + employee
        subText += '\nAre available at:\t{}.\n\n'.format(time)
        text += subText
    print (text)

    # Write a .txt file with the data.
    with open('output/output_' + filename.split('.')[0] + '.txt', 'a') as out:
        out.write(text + '\n')

    print ("Output files printed to:")
    print ("-> output/{}\t JSON formated file.".format(filename))
    print ("-> output/{}.txt\t text formated file.".
        format(filename.split('.')[0]))


def main(argv):
    inputfile = 'input.json'
    try:
        opts, args = getopt.getopt(argv,'hi:o:',['ifile='])
    except getopt.GetoptError:
        print ('main.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':   # -h help command
            print ("test.py -i <inputfile> \tFor an specific file name.")
            print ("test.py \tProgram will look for input.json file.")
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg

    # Variables
    try:
        data = open_json(inputfile)     # Data from json.
    except FileNotFoundError:
        global_error_stack.append('No file named '{}' found.'.
            format(inputfile))
        return 0
    try:
        staff = data['staff']   # Staff schedulesself.
    except KeyError:
        global_error_stack.append('*staff* key doesn`t exist!'
            + ' Check README file to see the format.')
        return 0
    availableTimes = {}

    # Build a schedule dictionary and fill it with the data.
    # Initialize some important values.
    try:
        startTime = format_time(data['WorkHours']['start'])
        endTime = format_time(data['WorkHours']['end'])
        lunchStart = format_time(data['Lunch']['start'])
        lunchEnd = format_time(data['Lunch']['end'])
    except KeyError:
        global_error_stack.append('One of the main keys or values doesn`t'
            + ' exist, check README file to see the format.')
        return 0

    try:
        meetDuration = (float(data['MeetDuration']) * 100.0) / 6000.0
    except ValueError:
        global_error_stack.append(
            'Meet duration must be in minutes and in the range of 0 to 60.'
            + ' Given value is: -1'
        )
        meetDuration = -1
    except KeyError:
        global_error_stack.append('*MeetDuration* key doesn`t exist!'
            + ' Check README file to see the format.')
        return 0

    # Check that all this values are correct.
    if (startTime < 0 or endTime < 0 or lunchStart < 0 or lunchEnd < 0):
        global_error_stack.append('Wrong value on JSON *WorkHours* or *Lunch*.')
        return 0
    elif (lunchStart > lunchEnd or startTime > endTime):
        global_error_stack.append('Start times must be lower than end times '
            + 'for WorkHours and Lunch.')
        return 0
    elif (meetDuration < 0 or meetDuration > 60):
        global_error_stack.append('Meet duration must be in minutes and '
            + 'in the range of 0 to 60.\n'
            + 'Given value is: {}'.format(meetDuration))
        return 0
    else:
        # If all the values are okay then
        time = startTime
        while (time <= endTime):
            # Build the dictionary empty.
            keyTime = deformat_time(time)
            availableEmployees = [
                employee
                for employee in data['staff']
                if (is_employee_available(keyTime, data['staff'][employee]))
            ]
            if ((time < lunchStart or time > lunchEnd) and
                (len(availableEmployees) > 2)):
                # Ignore lunch times and times with less than 3
                availableTimes[keyTime] = availableEmployees
            time += meetDuration

        # Print result
        print_results(availableTimes, inputfile)

if __name__ == '__main__':
    main(sys.argv[1:])
    # Check for errors.
    if (len(global_error_stack) > 0):
        print ("Errors found durring execution:")
        for msg in global_error_stack:
            print("-> {}".format(msg))
