## やったこと
①Best-fit・free-list連結の実装(free_listを双方向リストにしたのでメタデータが増えた)
②4KBが空になったらシステムに返却（今回はあまり効果がなかった）
③メタデータの部分にデータを詰めメタデータのサイズを単純実装時の1/3に削減(24byte->8byte)
## やりたかったけどできなかったこと
heapをそこに入れるfreeな領域のサイズごとに分割することで、mallocで割り当てる領域を探す際の計算量を減らしたかったのだが、
謎のエラーが出て完成させることができなかった。(デバッグ中のものをheap_shippai.cに置いておく。)
## 参考にしたもの
https://www.slideshare.net/kosaki55tea/glibc-malloc
のp53まで（バッファの遅延合体やマルチスレッドは触らなかった）
## 結果
### ①のみ
free_listを双方向リストにしたのでメタデータが増えてしまい、Challenge1,2で悪化した。
```
Challenge 1: simple malloc => my malloc
Time: 22 ms => 307 ms
Utilization: 70% => 67%
==================================
Challenge 2: simple malloc => my malloc
Time: 14 ms => 242 ms
Utilization: 40% => 31%
==================================
Challenge 3: simple malloc => my malloc
Time: 167 ms => 339 ms
Utilization: 8% => 37%
==================================
Challenge 4: simple malloc => my malloc
Time: 28534 ms => 1913 ms
Utilization: 15% => 73%
==================================
Challenge 5: simple malloc => my malloc
Time: 17745 ms => 1212 ms
Utilization: 15% => 75%
==================================
```
### ①②
全体的に多少の向上が見られた
```
Challenge 1: simple malloc => my malloc
Time: 12 ms => 225 ms
Utilization: 70% => 75%
==================================
Challenge 2: simple malloc => my malloc
Time: 16 ms => 122 ms
Utilization: 40% => 38%
==================================
Challenge 3: simple malloc => my malloc
Time: 144 ms => 170 ms
Utilization: 8% => 49%
==================================
Challenge 4: simple malloc => my malloc
Time: 25912 ms => 1808 ms
Utilization: 15% => 75%
==================================
Challenge 5: simple malloc => my malloc
Time: 22796 ms => 1194 ms
Utilization: 15% => 76%
==================================
```
### ①②③
Challenge2,3において飛躍的な結果の向上が見られた。
```
Challenge 1: simple malloc => my malloc
Time: 19 ms => 72 ms
Utilization: 70% => 75%
==================================
Challenge 2: simple malloc => my malloc
Time: 15 ms => 52 ms
Utilization: 40% => 53%
==================================
Challenge 3: simple malloc => my malloc
Time: 156 ms => 79 ms
Utilization: 8% => 60%
==================================
Challenge 4: simple malloc => my malloc
Time: 30637 ms => 7229 ms
Utilization: 15% => 72%
==================================
Challenge 5: simple malloc => my malloc
Time: 23748 ms => 2677 ms
Utilization: 15% => 76%
==================================
```
