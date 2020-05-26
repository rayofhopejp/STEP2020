def count_characters(words):
    dic={}
    for word in words:
        cnt=[0]*26
        for c in word:
            cnt[ord(c)-ord('a')]+=1
        dic[word]=cnt
    return dic

#"words" and "charactors" are consist of lowercases.
def main(words,characters):
    print(characters)
    char_count=[characters.count(chr(ord('a')+i)) for i in range(26)]
    char_count_dict=count_characters(words)
    ans=[]
    for k,v in char_count_dict.items():
        for i in range(26):
            if v[i]>char_count[i]:
                break
            if i==26-1:
                ans.append(k)
    return ans

if __name__ == '__main__':
    path="./dictionary.words"
    f=open(path)
    words=[line.strip().lower() for line in f.readlines()]
    charactors=input().strip().lower()
    print( main(words,charactors) )
    