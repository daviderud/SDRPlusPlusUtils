import sqlite3
from sqlite3 import Error
import json
from tkinter import filedialog



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



def main():
    # from SDRPlusPlus/misc_modules/frequency_manager/src/main.cpp
    dictionary_modes = {"NFM":0, "WFM":1, "AM":2, "DSB":3, "USB":4, "CW":5, "LSB":6, "RAW":7}

    # Open the input file dialog
    database = filedialog.askopenfilename(title="Select FMSuite database", filetypes=(("FMSuite database", "*.db"), ("all files", "*.*")))   
    if database == "":
        return
    
    # Open the output file dialog
    output_json_filename = filedialog.asksaveasfilename(title="Enter JSON destination file", filetypes=(("JSON file", "*.json"), ("all files", "*.*")), initialfile=database.rsplit(".", 1)[0])
    if output_json_filename == "":
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

        # Save the row_data as a JSON file
        with open(output_json_filename, 'w') as json_file:
            
            # format as per SDRPlusPlus import need
            json_file.write('{"bookmarks": {')
            
            for i,entry in enumerate(saved_entries):
                # put together entry and title in a dictionary
                dictionary = dict(zip(titles, entry))
                print(dictionary)

                # format GEO info data
                geo_string = ""
                if dictionary['City'] != "":
                    geo_string = geo_string + "Cty: " + dictionary['City'] + " "
                
                if dictionary['Country'] != "":
                    geo_string = geo_string + "Cntr: " + dictionary['Country'] + " "
                
                if dictionary['Language'] != "":
                    geo_string = geo_string + "Lng: " + dictionary['Language'] + " "

                 # format time data
                startTime = dictionary['StartTime']
                if startTime.isdigit() and len(startTime) == 4:
                    startTime_string = startTime
                else:
                    startTime_string = "0"

                stopTime = dictionary['StopTime']
                if stopTime.isdigit() and len(stopTime) == 4:
                    stopTime_string = stopTime
                else:
                    stopTime_string = "0"

                # format Day data

                days = dictionary['Days']
                digits = ["1", "2", "3", "4", "5", "6", "7"]
                days_array = []

                if days != "":
                    for digit in digits:
                        if digit in days:
                            days_array.append("true")
                        else:
                            days_array.append("false")
                else:
                    for digit in digits:
                        days_array.append("true")


                reformatted_dictionary = {dictionary['Description']: {"bandwidth": dictionary['Filter Bandwidth'],"frequency":dictionary['Frequency'],"mode":dictionary_modes[dictionary['Mode']], "geo":geo_string, "startTime":startTime_string, "stopTime":stopTime_string, "days":days_array, "notes": dictionary['Notes']}}

                token = json.dumps(reformatted_dictionary, indent=4)
                
                # clean the description name coming from some FMSuite exports
                token = token.replace("\\ufffd", " ")

                json_file.write(token[1:-1])

                # seprate the entries with commas if not the last
                if i != len(saved_entries) - 1:
                    json_file.write(',')
            
            json_file.write('}\n}')
    

    conn.close()


if __name__ == '__main__':
    main()