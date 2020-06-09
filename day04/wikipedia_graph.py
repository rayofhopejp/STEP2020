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

graph=read_graph_data("./wikipedia_links/links.txt","./wikipedia_links/pages.txt")
print("読み込み完了")
print(graph["佐渡島"])