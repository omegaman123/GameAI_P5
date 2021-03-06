import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappush, heappop
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.
    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        possible = True
        if 'Consumes' in rule:
            for material in rule['Consumes']:
                if state[material] < rule['Consumes'][material]:
                    possible = False
        if 'Requires' in rule:
            for req in rule['Requires']:
                if state[req] < 1:
                    possible = False
        return possible

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        if 'Consumes' in rule:
            for material in rule['Consumes']:
                next_state[material] -= rule['Consumes'][material]
        for product in rule['Produces']:
            next_state[product] += rule['Produces'][product]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.
    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        num_goals = len(goal)
        reached = 0
        for g in goal:
            if state[g] >= goal[g]:
                reached += 1
        return reached == num_goals

        # for g, v in goal.items():
        #     if g in state:
        #         if v == state[g]:
        #             reached += 1
        # return reached == num_goals

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(current_state, effect_state, action):
    # Implement your heuristic here!
    # for keys in effect_state:
    #     if not keys in current_state:  # something new is worth exploring
    #         return -1
    # Only mine with strongest tools
    if "axe for coal" in action:
        strongest_tool = ""
        if current_state['iron_pickaxe'] > 0:
            strongest_tool = 'iron_pickaxe'
        elif current_state['stone_pickaxe'] > 0:
            strongest_tool = 'stone_pickaxe'
        elif current_state['wooden_pickaxe'] > 0:
            strongest_tool = 'wooden_pickaxe'
        if strongest_tool not in action:
            return inf
    if "axe for cobble" in action:
        strongest_tool = ""
        if current_state['iron_pickaxe'] > 0:
            strongest_tool = 'iron_pickaxe'
        elif current_state['stone_pickaxe'] > 0:
            strongest_tool = 'stone_pickaxe'
        elif current_state['wooden_pickaxe'] > 0:
            strongest_tool = 'wooden_pickaxe'
        if strongest_tool not in action:
            return inf
    if "axe for ore" in action:
        strongest_tool = ""
        if current_state['iron_pickaxe'] > 0:
            strongest_tool = 'iron_pickaxe'
        elif current_state['stone_pickaxe'] > 0:
            strongest_tool = 'stone_pickaxe'
        elif current_state['wooden_pickaxe'] > 0:
            strongest_tool = 'wooden_pickaxe'
        if strongest_tool not in action:
            return inf
    if "stone_axe at bench" in action:
        if current_state["stone_axe"] < 1:
            return -100
    if "craft cart" in action:
        if effect_state['cart'] > 1:
            return inf
        else:
            return -1000
    if "craft rail" in action:
        if current_state['cart'] > 0:
            return -1000
        else:
            return -1000
    if effect_state['bench'] > 1:  # only need 1
        return inf
    elif effect_state['wooden_axe'] > 1:  # only need 1
        return inf
    elif effect_state['furnace'] > 1:  # only need 1
        return inf
    elif effect_state['wooden_pickaxe'] > 1:  # only need 1
        return inf
    elif effect_state['stone_pickaxe'] > 1:  # only need 1
        return inf
    elif effect_state['stone_axe'] > 1:  # only need 1
        return inf
    elif effect_state['iron_pickaxe'] > 1:  # only need 1
        return inf
    elif effect_state['iron_axe'] > 1:  # only need 1
        return inf

    elif effect_state['plank'] > 8:  # having more than a certain number is redundant
        return 1000
    elif effect_state['wood'] > 3:  # having more than a certain number is redundant
        return 1000
    elif effect_state['stick'] > 5:  # having more than a certain number is redundant
        return 1000
    elif effect_state['cobble'] > 8:  # having more than a certain number is redundant
        return 1000
    elif effect_state['coal'] > 17:  # having more than a certain number is redundant
        return 1000
    elif effect_state['ore'] > 17:  # having more than a certain number is redundant
        return 1000
    elif effect_state['ingot'] > 17:  # having more than a certain number is redundant
        return 1000

    elif effect_state['plank'] > 4:  # having more than a certain number is redundant
        return 500
    elif effect_state['wood'] > 2:  # having more than a certain number is redundant
        return 500
    elif effect_state['stick'] > 2:  # having more than a certain number is redundant
        return 500
    elif effect_state['cobble'] > 5:  # having more than a certain number is redundant
        return 500
    elif effect_state['coal'] > 5:  # having more than a certain number is redundant
        return 500
    elif effect_state['ore'] > 5:  # having more than a certain number is redundant
        return 500
    elif effect_state['ingot'] > 7:  # having more than a certain number is redundant
        return 500
        # prioritize getting a tool upgrade
    elif current_state['iron_pickaxe'] == 0 and effect_state['iron_pickaxe'] == 1:
        return -100
    elif current_state['stone_pickaxe'] == 0 and effect_state['stone_pickaxe'] == 1:
        return -10
    return 0


def search(graph, state, is_goal, limit, heuristic):
    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    h = []
    heappush(h, (0, state))
    came_from = dict()
    cost_so_far = dict()
    came_from[state] = (None, "start")
    cost_so_far[state] = 0.0
    end_state = None
    failed = True
    path = []
    iterations = 0
    max_heap = 0

    # while True:
    while time() - start_time < limit:
        iterations = iterations + 1

        current = heappop(h)[1]
        if is_goal(current):
            print(f"\nstate is {current}---------------------")
            print(time() - start_time, 'seconds.')
            end_state = current
            failed = False
            break
        for possible_action, effect_state, cost in graph(current):
            # print(f"\nfrom state {current} we can do action {possible_action} with effect {effect_state} with cost {cost}")
            new_cost = cost_so_far[current] + cost
            if effect_state not in cost_so_far or new_cost < cost_so_far[effect_state]:
                # print(f"\nState is going to be {effect_state} from action {possible_action}")
                # heuristic(current ,effect_state)
                cost_so_far[effect_state] = new_cost
                priority = new_cost + heuristic(current, effect_state, possible_action)
                if priority < 10000:
                    heappush(h, (priority, effect_state))
                hl = len(h)
                max_heap = max(hl, max_heap)
                came_from[effect_state] = (current, possible_action, cost)

        # Failed to find a path
    if failed:
        print(time() - start_time, 'seconds.')
        print("Failed to find a path from", state, 'within time limit.')
        return None

    ptr = came_from[end_state]
    cost = 0
    while ptr[1] is not "start":
        path.insert(0, (ptr[0], ptr[1]))
        cost += ptr[2]
        ptr = came_from[ptr[0]]

    print(f'total cost is {cost} length is {len(path)}')
    print(f'Iterations: {iterations}, max_heap: {max_heap}\n')


    return path


if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t', state)
            print(action)
