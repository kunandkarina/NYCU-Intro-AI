import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    # raise NotImplementedError("To be implemented")
    """
    1. load csv file into data_list
    2. store into edges with format{startID:(endID, distance)}
    3. implement DFS with stack
    4. using trace to backtrack the path
    5. return


    """



    file = open(edgeFile)
    reader = csv.reader(file)
    data_list = list(reader)
    file.close()

    edges = {}
    for i in range(1, len(data_list)):
        if edges.get(int(data_list[i][0])) != None:
            edges[int(data_list[i][0])].append(
                (int(data_list[i][1]), float(data_list[i][2])))
        else:
            edges[int(data_list[i][0])] = [
                (int(data_list[i][1]), float(data_list[i][2]))]


    stack = [(start,0,0)]
    visited = [start]
    num_visited = 0
    trace = {}

    while(True):
        flag = True
        top = stack[-1]
        stack.pop()
        if top[0] in edges.keys():
            for ID, dist in edges[top[0]]:
                if ID in visited:
                    continue
                if ID == end:
                    num_visited += 1
                    trace[end] = (top[0], dist)
                    flag = False
                    break
                visited.append(ID)
                stack.append((ID, dist, top[0]))
                num_visited += 1
        trace[top[0]] = (top[2], top[1])
        if flag == False: 
            break
    
    tol_dis = 0
    path = [end]
    tol_dis += trace[path[0]][1]
    while trace[path[0]][0] != 0:
        path.insert(0, trace[path[0]][0])
        tol_dis += trace[path[0]][1]

    return path, tol_dis, num_visited
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
