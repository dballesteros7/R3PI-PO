#!flask/bin/python
import json
import glob
import os

from flask import Flask, jsonify
from creds.py import bigOvenAPIkey

recipe_blob_dct = {
    1 : {
        'id': 1,
        'title': 'Chicken Alfredo',
        'description': 'Chicken & Pasta & Cream.',
        'img': 'https://c1.staticflickr.com/3/2504/3874012191_48ec021023.jpg'
    },
    2 : {
        'id': 2,
        'title': 'Lasagna',
        'description': 'Garfield\'s Favorite.',
        'img': 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Lasagna_(1).jpg'
    },
    3 : {
        'id': 3,
        'title': 'Pizza',
        'description': 'Best served cold, just like revenge.',
        'img': 'https://upload.wikimedia.org/wikipedia/commons/9/95/Pizza_with_various_toppings.jpg'
    }
}


def get_recipe_ids():
    """Returns a list of valid recipe IDS

    @return: a JSON object - list of recipe IDs, where recipe ID is a number
    """
    """
    1. Get listing of files in the directory
    2. Make array of integers with the names of the files
    """

    #jsonCounter = len(glob.glob1(".../recipeJSONs/","*.json"))

    #list = [None] * jsonCounter

    dirListing = os.listdir(".../recipeJSONs/")
    lst = []
    tempName = []

    for item in dirListing:
        if ".json" in item:
            tempName = os.path.splitext(item)[0]
            lst.append(int(tempName))

    return lst
    #return jsonify({'list': recipe_blob_dct.keys()})


def get_recipe_info(recipe_id):
    """Information about the recipe

    @type recipe_id: number
    @return: a JSON object
    """

    """
    1. Get list of files
    2. If recipe_id present in list, get the contents of the files
    3. Else, make API call to get the JSON data from bigOven
    4. jsonify the data and return
    """
    list = get_recipe_ids()
    if recipe_id in list:


    """
    if recipe_id not in recipe_blob_dct.keys():
        return None
    else:
        return jsonify(recipe_blob_dct[recipe_id])
    """


def main():
    print get_recipe_ids()


if __name__ == '__main__':
    main()