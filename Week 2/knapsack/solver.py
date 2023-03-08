#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])


def sort_items(items):
    
    return sorted(items, key=lambda items: (items.value / items.weight, 1/items.weight), reverse=True)   

def max_value(sorted_items, current_value, capacity):
    additional_value = 0
    for i in sorted_items:
#         print(i.weight)
        if capacity >= 0:
#             print(capacity)
            weight_taken = min(i.weight, capacity)
            capacity -= weight_taken
#             print(capacity)
            additional_value += i.value * weight_taken / i.weight
#             print(additional_value)
    
    return additional_value + current_value

def dummy_solver(items, current_index, current_value, current_capacity, 
                 actual_max, current_selection, max_selection):

    if current_index < len(items):
        item = items[current_index] 
        
        # try adding this item
        if item.weight <= current_capacity:
            new_capacity = current_capacity - item.weight
            current_selection[current_index] = 1
            new_value = current_value + item.value
            current_max = max_value(items[current_index+1:], new_value, new_capacity)
            if current_max < actual_max:
                pass
            else:
                if new_value > actual_max:
                    max_selection = current_selection[:]
                    actual_max = new_value
                max_selection, actual_max = dummy_solver(items, current_index+1, new_value, new_capacity, actual_max, 
                             current_selection, max_selection)

        # try not adding this item
        new_capacity = current_capacity
        current_selection[current_index] = 0
        new_value = current_value 
        current_max = max_value(items[current_index+1:], new_value, new_capacity)
#         print(current_max)
#         print(current_selection)

        if current_max < actual_max:
            pass
        else:
            if new_value > actual_max:
#                 print(new_value, actual_max)
                max_selection = current_selection[:]
    #             print(max_selection)
                actual_max = new_value


            max_selection, actual_max = dummy_solver(items, current_index+1, new_value, new_capacity, actual_max, 
                             current_selection, max_selection)
#         print(max_selection)
    return max_selection, actual_max


def final_solution(items, sorted_items, solution):
    answer = [0]*len(items)
    value = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            value += sorted_items[i].value
            answer[sorted_items[i].index]=1

    return answer, value

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    sorted_items = sort_items(items)
    solution, max_value = dummy_solver(sorted_items, 0, 0, capacity, 0, [0]*item_count, [0]*item_count)
    taken, value = final_solution(items, sorted_items, solution)

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    # value = 0
    # weight = 0
    # taken = [0]*len(items)

    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

