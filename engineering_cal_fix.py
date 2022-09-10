from inspect import _void
import icalendar as ical
import csv # Could use pandas but would be slightly overkill
import urllib.request  #To calendar url
'''Made to fix the icalendar files that mytimetable.com gives me.'''
# TODO:
# - Make it so that it can be run from the command line
# - Use MyTimetable API directly to get the calendar url
# - Automatically upload to Outlook using Outlook Calendar API
# - Done -- Automatically download calendar by interacting with mytimetable.com
# - DONE --Change hard coded variables to text files

csv_path = r'find_replace.csv' # Path to the csv file with the find and replace values
ics_path = r'calendar.ics' # Path to ical file
calendar_url = 'https://mytimetable.durham.ac.uk/calendar/export/d61ad5f1523baa3cb3c4a6bf51611cfb6468d982.ics'

calendar = urllib.request.urlretrieve(calendar_url, ics_path); # Download the calendar


# Read the csv file
with open(r'find_replace.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', dialect='excel') 
    head = next(reader) # Skip the header
    find = [] # List of strings to find
    replace = [] # List of strings to replace with
    for line in (reader):
        find.append(line[0])
        replace.append(line[1])

find_replace = zip(find, replace)
with open(ics_path, 'r') as f:
    filedata = f.read()
    for find, replace in find_replace:
        filedata = filedata.replace(find, replace)

with open(ics_path, 'w') as f:
    f.write(filedata)

def remove_events_with_summary(event, summary, location = None): # Remove all events with a given summary, though for now set date to 01/01/2025 and remove manually
    '''Remove all events with a given summary, though for now set date to 01/01/2025, optionally NOT the ones with a given location

    Parameters
    ----------
    event : icalendar.Event
        Event to be removed
    summary : string
        Summary parameter of the event to be removed
    location : string, optional
        Location parameter of the event to be KEPT
    '''
    removal_date = '20250101T000000Z'
    # TODO: make method of icalendar.Calendar
    if event.get('summary') == summary and location is None:
        event['dtstart'] = removal_date
        event['dtend'] = removal_date
        event['dtstamp'] = removal_date
        event['description'] = 'This event has been removed'
    elif event.get('summary') == summary and event.get('location') != location:
        event['dtstart'] = removal_date
        event['dtend'] = removal_date
        event['dtstamp'] = removal_date
        event['description'] = 'This event has been removed'

remove_events_with_summary()
# Open the .ics file to delete the duplicate entries
opencalendar = ical.Calendar.from_ical(open(ics_path, 'rb').read()) # Open the calendar as an icalendar object
for event in opencalendar.walk('vevent'): # Loop through all events and remove duplicates
    remove_events_with_summary(event, summary = 'ENGI3351')
    remove_events_with_summary(event, summary = 'Engineering Labs', location = 'D/E121')




# write the new calendar to an ics file
f = open(ics_path, 'wb')
f.write(opencalendar.to_ical())
f.close()

print("Program ran successfully")