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

def count_betweeness(graph): 
    edge_betweeness={}#(from,to):edge betweeness
    for frm,tos in graph.items():#全てのノードを追加
        for to in tos:
            edge_betweeness[(frm,to)]=0
    for start in graph:#全てのノードを始点としてBFSを行う
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
                        #通ったことをカウント
                        edge_betweeness[(i,next_node)]+=1
                        visited[next_node]=1
                        nxt.append(next_node)
            now=nxt
    return edge_betweeness

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
    #print(len(connected_groups_now),connected_groups_now,sep='groups\n')
    while True:
        groups=[]
        #1.残っている全てのリンクのedge betweennessを計算する。
        #edge_betweenessは、任意の2ノード間の最短パスに含まれる回数
        edge_betweeness=count_betweeness(new_graph)
        #2.最もedge betweenessが高いリンクを切る。
        max_edge_from,max_edge_to=max(edge_betweeness, key=edge_betweeness.get)
        new_graph[max_edge_from].remove(max_edge_to)
        #3.1-2を、連結成分がN個になるまで繰り返す。
        connected_groups_now=connected_groups(new_graph)
        if len(connected_groups_now)>=N:
            return len(connected_groups_now),connected_groups_now


if __name__=='__main__':
    #graphは隣接リスト
    graph=read_graph_data("./sns_links/links.txt","./sns_links/nicknames.txt")
    print("Calcurate shortest distance... please input nicknames")
    nickname_from=input("from:")
    nickname_to=input("to:")
    print(isConnected_BFS(graph,nickname_from, nickname_to))
    print("Divide members to N groups:")
    N=int(input("N:"))
    print(*grouping_girvan_newman(graph,N),sep='groups\n')