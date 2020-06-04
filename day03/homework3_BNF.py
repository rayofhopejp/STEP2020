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

class Evaluation:
  def __init__(self,tokens):
    self.itr=0
    self.tokens=tokens
    self.size=len(tokens)
  def num(self):
    if self.tokens[self.itr]['type']=='MINUS':#優先度が一番高い、数字の符号としてのマイナス
      if self.tokens[self.itr+1]['type']=='NUMBER':
        self.itr+=2
        return -self.tokens[self.itr-1]['number']
      if self.tokens[self.itr+1]['type']=='LEFT':
        self.itr+=1
        return -self.bracket()
    if self.tokens[self.itr]['type']=='NUMBER':#数字
      self.itr+=1
      return self.tokens[self.itr-1]['number'] 
    else:
      print('Invalid syntax:',self.tokens[self.itr])
      exit(1)
  def bracket(self):
    ret=None
    if self.tokens[self.itr]['type']=='LEFT':
      self.itr+=1
      ret=self.plusminus()
      if self.itr>=self.size or self.tokens[self.itr]['type']!='RIGHT':
        print('Invalid syntax: There is lack of right bracket')
        if self.itr<self.size:
          print(self.tokens[self.itr]['type'])
        exit(1)
      self.itr+=1
    else:
      ret=self.num()
    return ret
  def muldiv(self): 
    ans=self.bracket()
    while self.itr<self.size and self.tokens[self.itr]['type'] in ['MUL','DIV']:
      self.itr+=1
      if self.tokens[self.itr-1]['type']=='MUL':
        ans*=self.bracket()
      if self.tokens[self.itr-1]['type']=='DIV':
        denomi=self.bracket()
        if denomi==0:
          print('Divide by zero')
          exit(1)
        ans/=denomi
    return ans
  def plusminus(self): 
    ans=self.muldiv()
    while self.itr<self.size and self.tokens[self.itr]['type'] in ['PLUS','MINUS']:
      self.itr+=1
      if self.tokens[self.itr-1]['type']=='PLUS':
        ans+=self.muldiv()
      if self.tokens[self.itr-1]['type']=='MINUS':
        ans-=self.muldiv()
    return ans
  def calc(self):
    self.itr=0
    return self.plusminus()

def evaluate(tokens):
  return Evaluation(tokens).calc()


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
  print("==== 発展:括弧の前にマイナスが入ってる物を掛け算割り算するパターン（とてもきつい） ====")
  test("(3.0+4*-(2-1))/5")
  print("==== 発展CLEAR!!!====\n")


runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)