from collections import defaultdict
import sys
import numpy as np


class Heap():

    def __init__(self):
        self.arraylist = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapMinHeapNode(self, a, b):
        t = self.arraylist[a]
        self.arraylist[a] = self.arraylist[b]
        self.arraylist[b] = t

    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if (left < self.size and
                self.arraylist[left][1]
                < self.arraylist[smallest][1]):
            smallest = left

        if (right < self.size and
                self.arraylist[right][1]
                < self.arraylist[smallest][1]):
            smallest = right

        if smallest != idx:
            self.pos[self.arraylist[smallest][0]] = idx
            self.pos[self.arraylist[idx][0]] = smallest

            self.swapMinHeapNode(smallest, idx)

            self.minHeapify(smallest)

    def extractMin(self):

        if self.isEmpty() == True:
            return

        root = self.arraylist[0]

        lastNode = self.arraylist[self.size - 1]
        self.arraylist[0] = lastNode

        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist):

        i = self.pos[v]

        self.arraylist[i][1] = dist

        while (i > 0 and self.arraylist[i][1] <
               self.arraylist[(i - 1) // 2][1]):
            self.pos[self.arraylist[i][0]] = (i - 1) // 2
            self.pos[self.arraylist[(i - 1) // 2][0]] = i
            self.swapMinHeapNode(i, (i - 1) // 2)

            i = (i - 1) // 2;

    def isInMinHeap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


def printArr(dist, n):
    print("Vertex\tDistance from source")
    for i in range(n):
        print("%d\t\t%d" % (i, dist[i]))


class Graph():

    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
        self.gra = defaultdict(list)

    def addEdge(self, src, dest, weight):
        self.gra[src].append(dest)
        self.gra[dest].append(src)
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    def DFSUtil(self, v, visited):

        visited.add(v)

        print(v, end=' ')

        for neighbour in self.gra[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    def print_DFS(self, v):

        visited = set()

        self.DFSUtil(v, visited)

    def dijkstra(self, src):

        V = self.V
        dist = []

        minHeap = Heap()

        for v in range(V):
            dist.append(1e7)
            minHeap.arraylist.append(minHeap.newMinHeapNode(v, dist[v]))

            minHeap.pos.append(v)

        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])

        minHeap.size = V

        while minHeap.isEmpty() == False:

            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]

            for pCrawl in self.graph[u]:

                v = pCrawl[0]

                if (minHeap.isInMinHeap(v) and
                        dist[u] != 1e7 and \
                        pCrawl[1] + dist[u] < dist[v]):
                    dist[v] = pCrawl[1] + dist[u]

                    minHeap.decreaseKey(v, dist[v])
        return dist
        # printArr(dist, V)


if __name__ == "__main__":
    print(
        ' 1 : two people in the cafe\n',
        '2 : more than two people in the cafe\n',
        '3 : test\n',
        '4 : Enter exit\n'
    )
    list_cofe = []
    person_list = []
    listnodes = []
    count = 0
    x = input()
    while x != 'exit':
        # V1 = -100
        # V2 = -100


        if x == '1':
            v, e = [int(x) for x in input().split()]
            nodes = [int(x) for x in input().split()]
            listnodes = list(nodes)
            V1 = nodes[0]
            V2 = nodes[-1]
            person_list.append(V1)
            person_list.append(V2)
            g = Graph(v)
            for i in range(0, e):
                v1, v2, w = [int(x1) for x1 in input().split()]
                g.addEdge(v1, v2, w)
                # graph.addEdge(v2, v1, w)
            a = g.dijkstra(V1)
            b = g.dijkstra(V2)
            dif = list(abs(np.array(a) - np.array(b)))
            temp = min(dif)
            res = [i for i, j in enumerate(dif) if j == temp]
            for i in res:
                print(i, end=" ")
            print()
            x = input()
        if x == '2':
            if count == 0:
                p, node = input().split()
                node = int(node)
            # while p != 'exit':
            if p == 'join':
                person_list.append(node)
                # print('person', person_list)
                list_cofe = set(listnodes) - set(person_list)
                # print('list_cofe', list_cofe)
                list = []
                for i in list_cofe:
                    # print('i= ', i)
                    a = 0
                    D = g.dijkstra(i)
                    # print(D)
                    s = []
                    for i in person_list:
                        s.append(D[i])
                    D = s
                    # print(D)
                    for j in range(0, len(person_list)):
                        for k in range(len(person_list) - 1, j, -1):
                            if i == k:
                                continue
                            # print(D[j], D[k])
                            a += abs(D[j] - D[k])
                    list.append(a)
                    # print('list ', list)
            t = min(list)
            r = [i for i, j in enumerate(list) if j == t]
            print(r)
            # if len(r) > 1000:
            #     for i in r:
            #         print(list_cofe[i])
            # x = input()
            P = [x for x in input().split()]
            x = P[0]
            if len(P) > 1:
                x = '2'
                count=1
                p = P[0]
                node = P[1]
                node = int(node)

            if p == 'left':
                node = int(node)
                # print(list_cofe)
                # print(person_list)
                if node in list_cofe:
                    list_cofe.remove(node)
                if node in person_list:
                    person_list.remove(node)
                # print(list_cofe)
                # print(person_list)
                # print(g.graph)
                # print(g.gra)
                if node in g.graph:
                    g.graph.pop(node)
                if node in g.gra:
                    g.gra.pop(node)
                # g.graph.pop(node)
                # g.gra.pop(node)
                for key, val in g.gra.items():
                    if node in val:
                        val.remove(node)
                for key, val in g.graph.items():
                    for i in val:
                        if node in i:
                            val.remove(i)

                l = []
                for i in list_cofe:
                    # print('i= ', i)
                    a = 0
                    D = g.dijkstra(i)
                    # print(D)
                    ss = []
                    for i in person_list:
                        ss.append(D[i])
                    D = ss
                    # print(D)
                    for j in range(0, len(person_list)):
                        for k in range(len(person_list) - 1, j, -1):
                            if i == k:
                                continue
                            # print(D[j], D[k])
                            a += abs(D[j] - D[k])
                    l.append(a)
                    # print('list ', l)
                t = min(l)
                r = [i for i, j in enumerate(l) if j == t]
                print(r)
                # if len(r) > 1000:
                #     for i in r:
                #         print(list_cofe[i])
                P = [x for x in input().split()]
                x = P[0]
                if len(P) > 1:
                    x = '2'
                    count = 1
                    p = P[0]
                    node = P[1]
                    node = int(node)

            # print(g.graph)
            # print(g.gra)

        if x == 'test':
            g.print_DFS(0)
            x = input()
            print()
        if x == 'exit':
            exit(0)


