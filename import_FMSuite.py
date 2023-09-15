import sqlite3
from sqlite3 import Error
import json


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
    database = r"d:\rud\OneDrive\0_mega_synch\documenti\lab casa\SDR\SDRSharp\Plugins\FMSuite\FMSuite.Databases\FMSuite.FMlistNL.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Reading original FMSuite database...")
        titles, saved_entries = select_all_entries(conn)

        for title in titles:
            print(title)

        # Save the row_data as a JSON file
        with open('output.json', 'w') as json_file:
            for entry in saved_entries:
                json.dump(entry, json_file)
                #print(entry)
    

    conn.close()


if __name__ == '__main__':
    main()