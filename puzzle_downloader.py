import requests
from parser import parse_from_string


def get_puzzle(puzzle_number, save_index, file_prefix='puzzle', file_extension='txt'):
    # set some basic headers
    headers = {
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

    response = requests.post('https://webpbn.com/export.cgi/export.cgi/webpbn004533.xml', headers=headers, data=data)

    # if file_extension is not empty, add '.' before it
    if file_extension is not '':
        file_prefix = '.'+file_prefix
    # parse received puzzle and save it to file
    parse_from_string(response.text, f'{file_prefix}{save_index}{file_extension}')


get_puzzle(304, 12)
# a = [304, 307, 1398, 3965, 4097, 4239, 4255, 4404, 4405, 4406, 4407, 4408, 4451, 4481, 4482]
#
# for index, x in enumerate(a):
#     print(index)
#     get_puzzle(x, index)

