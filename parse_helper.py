#!flask/bin/python
import re, json
from flask import jsonify

from persistent_helpers import get_recipe_info

def route_command(text, recipe_id):
    """Decide if command is:
    a. Generic:
        - what is step <X>?
        - how much of <X> is required?
    b. Hardware related
        - what's the temperature of the oven?
        - is the oven ready?
    Route command accordingly

    @type recipe_id: number
    @type text: Request as String
    @return: Respose as String
    """
    text = text.lower()
    recipe_id = int(recipe_id)

    tokens = map(lambda x: x.strip(), text.split())
    tokens = set(tokens)

    hardware_kw = set(['temperature', 'oven', 'owen'])

    if len(tokens & hardware_kw) > 0:
        response = exec_hardware_command(text)
    else:
        response = exec_generic_command(recipe_id, text)

    if response is None:
        # TODO Handle elegantly
        return None

    return response


def exec_generic_command(recipe_id, text):
    """Execute generic command:
    A. what is step <X>?
    B. how much of <X> is required?

    @type recipe_id: number
    @type text: Request as String
    @return: Respose as String
    """
    # Keywords for A and B
    step_kw = ['step']
    ing_qty_kw = ['how much', 'required', 'needed', 'need', 'how many']

    # Check what kind of a question it is
    step_match = sum([kw in text for kw in step_kw])
    ing_quantity_match = sum([kw in text for kw in ing_qty_kw])

    if step_match == 0 and ing_quantity_match == 0:
        return None
    elif step_match > 0 :
        return respond_to_step(text, recipe_id)
    elif ing_quantity_match > 0:
        return respond_to_ing_qty(text, recipe_id)
    else:
        return None


def exec_hardware_command(text):
    """Execute hardware-related command
    A. what is the temperature of the oven?
    B. is the oven ready?

    @type text: Request as String
    @return: Respose as String
    """
    # Keywords for A and B
    temp_kw = ['temperature', ]
    ready_kw = ['ready', ]

    # Check what kind of a question it is
    temp_match = sum([kw in text for kw in temp_kw])
    ready_match = sum([kw in text for kw in ready_kw])

    if temp_match == 0 and ready_kw == 0:
        return None
    elif temp_match > 0 :
        return respond_to_step(text)
    elif ing_quantity_match > 0:
        return ready_match(text)
    else:
        return None


def respond_to_step(text, recipe_id):
    """Respond to:
    'what is step <X>?'
    """
    # Which step is required?
    match = re.search('step (?P<step_num>\w+)', text)
    step_str = match.group('step_num')

    try:
        step_num = int(step_str)
    except ValueError:
        step_num = text2int(step_str)

    # What are the steps in the recipe?
    recipe_info_str = json.loads(get_recipe_info(recipe_id))
    recipe_info = recipe_info_str['response']
    raw_instructions = recipe_info["Instructions"].replace('\r', '').replace('\n', '')
    instructions = raw_instructions.split('. ')
    num_instructions = len(instructions)

    # Construct response
    if step_num > num_instructions:
        response = "Step %d does not exist. There are %d steps." % (step_num, num_instructions)
    else:
        response = instructions[step_num-1]

    return json.dumps({'response' : response})


def respond_to_ing_qty(text, recipe_id):
    """Respond to:
    'how much of <X> is required?'
    """
    # What is the ingredient?
    # Detect by simple pattern matching
    match = re.search('of (?P<ing>\w+) is', text)
    ingredient = match.group('ing')

    # What are the ingredients in this recipe?
    recipe_info_str = json.loads(get_recipe_info(recipe_id))
    recipe_info = recipe_info_str['response']
    # List of 'ingredient' dicts
    ingredients = recipe_info["Ingredients"]
    # Create a dict {ingredient_name -> quantity}
    ing_dct = {}
    for ing in ingredients:
        name = ing['Name'].lower()
        quantity = ing['Quantity']
        units = ing.get('Unit', '')

        ing_dct[name] = (quantity, units)

    # Construct a response
    if ingredient not in ing_dct.keys():
        response = "%s is not necessary" % ingredient
    else:
        response = "%s %s required" % ing_dct[ingredient]

    return json.dumps({'response' : response})


def respond_to_temp(text):
    # What is the temperature?

    # Construct response
    pass


def respond_to_ready(text):
    # What is the state?

    # Construct response
    pass


def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def main():
    recipe_id = 190371
    # text = "how much of garlic is required?"
    # print respond_to_ing_qty(text, recipe_id)
    text = "what is step three"
    print route_command(text, recipe_id)

if __name__ == '__main__':
    main()
