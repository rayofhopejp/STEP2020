def foo(b):
    print("bのid:\t%#08x"%id(b))
    b.append(2)
    print("bのid(append(2)後):\t%#08x"%id(b))
    b = b + [3]
    print("bのid(+[3]後):\t%#08x"%id(b))
    b.append(4)
    print("bのid(append(4)後):\t%#08x"%id(b))
    print('b:', b)
a = [1]
print("aのid(定義後):\t%#08x"%id(a))
foo(a)
print("aのid(関数foo後):\t%#08x"%id(a))
print('a:', a)