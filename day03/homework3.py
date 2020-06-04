def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  if index>0 and line[index-1] in ['*','/']:#*-(3とか
    index+=1
    token,index=readNumber(line,index)
    token['number']=-token['number']
    return token,index
  token = {'type': 'MINUS'}
  return token, index + 1

def readMul(line, index):
  token = {'type': 'MUL'}
  return token, index + 1

def readDiv(line, index):
  token = {'type': 'DIV'}
  return token, index + 1

def readL(line, index):
  token = {'type': 'LEFT'}
  return token, index + 1

def readR(line, index):
  token = {'type': 'RIGHT'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMul(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index)
    elif line[index] == '(':
      (token, index) = readL(line, index)
    elif line[index] == ')':
      (token, index) = readR(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

def evaluateplusminus(tokens): #このtokensの要素はPLUS,MINUS,NUMBERだけ
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  answer=0
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax:',tokens[index-1],tokens)
        exit(1)
    index += 1
  return [{'type': 'NUMBER','number':answer}]

def evaluatemuldiv(tokens):#このtokensの要素はPLUS,MINUS,MUL,DIV,NUMBERだけ
  plusminustokens=[]
  index=0
  while index < len(tokens):
    smallans=None
    if tokens[index]['type']=='NUMBER':
      smallans=tokens[index]['number']
      index+=1
    while index < len(tokens) and tokens[index]['type'] in ['MUL','DIV']:
      assert(index+1<len(tokens))
      if tokens[index]['type'] == 'MUL':
        smallans *= tokens[index+1]['number']
      elif tokens[index]['type'] == 'DIV':
        smallans /= tokens[index+1]['number']
      index+=2
    if smallans==None:
      plusminustokens.append(tokens[index])
      index+=1
    else:
      plusminustokens.append({'type':'NUMBER','number':smallans})
  return evaluateplusminus(plusminustokens)

def evaluatebracket(tokens):#このtokensの要素は(),PLUS,MINUS,MUL,DIV,NUMBER全て含む
  index=0
  left_bracket=len(tokens)+1
  bracket_level=0
  while index < len(tokens): #最も外側の括弧を探す
    if tokens[index]['type']=='LEFT':
      left_bracket= index if bracket_level==0 else left_bracket
      bracket_level+=1
    elif tokens[index]['type']=='RIGHT':
      bracket_level-=1
      if bracket_level==0:
        tokens[left_bracket:index+1]=evaluatebracket(tokens[left_bracket+1:index])#最も外側の括弧の中身を抽出して計算する
        index=left_bracket
    index+=1
  #括弧を全て取り除けたら、掛け算割り算から計算する
  tokens=evaluatemuldiv(tokens)
  return tokens
    

        

def evaluate(tokens):
    single_token=evaluatebracket(tokens)
    assert(len(single_token)==1)
    assert(single_token[0]['type']=='NUMBER')
    return single_token[0]['number']


def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("0.3")
  test("1+2")
  test("1.0+2.1-3")
  test("3.0+4*2-1/5*2")
  test("3.0+4*2-1/5*2/3")
  test("3.0+4*2-1/5*4*5")
  test("-3.0+4*-2-1/5*2")#発展:マイナスの数をかける
  test("-3.0+4*2-1/-5*2")#発展:マイナスの数でわる
  #()が入ったテストケース
  test("(2+3)")
  test("(2+3)*4")
  test("(3.0+4*(2-1))/5")
  test("3.0+4/2/3/5*2*(2-1)/5")
  test("(3.0+4*(3.0+4*(3.0+4*(3.0+4*(2-1)))))/5")
  print("==== Test finished! ====\n")
  print("==== 発展:括弧の前にマイナスが入ってる物を掛け算割り算するパターン（とてもきつい） ====\n")
  test("(3.0+4*-(2-1))/5")
  
runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)