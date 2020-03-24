# file for maintenancing database and puzzles parsing
from puzzle_downloader import check_all_xml_puzzles, download_puzzles_as_xml
from database import DatabaseHandler
from parser import parse_puzzle_from_xml_file
import tqdm


# create database that contain all retrieved puzzles
def init_and_populate_database(db_handler, directory_path, start_index, end_index):
    db_handler.create_table()
    for i in tqdm.tqdm(range(start_index, end_index + 1)):
        puzzle_data = parse_puzzle_from_xml_file(f'{directory_path}{i}.xml')
        if puzzle_data is not None:
            db_handler.insert_data(puzzle_data[0], puzzle_data[1], puzzle_data[2], puzzle_data[3], puzzle_data[4],
                                   puzzle_data[5], puzzle_data[6])


# method to retrieve all puzzles as xml files to 'puzzle' directory which is in the same location as script
# REMEMBER to create folder 'puzzles' before using this function
# download_puzzles_as_xml('puzzles', 'puzzle', 1, 33763)


# method to validate all puzzles and removing puzzles that do not exist
# check_all_xml_puzzles('puzzles/puzzle', 1, 33763)


# uncomment below lines to parse downloaded data
# dh = DatabaseHandler()
# init_and_populate_database(dh, 'puzzles/puzzle', 1, 33763)
# dh.close_connection()
