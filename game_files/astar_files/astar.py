from game_files.astar_files.node import Node


def sorted_insert(lst, item, w):
    for i in range(len(lst)):
        if item.get_f(w) <= lst[i].get_f(w):
            lst.insert(i, item)
            return True
    lst.append(item)
    return False


def heuristic(loc, target, D=1, D2=2):
    dx = abs(loc[0] - target[0])
    dy = abs(loc[1] - target[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def successors(grid, node):
    # input is node, output is nodes.
    straight_directions = (-1, 0), (0, -1), (0, 1), (1, 0)
    diag_directions = (-1, -1), (1, -1), (1, 1), (-1, 1)

    sons = []
    for dir in straight_directions:
        new_loc = try_move(grid, node.loc, dir)
        if new_loc:
            sons.append(Node(new_loc))

    for dir in diag_directions:
        new_loc = try_move(grid, node.loc, dir)
        if new_loc and try_move(grid, node.loc, (dir[0], 0)) and try_move(grid, node.loc, (0, dir[1])):
            sons.append(Node(new_loc))

    return sons  # returns list of nodes


def try_move(grid, loc, dir):
    grid_y = len(grid)
    grid_x = len(grid[0])
    new_x = loc[0] + dir[0]
    if 0 <= new_x < grid_x:
        new_y = loc[1] + dir[1]
        if 0 <= new_y < grid_y:
            if not grid[new_y][new_x]:
                return new_x, new_y

    return False


def a_star(grid, loc, target=(1, 1), w=0.5):
    open = [Node(loc, heuristic(loc, target), 0)]
    close = []
    while open:
        next = open.pop(0)
        close.append(next)
        if next.h == 0:
            return next.get_path()[::-1]
        sons = successors(grid, next)

        for s in sons:
            new_g = next.g + 1

            if s in open:
                old_node = open[open.index(s)]
                if new_g < old_node.g:
                    old_node.g = new_g
                    old_node.father = next
                    open.sort(key=lambda n: n.get_f(w))

            elif s in close:
                old_node = close[close.index(s)]
                if new_g < old_node.g:
                    old_node.g = new_g
                    old_node.father = next
                    sorted_insert(open, old_node, w)

            else:
                new = Node(s.get_loc(), heuristic(s.get_loc(), target), new_g, next)
                sorted_insert(open, new, w)
    return False


def main():
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    node = Node((0, 1))
    print(successors(grid, node))
    print(node.get_heurisitic((0, 1)))

    print(len(grid))
    solution = a_star(grid, (1, 1), (6, 10))
    print(solution)
    for block in solution:
        grid[block[1]][block[0]] = 'K'
    for line in grid:
        for col in line:
            print(col, end=' ')
        print('')
    print('')


if __name__ == '__main__':
    main()
