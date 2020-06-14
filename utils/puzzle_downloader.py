import requests
from utils.parser import parse_from_string_to_file, remove_not_existing_puzzle
import tqdm
from multiprocessing.dummy import Pool as ThreadPool


class PuzzleDownloader:
    def __init__(self):
        self.DIRECTORY = ''
        self.FILE_PREFIX = 'puzzle'

        # set some basic headers
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://webpbn.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://webpbn.com/export.cgi/webpbn004532.xml',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
        }

    def save_puzzle_parsed(self, puzzle_number, save_index, file_extension='txt'):
        # set id of downloaded puzzle and format of the exported data
        data = {
          'go': '1',
          'sid': '',
          'id': puzzle_number,
          'fmt': 'xml',
          'xml_clue': 'on',
          'xml_soln': 'on',
          'ss_soln': 'on',
          'sg_clue': 'on',
          'sg_soln': 'on'
        }

        response = requests.post('https://webpbn.com/export.cgi/export.cgi/webpbn004533.xml', headers=self.headers, data=data)

        # if file_extension is not empty, add '.' before it
        if file_extension is not '':
            file_extension = '.'+file_extension
        # if directory exists and does not end with slash, add it
        if self.DIRECTORY is not '' and self.DIRECTORY[-1] is not '/':
            self.DIRECTORY = self.DIRECTORY + '/'
        # parse received puzzle and save it to file
        parse_from_string_to_file(response.text, f'{self.DIRECTORY}{self.FILE_PREFIX}{save_index}{file_extension}')

    def get_and_save_puzzle_as_xml(self, puzzle_number, file_extension='xml'):
        # set id of downloaded puzzle and format of the exported data
        data = {
          'go': '1',
          'sid': '',
          'id': puzzle_number,
          'fmt': 'xml',
          'xml_clue': 'on',
          'xml_soln': 'on',
          'ss_soln': 'on',
          'sg_clue': 'on',
          'sg_soln': 'on'
        }

        response = requests.post('https://webpbn.com/export.cgi/export.cgi/webpbn004533.xml', headers=self.headers, data=data)

        # if file_extension is not empty, add '.' before it
        if file_extension is not '':
            file_extension = '.' + file_extension
        # if directory exists and does not end with slash, add it
        if self.DIRECTORY is not '' and self.DIRECTORY[-1] is not '/':
            self.DIRECTORY = self.DIRECTORY + '/'
        # parse received puzzle and save it to file
        f = open(f'{self.DIRECTORY}{self.FILE_PREFIX}{puzzle_number}{file_extension}', 'w')
        f.write(response.text)
        f.close()


# get all puzzles as XMLs
def download_puzzles_as_xml(directory_path, file_prefix, start_index, end_index):
    pool = ThreadPool(16)
    pd = PuzzleDownloader()
    pd.DIRECTORY = directory_path
    pd.FILE_PREFIX = file_prefix
    my_array = [i for i in range(start_index, end_index+1)]
    for _ in tqdm.tqdm(pool.imap_unordered(pd.get_and_save_puzzle_as_xml, my_array), total=len(my_array)):
        pass


# check if every file contains valid puzzle
def check_all_xml_puzzles(directory_path, start_index, end_index):
    pool = ThreadPool(16)
    my_array = [f'{directory_path}{i}.xml' for i in range(start_index, end_index+1)]
    for _ in tqdm.tqdm(pool.imap_unordered(remove_not_existing_puzzle, my_array), total=len(my_array)):
        pass







