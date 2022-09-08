import icalendar as ical
import os
'''Made to fix the icalendar files that mytimetable.com gives me.'''
# TODO:
# - Make it so that it can be run from the command line
# - Change hard coded variables to text files


ics_path = r'snbc51-MyTimetable(4).ics' # Path to the original icalendar file

# Define the find and replace terms
# TODO - make this a dictionary

find_arr = []
replace_arr = []

# Solid Mechanics 3 (ENGI3411)
find_arr.append("SUMMARY:ENGI3411")
replace_arr.append("SUMMARY: Solid Mechanics 3 (ENGI3411)")

# Control and Signal Processing 3 (ENGI3391)
find_arr.append("SUMMARY:ENGI3391")
replace_arr.append("SUMMARY: Control and Signal Processing 3 (ENGI3391)")

# Materials
find_arr.append("SUMMARY:ENGI3471")
replace_arr.append("SUMMARY:Materials 3 (ENGI3471)")

# Thermo
find_arr.append("SUMMARY:ENGI3291")
replace_arr.append("SUMMARY:Thermodynamics and Fluid Mechanics 3 (ENGI3291)")

# Electrical (W103)
find_arr.append("SUMMARY:ENGI3371\nDESCRIPTION:Electrical Engineering 3\nLOCATION:D/W103")
replace_arr.append("SUMMARY:Electrical Engineering 3 (ENGI3371)\nDESCRIPTION:Electrical Engineering 3\nLOCATION:D/W103")

# Electrical (CG85)
find_arr.append("SUMMARY:ENGI3371\nDESCRIPTION:Electrical Engineering 3\nLOCATION:D/CG85")
replace_arr.append("SUMMARY:Electrical Engineering 3 (ENGI3371)\nDESCRIPTION:Electrical Engineering 3\nLOCATION:D/CG85")

# Academic Advisor Meeting
find_arr.append("SUMMARY:ENGI3371\nDESCRIPTION:L3 Academic Adviser")
replace_arr.append("SUMMARY:Academic Advisor Meeting\nDESCRIPTION:L3 Academic Adviser")

# Labs
find_arr.append("SUMMARY:ENGI3371\nDESCRIPTION:Engineering Labs 3")
replace_arr.append("SUMMARY:Engineering Labs\nDESCRIPTION:Engineering Labs 3")

# Design (Only replace the first one)
find_arr.append("SUMMARY:ENGI3351\nDESCRIPTION:Engineering Design 3\nLOCATION:D/E121")
replace_arr.append("SUMMARY:Engineering Design\nDESCRIPTION:Engineering Design 3\nLOCATION:D/E121")
find_replace = zip(find_arr, replace_arr)

# Read the file and perform the find and replace

with open(ics_path, 'r') as f:
    filedata = f.read()
    for find, replace in find_replace:
        filedata = filedata.replace(find, replace)

with open(ics_path, 'w') as f:
    f.write(filedata)


# Open the .ics file to delete the duplicate entries
opencalendar = ical.Calendar.from_ical(open(ics_path, 'rb').read()) # Open the calendar as an icalendar object
for event in opencalendar.walk('vevent'): # Loop through all events and remove duplicates
    if event.get('summary') == 'ENGI3351' or (event.get('summary') == 'Engineering Labs' and event.get('location') != 'D/E121'):
        opencalendar.remove_component(event)
        

# write the new calendar to an ics file
f = open(ics_path, 'wb')
f.write(opencalendar.to_ical())
f.close()

print("Program ran successfully")

