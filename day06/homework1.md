プログラム
```
aのid(定義後):  0x1044b2f88
bのid:  0x1044b2f88
bのid(append(2)後):     0x1044b2f88
bのid(+[3]後):  0x1046c7c48
bのid(append(4)後):     0x1046c7c48
b: [1, 2, 3, 4]
aのid(関数foo後):       0x1044b2f88
a: [1, 2]
```
結果
```
aのid(定義後):  0x1044b2f88
bのid:  0x1044b2f88
bのid(append(2)後):     0x1044b2f88
bのid(+[3]後):  0x1046c7c48
bのid(append(4)後):     0x1046c7c48
b: [1, 2, 3, 4]
aのid(関数foo後):       0x1044b2f88
a: [1, 2]
```

cast：スコープの中だと復元できそう