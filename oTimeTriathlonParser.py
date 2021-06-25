import requests
from bs4 import BeautifulSoup


def parse_and_print_result(file, result):
    rank = result.find('div', {'class': 'rank'}).text
    if not rank.isnumeric():
        return

    division, sex = extract_division_and_sex(result.find('div', {'class': 'rank_a'}))
    name, year = extract_name_and_year(result.find('div', {'class': 'rname'}))
    country = 'RUS'
    region = extract_region(result.find('div', {'class': 'rteam'}))
    splits = extract_splits(result.find('div', {'class': 'mmm'}).find('div', {'class': 'mores'}))
    time = extract_time(result.find('div', {'class': 'rres'}))

    print(name, division, sex, country, year, region, splits[0], splits[1], splits[2], splits[3], splits[4], time,
          sep='\t', file=file)


def extract_division_and_sex(division_rank):
    division = division_rank.text.split('-')[0].strip().replace("Ж", "F").replace("М", "M")
    sex = division[:1]
    return division, sex


def extract_name_and_year(name_and_year):
    line = name_and_year.text
    open_index = line.rfind('(')
    close_index = line.rfind(')')
    name = line[:open_index].strip()
    year = line[open_index + 1:close_index]
    return name, year


def extract_region(region_and_team):
    for val in region_and_team.find('br').previous_siblings:
        return val.strip()


def extract_splits(splits):
    times = []
    table = splits.find("table")
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        split_line = cells[2].text
        index = split_line.find('(')
        if index >= 0:
            split_time = split_line[index + 1:].split(' ')[0].replace(')', '').strip()
            times.append(split_time)
        else:
            times.append('---')
    return times


def extract_time(time):
    time = time.text.strip()
    index = time.rfind(',')
    if index >= 0:
        return time[:index]
    else:
        return time


def get_results():
    url = 'https://reg.o-time.ru/start.php?ev=0&event=21235&dist=113k&group=0#find'

    request_result = requests.get(url)
    request_result.encoding = 'cp1251'

    soup = BeautifulSoup(request_result.text, features="html.parser")

    results = soup.find_all('div', {'class': ['results1', 'results2']})

    file = open("results.tsv", "w")
    print('Name', 'Division', 'Sex', 'Country', 'BirthYear', 'Region', 'Swim', 'T1', 'Bike', 'T2', 'Run', 'Finish',
          sep='\t', file=file)
    for result in results:
        parse_and_print_result(file, result)
    file.close


get_results()
