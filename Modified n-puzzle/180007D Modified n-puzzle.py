import sys
import argparse

# Input start configuration and goal configuration and heuristic_name as cmd inputs
start_configuration_file_name = sys.argv[1]
goal_configuration_file_name = sys.argv[2]
heuristic_name = sys.argv[3]
# start_configuration_file_name = "Sample_Start_Configuration.txt"
# goal_configuration_file_name = "Sample_Goal_Configuration.txt"
# heuristic_name = "manhattan"

output_file_name = "Output.txt"


# Take inputs and append them to given list
def take_inputs(file_name, append_list):
    file = open(file_name, "r")
    lines = file.readlines()
    for line in lines:
        append_list.append(line.strip().split())
    file.close()
    return append_list


start_conf = []
goal_conf = []
start_conf = take_inputs(start_configuration_file_name, start_conf)
goal_conf = take_inputs(goal_configuration_file_name, goal_conf)

size = len(start_conf)

# get number of misplaced tiles
def get_misplaced_tiles(goal_configuration, conf):
    total = 0
    for row in range(size):
        for col in range(size):
            if goal_configuration[row][col] != conf[row][col]:
                total += 1
    return total


# get manhattan distance
def get_manhattan_distance(goal_configuration, tile, r, c):
    if tile == '-':
        return 0
    for row in range(size):
        for col in range(size):
            if goal_configuration[row][col] == tile:
                return abs(row - r) + abs(col - c)


# get total manhattan distance
def get_total_manhattan_distance(goal_configuration, conf):
    total = 0
    for r in range(size):
        for c in range(size):
            total += get_manhattan_distance(goal_configuration, conf[r][c], r, c)
    return total


# choose heuristic from number of misplaced tiles or manhattan
def choose_heuristic(h_name):
    if h_name == 'misplaced':
        return get_misplaced_tiles
    elif h_name == 'manhattan':
        return get_total_manhattan_distance
    else:
        raise NotImplementedError("Only misplaced_tiles and manhattan_distance are available")


heuristic = choose_heuristic(heuristic_name)


class Node:
    def __init__(self, conf, parent, g):
        self.conf = conf
        self.parent = parent
        self.g = g
        self.h = heuristic(goal_configuration=goal_conf, conf=conf)

    def f(self):
        return self.g + self.h


# g values = 0 for starting node
open_nodes = [Node(start_conf, None, 0)]
closed_nodes = []


# return the node with minimum f value in open node set
def get_min_open_node():
    min_node = open_nodes[0]
    min_f_value = open_nodes[0].f()
    for open_node in open_nodes[1:]:
        if open_node.f() < min_f_value:
            min_node = open_node
            min_f_value = open_node.f()
    return min_node


# return the node in open node set which has the same configuration to given node
def get_open_node(node):
    for open_node in open_nodes:
        if open_node.conf == node.conf:
            return open_node


# return next possible location
def get_next_possible_locations(current_node):
    dash_location1 = None
    dash_location2 = None
    nodes = []
    for row in range(size):
        for col in range(size):
            if current_node.conf[row][col] == '-':
                if dash_location1 == None:
                    dash_location1 = (row, col)
                else:
                    dash_location2 = (row, col)

    if dash_location1[0] - 1 >= 0 and current_node.conf[dash_location1[0] - 1][dash_location1[1]] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location1[0]][dash_location1[1]], temp_conf[dash_location1[0] - 1][dash_location1[1]] = \
            temp_conf[dash_location1[0] - 1][dash_location1[1]], temp_conf[dash_location1[0]][dash_location1[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location1[0] + 1 <= (size - 1) and current_node.conf[dash_location1[0] + 1][dash_location1[1]] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location1[0]][dash_location1[1]], temp_conf[dash_location1[0] + 1][dash_location1[1]] = \
            temp_conf[dash_location1[0] + 1][dash_location1[1]], temp_conf[dash_location1[0]][dash_location1[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location1[1] - 1 >= 0 and current_node.conf[dash_location1[0]][dash_location1[1] - 1] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location1[0]][dash_location1[1]], temp_conf[dash_location1[0]][dash_location1[1] - 1] = \
            temp_conf[dash_location1[0]][dash_location1[1] - 1], temp_conf[dash_location1[0]][dash_location1[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location1[1] + 1 <= (size - 1) and current_node.conf[dash_location1[0]][dash_location1[1] + 1] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location1[0]][dash_location1[1]], temp_conf[dash_location1[0]][dash_location1[1] + 1] = \
            temp_conf[dash_location1[0]][dash_location1[1] + 1], temp_conf[dash_location1[0]][dash_location1[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location2[0] - 1 >= 0 and current_node.conf[dash_location2[0] - 1][dash_location2[1]] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location2[0]][dash_location2[1]], temp_conf[dash_location2[0] - 1][dash_location2[1]] = \
            temp_conf[dash_location2[0] - 1][dash_location2[1]], temp_conf[dash_location2[0]][dash_location2[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location2[0] + 1 <= (size - 1) and current_node.conf[dash_location2[0] + 1][dash_location2[1]] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location2[0]][dash_location2[1]], temp_conf[dash_location2[0] + 1][dash_location2[1]] = \
            temp_conf[dash_location2[0] + 1][dash_location2[1]], temp_conf[dash_location2[0]][dash_location2[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location2[1] - 1 >= 0 and current_node.conf[dash_location2[0]][dash_location2[1] - 1] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location2[0]][dash_location2[1]], temp_conf[dash_location2[0]][dash_location2[1] - 1] = \
            temp_conf[dash_location2[0]][dash_location2[1] - 1], temp_conf[dash_location2[0]][dash_location2[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))

    if dash_location2[1] + 1 <= (size - 1) and current_node.conf[dash_location2[0]][dash_location2[1] + 1] != '-':
        temp_conf = [x[:] for x in current_node.conf]
        temp_conf[dash_location2[0]][dash_location2[1]], temp_conf[dash_location2[0]][dash_location2[1] + 1] = \
            temp_conf[dash_location2[0]][dash_location2[1] + 1], temp_conf[dash_location2[0]][dash_location2[1]]
        nodes.append(Node(temp_conf, current_node, current_node.g + 1))
    return nodes


def get_move(from_node, to_node):
    move = "("
    for row in range(size):
        for col in range(size):
            if from_node.conf[row][col] != to_node.conf[row][col] and from_node.conf[row][col] != '-':
                move += from_node.conf[row][col] + ","
                if row - 1 >= 0 and from_node.conf[row][col] == to_node.conf[row - 1][col]:
                    move += "up)"
                if row + 1 <= (size - 1) and from_node.conf[row][col] == to_node.conf[row + 1][col]:
                    move += "down)"
                if col - 1 >= 0 and from_node.conf[row][col] == to_node.conf[row][col - 1]:
                    move += "left)"
                if col + 1 <= (size - 1) and from_node.conf[row][col] == to_node.conf[row][col + 1]:
                    move += "right)"
                break
    return move


# Get the full path
def get_full_path(current_node):
    full_path = []
    while current_node.parent != None:
        full_path.append(get_move(current_node.parent, current_node))
        current_node = current_node.parent
    full_path.reverse()
    return full_path


# check whether given node is in open node set
def check_node_open(node):
    for open_node in open_nodes:
        if open_node.conf == node.conf:
            return True
    return False


# check whether given node is in closed node set
def check_node_close(node):
    for closed_node in closed_nodes:
        if closed_node.conf == node.conf:
            return True
    return False


iterations = 0
def A():
    iterations = 0
    while len(open_nodes) > 0:
        iterations += 1
        current_node = get_min_open_node()
        if current_node.conf == goal_conf:
            return [iterations, get_full_path(current_node)]
        open_nodes.remove(current_node)
        closed_nodes.append(current_node)
        for next_node in get_next_possible_locations(current_node):
            if check_node_close(next_node):
                continue
            if not (check_node_open(next_node)):
                open_nodes.append(next_node)
            else:
                open_state = get_open_node(next_node)
                if next_node.g < open_state.g:
                    open_state.g = next_node.g
                    open_state.parent = next_node.parent

iterations, path = A()
print(iterations, path)

outFile = open(output_file_name, "w")
outFile.write(", ".join(path))
outFile.close()

iteration_out = open(f"{heuristic_name}.txt", "w")
iteration_out.write(str(iterations))
iteration_out.close()




