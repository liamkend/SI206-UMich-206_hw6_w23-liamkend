import requests
import json
import unittest
import os

###########################################
# Your name: Liam Kendall                 #
# Who you worked with: Zack Eisman        #
###########################################

def load_json(filename):
    try:
        with open(filename, 'r') as inFile:
            data = inFile.read()
            d = json.loads(data)
    except:
        d = {}
    return d

def write_json(filename, dict):
    with open(filename, 'w') as outFile:
        json.dump(dict, outFile)

def get_swapi_info(url, params=None):
    try:
        r = requests.get(url, params)
        return json.loads(r.text)
    except:
        print("Exception!")
        return None

def cache_all_pages(people_url, filename):    
    d = load_json(filename)
    r = requests.get(people_url)
    page = json.loads(r.text)
    next = page.get('next')
    num = 1
    page_num = 'page 1'

    if page_num not in d:
        d[page_num] = page.get('results')
    
    while next:
        num += 1
        page_num = "page " + str(num)
        page = get_swapi_info(next)
        if page_num not in d:
            d[page_num] = page.get('results')
        next = page.get('next')
        
    write_json(filename, d)

def get_starships(filename):
    '''
    Access the starships url for each character (if any) and pass it to the get_swapi_info function 
    to get data about a person's starship.
    
    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the character's name as a key and a list of the name their 
    starships as the value
    '''

    pass

#################### EXTRA CREDIT ######################

def calculate_bmi(filename):
    '''
    Calculate each character's Body Mass Index (BMI) if their height and mass is known. With the metric 
    system, the formula for BMI is weight in kilograms divided by height in meters squared. 
    Since height is commonly measured in centimeters, an alternate calculation formula, 
    dividing the weight in kilograms by the height in centimeters squared, and then multiplying 
    the result by 10,000, can be used.

    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the name as a key and the BMI as the value
    '''

    pass

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "swapi_people.json"
        self.cache = load_json(self.filename)
        self.url = "https://swapi.dev/api/people"

    def test_write_json(self):
        write_json(self.filename, self.cache)
        dict1 = load_json(self.filename)
        self.assertEqual(dict1, self.cache)

    def test_get_swapi_info(self):
        people = get_swapi_info(self.url)
        tie_ln = get_swapi_info("https://swapi.dev/api/vehicles", {"search": "tie/ln"})
        self.assertEqual(type(people), dict)
        print(tie_ln['results'][0]["name"])
        self.assertEqual(tie_ln['results'][0]["name"], "TIE/LN starfighter")
        self.assertEqual(get_swapi_info("https://swapi.dev/api/pele"), None)
    
    def test_cache_all_pages(self):
        cache_all_pages(self.url, self.filename)
        swapi_people = load_json(self.filename)
        self.assertEqual(type(swapi_people['page 1']), list)

    def test_get_starships(self):
        starships = get_starships(self.filename)
        self.assertEqual(len(starships), 19)
        self.assertEqual(type(starships["Luke Skywalker"]), list)
        self.assertEqual(starships['Biggs Darklighter'][0], 'X-wing')

    def test_calculate_bmi(self):
        bmi = calculate_bmi(self.filename)
        self.assertEqual(len(bmi), 59)
        self.assertAlmostEqual(bmi['Greedo'], 24.73)
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
