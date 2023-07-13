import csv
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    # raise NotImplementedError("To be implemented")
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
    

    queue = [[start, 0, 0]]    # ID, accumulated dist, parent
    # for i in queue:
    #     print(i)
    print(edges[start])
    for ID, dist in edges[queue[0][0]]:
        print(ID,dist)

    trace = {}
    num_visited = 0

    while(True):
        flag = True
        # min : index having minimum accumulated dist
        min = 0
        for i in queue:
            if i[1] < queue[min][1]:
                min = queue.index(i)
        
        if queue[min][0] in edges.keys():
            for ID, dist in edges[queue[min][0]]:
                change = False
                if ID in trace.keys():
                    continue
                for i in range(len(queue)):
                    if queue[i][0] == ID:
                        if queue[min][1] + dist < queue[i][1]:
                            queue[i][1] = queue[min][1] + dist
                            queue[i][2] = queue[min][0]
                        change = True
                if change == True:
                    continue
                if ID == end:
                    trace[end] = queue[min][0]
                    d = queue[min][1] + dist
                    num_visited += 1
                    flag = False
                    break
                queue.append([ID, queue[min][1] + dist, queue[min][0]])
                num_visited += 1
        trace[queue[min][0]] = queue[min][2]
        if flag == False:
            break
        queue.pop(min)

    path = [end]
    while trace[path[0]] != 0:
        path.insert(0, trace[path[0]])

    return path, d, num_visited

    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
