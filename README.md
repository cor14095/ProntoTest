# TaskEasy CODING CHALLENGE
- Due date: January Saturday 26th 2019
- Use any language to write a program that achieves desired result
- Send us the code, the input, and the output

## The challenge:

### Given:
1. Kyle has meetings at 1:30PM, 2:30PM, and 6PM
2. Paul has meetings at 7AM, 9AM, 1:30PM, 3PM, and 3:30PM
3. Alex has meetings at 8AM, 9:30AM, 12:30PM, and 3PM
4. Luis has meetings at 9AM, 1:30PM, 3PM, and 3:30PM
5. Jairo has meetings at 8AM, 9AM, and 6PM
6. Sonya has a meeting at 8AM, 12:30PM, 1:30PM, 3:30PM

### Extra info:
- Office hours are 8AM-5PM
- Lunch is 12PM-1PM
- All meetings are half an hour long

### Desired Result:
- Return all the times when at least three people are available and who those people are
- Result should be in a format that can be used as an input for another program

## The Solution:
Program was developed with Python 3.6.3, it takes as an input a JSON file located at `input/`.
The JSON file **must** follow the following format:
1. staff *(dictionary)*
   - Employee name *(key)*
     - List of meeting times in `time format` *(ej. "1:30PM")*.
   - Any number of this.
2. WorkHours *(dictionary)*
   - start *(key)*
     - Value in `time format`
   - end *(key)*
     - Value in `time format`
3. Lunch *(dictionary)*
  - start *(key)*
    - Value in `time format`
  - end *(key)*
    - Value in `time format`
4. MeetDuration *(key)*
   - Value as an `int` representing the time of the meetings.

* `time format` is a string following in the form of HH:MM[PM/AM], if [PM/AM] is not specified the program assumes the time is in 24h format.

The program can take 1 argument:
1. `-i <filename>`: Name of the input file at `input/` folder. If no arguments given, the default filename to look is `input.json`.

### Run the code:
```
git clone
cd ProntoTest
python main.py -i schedule.json
```
Output will be on the folder `output/`, if it doesn't exist the program will create it.
