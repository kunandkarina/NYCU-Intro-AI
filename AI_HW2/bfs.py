import csv
edgeFile = 'edges.csv'


def bfs(start, end):

    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")

    """
    1. load csv file into data_list
    2. store into edges with format{startID:(endID, distance)}
    3. implement BFS
    4. using trace to backtrack the path
    5. return


    """
    file = open(edgeFile)
    reader = csv.reader(file)
    data_list = list(reader)
    file.close()

    edges = {}
    # print(type(edges))
    for i in range(1, len(data_list)):
        if edges.get(int(data_list[i][0])) != None:
            edges[int(data_list[i][0])].append(
                (int(data_list[i][1]), float(data_list[i][2])))
        else:
            edges[int(data_list[i][0])] = [
                (int(data_list[i][1]), float(data_list[i][2]))]
            
    queue = [(start, 0, 0)]
    visited = [start]
    trace = {}
    num_visited = 0
    # for a,b in edges[4421728047]:
    #     print(a,b)
    # print(queue[0][0])

    flag = True
    while (True):
        if queue[0][0] in edges.keys():
            # ID for endID dist for distance
            for ID, dist in edges[queue[0][0]]:
                if ID in visited:
                    continue
                if ID == end:
                    trace[end] = (queue[0][0], dist)
                    num_visited += 1
                    flag = False
                    break
                queue.append((ID, dist,  queue[0][0]))
                visited.append(ID)
                num_visited += 1
        trace[queue[0][0]] = (queue[0][2], queue[0][1])
        if flag == False:
            break
        queue.pop(0)

    tol_dis = 0
    path = [end]
    tol_dis += trace[path[0]][1]

    # print(trace[1079387396][0])

    while trace[path[0]][0] != 0:
        path.insert(0, trace[path[0]][0])
        tol_dis += trace[path[0]][1]

    return path, tol_dis, num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902,  1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
