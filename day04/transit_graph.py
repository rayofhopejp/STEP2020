#グラフは隣接リストで実装する
#グラフの読み込み
def read_graph_data(linksfile,namesfile):
    lf = open(linksfile)
    nf = open(namesfile)
    names=dict([line.strip().split() for line in nf.readlines()])
    nodelist={v:[] for v in names.values()} #dict
    for line in lf.readlines():
        n_from,n_to,cost=line.strip().split()
        nodelist[ names[n_from] ].append([names[n_to],int(cost)])
        nodelist[ names[n_to] ].append([names[n_from],int(cost)])
    lf.close()
    nf.close()
    return nodelist

#dijkstra法により最短経路を求める
#優先度付きキューを用いて計算量はE+Vlog(V)
import heapq
def dijkstra(graph,start,end):
    if start not in graph.keys() or end not in graph.keys():
        return "そのような駅は存在しません",-1
    INF=1001001001
    distances={k:INF for k in graph.keys()}
    prev_node={k:-1 for k in graph.keys()}
    #最短距離を求める
    que=[(0,start),]
    heapq.heapify(que)
    while len(que)>0:
        now_cost,now_node=heapq.heappop(que)
        if now_cost>distances[now_node]:
            continue
        for next_node,cost in graph[now_node]:
            if now_cost+cost<distances[next_node]:
                distances[next_node]=now_cost+cost
                prev_node[next_node]=now_node
                heapq.heappush(que, (now_cost+cost,next_node))
    #最短経路を求める
    if distances[end]==INF:
        return "到達できません",-1
    now_node=end
    route=[end,]
    while now_node!=start:
        assert(now_node in prev_node.keys())
        now_node=prev_node[now_node]
        route.append(now_node)
    return list(reversed(route)),distances[end]

graph=read_graph_data("./transit_links/edges.txt","./transit_links/stations.txt")
route,duration=dijkstra(graph,"新宿","四ツ谷")
print(route,duration,"分")
route,duration=dijkstra(graph,"新宿","四谷")
print(route,duration,"分")
route,duration=dijkstra(graph,"千葉","赤羽岩淵")
print(route,duration,"分")