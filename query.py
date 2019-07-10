import requests
import re
import time
import json

base_url = 'https://app.dimensions.ai/api/'
namespace = '["grid.16416.34", "grid.412750.5", "grid.414078.e", "grid.416663.0"]'


def get_org_from_org_id(org_id):
    if (org_id == "grid.16416.34"):
        return "University of Rochester"
    elif (org_id == "grid.412750.5"):
        return "University of Rochester Medical Center"
    elif (org_id == "grid.414078.e"):
        return "Highland Hospital"
    elif (org_id == "grid.416663.0"):
        return "Strong Memorial Hospital"
    else:
        return "NOT UR AFFILIATED"


def initialize_session():

    login = json.load('config.json')

    print('\nInitializing session...\n')

    resp = requests.post(base_url + 'auth.json', json=login)
    resp.raise_for_status()

    header = {
        'Authorization': 'JWT ' + resp.json()['token']
    }

    print('Session in progress...\n')

    # print('Got token: ' + resp.json()['token'])

    return header


def query_author(faculty_name_with_comma, header):
    faculty = get_author_name(faculty_name_with_comma)

    print('Querying author "{}"...\n'.format(faculty))
    id_affiliation = ['UNDETERMINED', 'UNDETERMINED']

    query = 'search publications in researchers for "\\"{}\\"" return researchers'.format(faculty)
    response = requests.post(
        base_url + 'dsl.json',
        data=query.encode(),
        headers=header)
    try:
        response = response.json()
    except:
        time.sleep(1)
        response = requests.post(
            base_url + 'dsl.json',
            data=query.encode(),
            headers=header)
        try:
            response = response.json()
        except:
            return id_affiliation
    # print(response, '\n')

    if (response['_stats']['total_count'] == 0):
        # print('sliced name from faculty list from : {} into : {}\n'.format(faculty, slice_name_from_faculty_list(faculty_name_with_comma)))
        id_affiliation = ['DNE', 'DNE']

    else:
        try:
            for author in response['researchers']:

                try:
                    last = author['last_name']
                    first = author['first_name']
                    if (last_first_are_in_full(last, first, faculty_name_with_comma)):
                        print('Last and First are in Full: ', first, last, '\n')
                        dim_id = author['id']
                        id_affiliation[0] = dim_id

                        try:
                            for affiliation in author['research_orgs']:
                                id_affiliation[1] = get_org_from_org_id(affiliation)
                                if (affiliation in namespace):
                                    print('Found id : {} and affiliation : {}\n'.format(id_affiliation[0], id_affiliation[1]))
                                    return id_affiliation

                        except KeyError:
                            print("Couldn't extract any affiliations for given author:\n{}\n".format(author))
                            id_affiliation[1] = 'NO AFFILIATIONS'
                            continue

                except KeyError:
                    print("Couldn't extract last_name or first_name field from author:\n{}\n".format(author))

            if (id_affiliation[0] == 'UNDETERMINED'):
                if (response['_stats']['total_count'] >= 20):
                    id_affiliation = ['TOO MANY', 'TOO MANY']
                else:
                    id_affiliation = ['DNE', 'DNE']

        except KeyError:
            print("Couldn't find any researchers with given name in response:\n{}\n".format(response))

    print('Found id : {} and affiliation : {}\n'.format(id_affiliation[0], id_affiliation[1]))
    return id_affiliation


def last_first_are_in_full(last_name, first_name, faculty):
    full_name = faculty.split(',')
    return match_last(last_name, full_name[0]) and match_first(first_name, full_name[1])


def match_last(last_name_from_query, last_name_from_faculty_list):
    query = slice_name_from_query(last_name_from_query)
    faculty = slice_last_name_from_faculty_list(last_name_from_faculty_list)
    # print('query last name : {}; faculty last name : {}\n'.format(query, faculty))
    return (query in faculty or faculty in query)


def match_first(first_name_from_query, first_name_from_faculty_list):
    query = slice_name_from_query(first_name_from_query)
    faculty = slice_first_name_from_faculty_list(first_name_from_faculty_list)
    # print('query first name : {}; faculty first name : {}\n'.format(query, faculty))
    return (query in faculty or faculty in query)


def slice_name_from_query(name_from_query):
    return name_from_query.split(' ')[0]


def slice_name_from_faculty_list(name_from_faculty_list):
    faculty = name_from_faculty_list.split(',')
    first = slice_first_name_from_faculty_list(faculty[1])
    last = slice_last_name_from_faculty_list(faculty[0])
    return first + ' ' + last


def slice_last_name_from_faculty_list(last_name_from_faculty_list):
    name_split = re.split(' |-', last_name_from_faculty_list)
    if (len(name_split) > 1):
        return name_split[1] if len(name_split[1]) != 1 else name_split[0]
    else:
        return name_split[0]


def slice_first_name_from_faculty_list(first_name_from_faculty_list):
    name_split = re.split(' |-', first_name_from_faculty_list)
    if (len(name_split) > 1):
        return name_split[0] if len(name_split[0]) != 1 else name_split[1]
    else:
        return name_split[0]


def get_author_name(original_name):
    full_name = ''
    full = original_name.split(',')

    firsts = full[1].split('-')
    for first in firsts:
        full_name += (first + ' ')

    lasts = full[0].split('-')
    for last in lasts:
        full_name += (last + ' ')

    full_name = full_name[:-1]
    return full_name


def get_author_name_just_one_first_name(original_name):
    full_name = ''
    full = original_name.split(',')

    firsts1 = full[1].split('-')
    firsts2 = firsts1[0].split(' ')
    if (len(firsts2) > 1):
        if (len(firsts2[0]) >= len(firsts2[1])):
            full_name += (firsts2[0] + ' ')
        else:
            full_name += (firsts2[1] + ' ')

    else:
        full_name += (firsts2[0] + ' ')

    lasts = full[0].split('-')
    for last in lasts:
        full_name += (last + ' ')

    full_name = full_name[:-1]
    return full_name
