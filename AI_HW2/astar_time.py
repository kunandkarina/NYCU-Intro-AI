import csv
import math
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    # raise NotImplementedError("To be implemented")
    case = 0
    file = open(heuristicFile)
    reader = csv.reader(file)
    data_list = list(reader)
    file.close()


    dists = {}
    for i in range(1, len(data_list)):
        if dists.get(int(data_list[i][0])) != None:
            dists[int(data_list[i][0])].append[float(data_list[i][1]), float(data_list[i][2]), float(data_list[i][3])]
        else:
            dists[int(data_list[i][0])] = [math.sqrt(float(data_list[i][1])), math.sqrt(float(data_list[i][2])), math.sqrt(float(data_list[i][3]))]

    file = open(edgeFile)
    reader = csv.reader(file)
    data_list = list(reader)
    file.close()


    # print(data_list[1])

    edges = {}
    for i in range(1, len(data_list)):
        if edges.get(int(data_list[i][0])) != None:
            edges[int(data_list[i][0])].append(
                (int(data_list[i][1]), float(data_list[i][2]), float(data_list[i][3]) * 1000/3600 ))
        else:
            edges[int(data_list[i][0])] = [
                 (int(data_list[i][1]), float(data_list[i][2]), float(data_list[i][3]) * 1000/3600 )]
            
    queue = [[start, dists[start][case], 0, 0]]         # ID, accumulated dist, parent
    trace = {}
    num_visited = 0

    # print(edges[start][1][2])


    while (True):
        flag = True
        # min : index having minimum accumulated dist
        min = 0
        for i in queue:
            if i[1] < queue[min][1]: 
                min = queue.index(i)

        if queue[min][0] in edges.keys():  # check if it is a leaf node
            for ID, dist, speed in edges[queue[min][0]]: 
                change = False
                if ID in trace.keys(): continue  # check if the node is explored
                for i in range(len(queue)):
                    if queue[i][0] == ID:
                        if queue[min][2] + dist/speed + dists[ID][case] < queue[i][1]: 
                            queue[i][1] = queue[min][2] + dist/speed + dists[ID][case]
                            queue[i][2] = queue[min][2] + dist/speed
                            queue[i][3] = queue[min][0]
                        change = True
                if change == True: 
                    continue     
                if ID == end: 
                    trace[end] = queue[min][0]
                    d = queue[min][2] + dist/speed
                    num_visited += 1
                    flag = False
                    break
                queue.append([ID, queue[min][2] + dist/speed + dists[ID][case], queue[min][2] + dist/speed, queue[min][0]])
                num_visited += 1

        trace[queue[min][0]] = queue[min][3]
        if flag == False: 
            break
        queue.pop(min)

    path = [end]
    while trace[path[0]] != 0:
        path.insert(0, trace[path[0]])

    return path, d, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
