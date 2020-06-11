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

import queue
import heapq
def count_betweeness_Brandes(graph):#ノード、辺の媒介中心性の計算
    edge_betweeness={}#(from,to):edge betweeness
    for frm,tos in graph.items():#全てのノードを追加
        for to,cost in tos:
            edge_betweeness[(frm,to)]=0
    #algorithm:https://www.eecs.wsu.edu/~assefaw/CptS580-06/papers/brandes01centrality.pdf
    #は頂点の媒介中心性を求めているので、それを辺にも応用したもの
    #ちなみにノードの中心媒介性はそのまま用いてもノードの重要度の指標になりそう。
    C_b={k:0 for k in graph.keys()}
    for s in graph.keys():
        P={k:[] for k in graph.keys()} #P[v]:頂点vに向かう最短経路において前に通った頂点のリスト
        sigma={k:0 for k in graph.keys()}#最短経路の数
        sigma[s]=1
        d={k:-1 for k in graph.keys()}#P[v]:sからvへの最短距離
        d[s]=0
        #ここは普通にDijkstraを行っている
        Q=[]
        heapq.heapify(Q)
        heapq.heappush(Q, (0,s))
        while len(Q)>0:
            #print(Q)
            nowcost,v=heapq.heappop(Q)
            if d[v]<nowcost:
                continue
            assert(d[v]==nowcost)
            for w,cost in graph[v]:
                if d[w]<0:
                    d[w]=d[v]+cost
                    heapq.heappush(Q, (d[w],w))
                if d[w]==d[v]+cost:
                    P[w].append(v)
                    sigma[w]+=sigma[v]
                if d[w]>d[v]+cost:
                    d[w]=d[v]+cost
                    heapq.heappush(Q, (d[w],w))
                    P[w]=[v,]#今までの記録は捨てる
                    sigma[w]=sigma[v]#今までの記録は捨てる
        #Sは全ての到達できるノードがsから近い順に並んでいる状態にする
        S=[k for k,v in sorted(d.items(), key=lambda x:x[1])]#最短経路長でソート
        delta={k:0 for k in graph.keys()}#これはsを始点とした時の頂点kの媒介中心性が求まる
        delta_edge={k:0 for k in edge_betweeness.keys()}#これはsを始点とした時のedgeの媒介中心性が求まる
        while len(S)>0:
            to=S.pop()#これは必ずsから遠い順に取り出される
            #print(d[to],end=",")
            for frm in P[to]:#toの前に通った頂点frmに対して
                delta[frm]+=sigma[frm]/sigma[to]*(1+delta[to])
                #toの媒介中心性(決定済み)にsigma[frm]/sigma[to]をかければ辺の媒介性が求まる
                edge_betweeness[(frm,to)]+=(sigma[frm]/sigma[to])*delta[to]
            if to!=s:
                C_b[to]+=delta[to]
    return C_b,edge_betweeness


def connected_groups(graph_directed):
    #連結であるとは、そのグループの中のどの2頂点を選んでもどちらか一方向に道が存在することとする。
    #無向グラフにしておく（ちょっとアレな手法かもしれない…）
    graph=copy.deepcopy(graph_directed)
    for frm,tos in graph.items():
        for to in tos:
            if frm not in graph[to]:
                graph[to].append(frm)
    groups=[]
    not_connected=[k for k in graph.keys()]
    while len(not_connected)>0:#全てのノードを始点としてBFSを行う
        start=not_connected.pop()
        group=[start,]
        now=[start,] 
        visited={ k:0 for k in graph.keys()}
        visited[start]=1
        count=0
        while len(now)>0:
            count+=1
            nxt=[]
            for i in now:
                for next_node in graph[i]: 
                    if  visited[next_node]==0:
                        group.append(next_node)
                        assert(next_node in not_connected)#無向グラフならこの条件を満たすはず
                        not_connected.remove(next_node)
                        visited[next_node]=1
                        nxt.append(next_node)
            now=nxt
        groups.append(group)
    return groups

#Nグループに分割する（Girvan-Newman法）→授業のグループとの関係が見えるのでは
def grouping_girvan_newman(graph,N):
    new_graph=copy.deepcopy(graph)
    connected_groups_now=connected_groups(new_graph)
    #最初の連結成分
    print("初期状態：")
    print(str(len(connected_groups_now))+"groups",*connected_groups_now,sep='\n')
    while True:
        groups=[]
        #1.残っている全てのリンクのedge betweennessを計算する
        #node_betweenessは、ある頂点が任意の2ノード間の最短パスに含まれる回数。（ただし自分が始点、終点であるものは除く）
        #edge_betweenessは、ある辺が任意の2ノード間の最短パスに含まれる回数
        node_betweeness,edge_betweeness=count_betweeness_Brandes(new_graph)
        #「到達できる場合最短経路長は必ず1である状態」になったらそれ以上の分類は不可能なので
        #辺を切ることをやめる
        if max(node_betweeness.values())==0:
            print("到達できる場合最短経路長は必ず1である状態です。")
            connected_groups_now=connected_groups(new_graph)
            return len(connected_groups_now),connected_groups(new_graph)
        #2.そうでない場合、最もedge betweenessが高いリンクを切る。
        max_edge_from,max_edge_to=max(edge_betweeness, key=edge_betweeness.get)
        #print("removed:",max_edge_from,max_edge_to,edge_betweeness[(max_edge_from,max_edge_to)])
        new_graph[max_edge_from].remove(max_edge_to)
        #3.1-2を、連結成分がN個になるまで繰り返す。
        connected_groups_now=connected_groups(new_graph)
        if len(connected_groups_now)>=N:
            return len(connected_groups_now),connected_groups_now


graph=read_graph_data("./transit_links/edges.txt","./transit_links/stations.txt")
print("=====TEST start=====")
route,duration=dijkstra(graph,"新宿","四ツ谷")
print(route,duration,"分")
route,duration=dijkstra(graph,"新宿","四谷")
print(route,duration,"分")
route,duration=dijkstra(graph,"千葉","赤羽岩淵")
print(route,duration,"分")
print("=====TEST end=====")
print("最も媒介中心性が高い駅を見つけました")
#Todo:このアルゴリズムだと辺に重みがあるとき正確に媒介中心性が高い駅が見つけられていない
#なぜならSから取り出す順番が必ずしも遠い順とは限らなくなっているから
#あとでcount_betweeness_BrandesをBFSからDijkstraに切り替えておく（木曜日の夜には間に合わなかったので）
node_betweeness,edge_betweeness=count_betweeness_Brandes(graph)
#print(node_betweeness)
important_station=max(node_betweeness, key=node_betweeness.get)
print(important_station)
#ちなみに
print("終着点の媒介中心性は必ず0になっているはずである。")
#例えば
print("「三鷹」の媒介中心性",node_betweeness["三鷹"])

if __name__=='__main__':
    while True:
        station_from=input("from:")
        station_to=input("to:")
        route,duration=dijkstra(graph,station_from,station_to)
        print(route,duration,"分")