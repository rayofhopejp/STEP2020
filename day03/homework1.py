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
  if index>0 and line[index-1] in ['*','/']:#*-とか
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
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

def evaluateplusminus(tokens):
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
        print('Invalid syntax:',tokens[index-1])
        exit(1)
    index += 1
  return answer

def evaluatemuldiv(tokens):
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

def evaluate(tokens):
    return evaluatemuldiv(tokens)


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
  print("==== Test finished! ====\n")
runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)