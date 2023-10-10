import sqlite3
from sqlite3 import Error
import json
from tkinter import filedialog

__version__ = "2.0"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_entries(conn):
    """
    Query all rows in the Data table
    :param conn: the Connection object
    :return: all rows in the Data table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Data")

    rows = cur.fetchall()

    #for row in rows:
    #    print(row)

    # Execute a query to fetch the table schema
    cur.execute("PRAGMA table_info(Data)")

    # Fetch all rows from the query result
    fetched_rows = cur.fetchall()

    column_names = []

    # Extract the column names from the result
    for fetched_row in fetched_rows:
        column_names.append(fetched_row[1])


    return column_names, rows


def select_all_same_name(conn, name):
    #TODO: rewrite more efficient with COUNT or so
    cur = conn.cursor()
    cur.execute('SELECT * FROM Data WHERE Description = ?', [name])

    rows = cur.fetchall()

    #for row in rows:
    #    print(row)

    return rows



def main():
    # from SDRPlusPlus/misc_modules/frequency_manager/src/main.cpp
    dictionary_modes = {"NFM":0, "WFM":1, "AM":2, "DSB":3, "USB":4, "CW":5, "LSB":6, "RAW":7}

    # Open the input file dialog
    database = filedialog.askopenfilename(title="Select FMSuite database", filetypes=(("FMSuite database", "*.db"), ("all files", "*.*")))   
    if database == "":
        print("Cancelled.")
        return
    
    # Open the output file dialog
    output_json_filename = filedialog.asksaveasfilename(title="Enter JSON destination file", filetypes=(("JSON file", "*.json"), ("all files", "*.*")), initialfile=database.rsplit(".", 1)[0])
    if output_json_filename == "":
        print("Cancelled.")
        return
    
    # Append the extension if not already present
    extension = ".json"  # Specify your desired extension here
    if not output_json_filename.endswith(extension):
        output_json_filename += extension

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Reading original FMSuite database...")
        titles, saved_entries = select_all_entries(conn)

        for title in titles:
            print(title)

        total_num = len(saved_entries)
        duplicated_num = 0

        # Save the row_data as a JSON file
        with open(output_json_filename, 'w') as json_file:
            
            # format as per SDRPlusPlus import need
            json_file.write('{"bookmarks": {')
            
            for i,entry in enumerate(saved_entries):
                # put together entry and title in a dictionary
                dictionary = dict(zip(titles, entry))
                #print(dictionary)

                # format GEO info data
                geo_string = ""

                if dictionary['Power'] != "" and dictionary['Power'] is not None:
                    geo_string = geo_string + "Pwr: " + str(dictionary['Power']) + " "

                if dictionary['City'] != "" and dictionary['City'] is not None:
                    geo_string = geo_string + "Cty: " + dictionary['City'] + " "
                
                if dictionary['Country'] != "" and dictionary['Country'] is not None:
                    geo_string = geo_string + "Cntr: " + dictionary['Country'] + " "
                
                if dictionary['Language'] != "" and dictionary['Language'] is not None:
                    geo_string = geo_string + "Lng: " + dictionary['Language'] + " "

                 # format time data
                startTime = dictionary['StartTime']
                if startTime is not None:
                    if startTime.isdigit() and len(startTime) == 4:
                        startTime_string = startTime
                    else:
                        startTime_string = "0"
                else:
                    startTime_string = "0"
                startTime_num = int(startTime_string)

                stopTime = dictionary['StopTime']
                if stopTime is not None:
                    if stopTime.isdigit() and len(stopTime) == 4 and stopTime is not None:
                        stopTime_string = stopTime
                    else:
                        stopTime_string = "0"
                else:
                    stopTime_string = "0"
                stopTime_num = int(stopTime_string)

                # format Day data

                days = dictionary['Days']
                digits = ["1", "2", "3", "4", "5", "6", "7"]
                days_array = []

                if days != "" and days is not None:
                    for digit in digits:
                        if digit in days:
                            days_array.append(True)
                        else:
                            days_array.append(False)
                else:
                    for digit in digits:
                        days_array.append(True)

                #if dictionary['Description'] == "Radio Delta International":
                #    xxx = 3

                # check if descritpion is duplicate. In that case, append the database ID to the name
                description_to_check = dictionary['Description']
                dupl_rows = select_all_same_name(conn, description_to_check)
                if len(dupl_rows) > 1:
                    description_string = dictionary['Description'] + "_" + str(dictionary['Id'])
                    duplicated_num += 1
                else:
                    description_string = dictionary['Description']

                if dictionary['Notes'] != "" and dictionary['Notes'] is not None:
                    notes_string = dictionary['Notes']
                else:
                    notes_string = ""

                reformatted_dictionary = {description_string: {"bandwidth": dictionary['Filter Bandwidth'],"frequency":dictionary['Frequency'],"mode":dictionary_modes[dictionary['Mode']], "geoinfo":geo_string, "startTime":startTime_num, "stopTime":stopTime_num, "days":days_array, "notes": notes_string}}

                token = json.dumps(reformatted_dictionary, indent=4)
                
                # clean the description name coming from some FMSuite exports
                token = token.replace("\\ufffd", " ")

                json_file.write(token[1:-1])

                # seprate the entries with commas if not the last
                if i != len(saved_entries) - 1:
                    json_file.write(',')
            
                print(f"\rTranslated entry: {i}, progress: {int(i/total_num*100)}%...", end ='', flush=True)
            json_file.write('}\n}')
            print(f"\n\rTranslated {i+1} entries. {duplicated_num} entries were duplicated. File {output_json_filename}. Done.")

    conn.close()


if __name__ == '__main__':
    main()