import copy

#グラフは隣接リストで実装する
#グラフの読み込み
def read_graph_data(linksfile,namesfile):
    lf = open(linksfile)
    nf = open(namesfile)
    names=dict([line.strip().split() for line in nf.readlines()])
    nodelist={v:[] for v in names.values()} #dict
    for line in lf.readlines():
        n_from,n_to=line.strip().split()
        nodelist[ names[n_from] ].append(names[n_to])
    lf.close()
    nf.close()
    return nodelist

#adrianからあなたに行けるか？
def isConnected_BFS(graph,A,B): #AとBがグラフ上で連結しているかと、最短距離をBFSでもとめる
    #BFSは重みなしグラフの単一始点最短経路問題において最も効率が良いアルゴリズムである。
    if A not in graph or B not in graph:
        return "そのような人はいません"
    now=[A,] 
    visited={ k:0 for k in graph.keys()}
    visited[A]=1
    count=0
    if A==B:
        return count
    while len(now)>0:
        count+=1
        nxt=[]
        for i in now:
            for next_node in graph[i]: 
                if next_node==B:
                    return str(count)+"回辺を辿れば到達できます"
                if  visited[next_node]==0:
                    visited[next_node]=1
                    nxt.append(next_node)
        now=nxt
    return "到達できません"

import queue
def count_betweeness_Brandes(graph):#ノード、辺の媒介中心性の計算
    edge_betweeness={}#(from,to):edge betweeness
    for frm,tos in graph.items():#全てのノードを追加
        for to in tos:
            edge_betweeness[(frm,to)]=0
    #algorithm:https://www.eecs.wsu.edu/~assefaw/CptS580-06/papers/brandes01centrality.pdf
    #は頂点の媒介中心性を求めているので、それを辺にも応用したもの
    #ちなみにノードの中心媒介性はそのまま用いてもノードの重要度の指標になりそう。
    C_b={k:0 for k in graph.keys()}
    for s in graph.keys():
        S=[] #stack
        P={k:[] for k in graph.keys()} #P[v]:頂点vに向かう最短経路において前に通った頂点のリスト
        sigma={k:0 for k in graph.keys()}#最短経路の数
        sigma[s]=1
        d={k:-1 for k in graph.keys()}#P[v]:sからvへの最短距離
        d[s]=0
        #ここは普通にBFSを行っている
        Q=queue.Queue()
        Q.put(s)
        while not Q.empty():
            v=Q.get()
            S.append(v)#sから近い順に（最短距離が単調増加に）格納される
            for w in graph[v]:
                if d[w]<0:
                    Q.put(w)
                    d[w]=d[v]+1
                if d[w]==d[v]+1:
                    sigma[w]+=sigma[v]
                    P[w].append(v)
        delta={k:0 for k in graph.keys()}#これはsを始点とした時の頂点kの媒介中心性が求まる
        delta_edge={k:0 for k in edge_betweeness.keys()}#これはsを始点とした時のedgeの媒介中心性が求まる
        while len(S)>0:
            to=S.pop()#これは必ずsから遠い順に取り出される
            for frm in P[to]:#toの前に通った頂点frmに対して
                delta[frm]+=sigma[frm]/sigma[to]*(1+delta[to])
                #toの媒介中心性(決定済み)にsigma[frm]/sigma[to]をかければ辺の媒介性が求まる
                edge_betweeness[(frm,to)]+=(sigma[frm]/sigma[to])*delta[to]
            if to!=s:
                C_b[to]+=delta[to]
    return C_b,edge_betweeness

def nondirectize_graph(graph_directed):
    #連結であるとは、そのグループの中のどの2頂点を選んでもどちらにも道が存在することとする。
    #無向グラフにしておく（ちょっとアレな手法かもしれない…）
    graph_nondirected={k:[] for k in graph_directed.keys()}
    for frm,tos in graph_directed.items():
        for to in tos:
            if frm in graph_directed[to]:
                graph_nondirected[frm].append(to)
    return graph_nondirected


def connected_groups(graph_nondirected):
    #連結であるとは、そのグループの中のどの2頂点を選んでもどちらにもに道が存在することとする。
    #このグラフはもともと無向グラフ
    groups=[]
    not_connected=[k for k in graph_nondirected.keys()]
    while len(not_connected)>0:#全てのノードを始点としてBFSを行う
        
        start=not_connected.pop()
        group=[start,]
        now=[start,] 
        visited={ k:0 for k in graph_nondirected.keys()}
        visited[start]=1
        count=0
        while len(now)>0:
            count+=1
            nxt=[]
            for i in now:
                for next_node in graph_nondirected[i]: 
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
            connected_groups_now=connected_groups(nondirectize_graph(new_graph))
            return len(connected_groups_now),connected_groups_now
        #2.そうでない場合、最もedge betweenessが高いリンクを切る。
        max_edge_from,max_edge_to=max(edge_betweeness, key=edge_betweeness.get)
        #print("removed:",max_edge_from,max_edge_to,edge_betweeness[(max_edge_from,max_edge_to)])
        new_graph[max_edge_from].remove(max_edge_to)
        #3.1-2を、連結成分がN個になるまで繰り返す。
        connected_groups_now=connected_groups(nondirectize_graph(new_graph))
        if len(connected_groups_now)>=N:
            return len(connected_groups_now),connected_groups_now


if __name__=='__main__':
    #graphは隣接リスト
    Graph=read_graph_data("./sns_links/links.txt","./sns_links/nicknames.txt")
    print("Calcurate shortest distance... please input nicknames")
    nickname_from=input("from:")
    nickname_to=input("to:")
    print(isConnected_BFS(Graph,nickname_from, nickname_to))
    print("最も中心媒介性が高い人物を選びました。")
    node_betweeness,edge_betweeness=count_betweeness_Brandes(Graph)
    important_person=max(node_betweeness, key=node_betweeness.get)
    print(important_person)
    print("Divide members to N groups:")
    N=int(input("N:"))
    groupnum,groups=grouping_girvan_newman(Graph,N)
    print(groupnum,"groups:")
    print(*groups,sep='\n')
    