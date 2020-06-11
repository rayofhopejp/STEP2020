# STEP class 4: SNS

## Name: Ray Oshikawa

## 調べたこと

- BFSにより、任意の二頂点間の最短経路長を求める
- 頂点の媒介中心性を求めることにより、多くの人の交流の架け橋になりそうな人（重要な人）を求める
- 辺の媒介中心性を用いてクラスタリングを行う

媒介中心性とは、「任意の二頂点の間を最短経路をたどって結んだ時その上にいる可能性の合計」です。（後述）

## 実行方法

1. ソースコードを置いたフォルダの中にフォルダ"sns_links"を作り、その下に"links.txt"と"nicknames.txt"を置きます
2. `$python3 SNS_graph.py`　を実行します

## 結果

以下のようになります。

adrianからedwin(私)へ到達するには三回辺をたどる必要がありました。

最も中心媒介性が高い、つまり「任意の二人の間を最短経路をたどって結んだ時その上にいる可能性が最も高い人物」は**jamie**さんでした！まだ直接繋がれていない人同士は、jamieさんのツテをたどって出会おうとすると効率がいいかもしれませんね:)

クラスタリングについては、小さなグループがいくつかできるというよりも、分割数Nを増やすほど1人ずつ大きなグループから外れていく形になりました。このSNSには派閥が存在せず、全体的に繋がれているという傾向があると思います！

```
from:adrian (←好きな人物を入力する)
to:edwin　(←好きな人物を入力する)
3回辺を辿れば到達できます
最も中心媒介性が高い人物を選びました。
jamie
Divide members to N groups:
N:30　(←好きな数字を入力する)
初期状態：
4groups
['luis', 'aaron', 'lance', 'dennis', 'francis', 'helen', 'howard', 'bruce', 'emma', 'jamie', 'kathleen', 'frances', 'herman', 'darryl', 'jerry', 'jimmie', 'diane', 'jon', 'duane', 'gene', 'jay', 'judith', 'cecil', 'edwin', 'janice', 'cody', 'kevin', 'cynthia', 'brett', 'jared', 'barry', 'debra', 'brenda', 'joel', 'eugene', 'danielle', 'jeremy', 'austin', 'johnnie', 'daniel', 'frederick', 'alexander', 'cheryl', 'jacqueline', 'jaime', 'jack', 'brent', 'hugh', 'adrian', 'joan', 'alan']
['lawrence']
['carolyn']
['betty']
10 groups:
['luis', 'aaron', 'dennis', 'howard', 'emma', 'jamie', 'frances', 'herman', 'francis', 'helen', 'darryl', 'jimmie', 'diane', 'kathleen', 'jon', 'jay', 'judith', 'lance', 'bruce', 'duane', 'debra', 'cody', 'eugene', 'danielle', 'gene', 'barry', 'austin', 'brett', 'janice', 'brenda', 'johnnie', 'frederick', 'jeremy', 'cynthia', 'jack', 'cecil', 'jacqueline', 'joel', 'jaime', 'alexander', 'hugh', 'brent', 'daniel', 'kevin', 'joan']
['lawrence']
['jerry']
['jared']
['edwin']
['cheryl']
['carolyn']
['betty']
['alan']
['adrian']
```

## 原理・アルゴリズム

媒介中心性を具体的な式で示すと、

$$b_{i} \equiv\sum_{i s=1 ; j s \neq i}^{N} \sum_{i_{i}=1 ; i \neq i}^{i s-1} \frac{g_{i}^{\left(i s i_{i}\right)}}{N_{i s i_{i}}}$$

（ただし$g_{i}^{\left(i_{s} i_{t}\right)}$は、ある頂点$v_{i_{s}}$から別の頂点$v_{i_{t}}$へ行く最短経路の中で$v_{i}$を通る数で、$N_{i_{s}i_{t}}$は$v_{i_{s}}$から$v_{i_{t}}$へ行く最短路の総数。）

求めるアルゴリズムは、重みなしグラフについては[A Faster Algorithm for Betweenness Centrality](https://www.eecs.wsu.edu/~assefaw/CptS580-06/papers/brandes01centrality.pdf)を参考にしました。

辺の媒介中心性はこの手法を少し改良すれば求めることができます。（SNS_graph.py, 78行目)

計算量は重 みなしグラフにおいて $O( nm+n^2 )$ 時間、重みありグラフにお いて $O(nm + n^2 \log n) $時間です。

媒介中心性を使ってコミュニティ分割する方法は、計算量が大きく、さらにどこまで分割するべきなのか($N$)を予め設定しなければいけないので、あまり実用には向いていないかもしれません。