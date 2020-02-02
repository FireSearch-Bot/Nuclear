tokens = []

def openFile(filename):
  data = open(filename,"r").read()
  return data

def lex(data):
  data = list(data)
  tok = ""
  string = ""
  state = 0
  comment = 0
  for char in data:
    tok += char
    if tok == " " or tok == "(" or tok == ")" or tok == ";":
      if state == 0:
        tok = ""
      else:
        tok = " "
    elif tok == "\n":
      tok = ""
    elif tok == "//":
      if comment == 0:
        comment = 1
        tok = ""
      elif comment == 1:
        comment = 0
        tok = ""
    elif comment == 1:
      tok = ""
    elif tok.lower() == "print":
      tokens.append("PRINT")
      tok = ""
    elif tok == "\"" or tok == "'":
      if state == 0:
        state = 1
      elif state == 1:
        tokens.append("STRING:" + string + "\"")
        string = ""
        state = 0
        tok = ""
    elif state == 1:
      string += tok
      tok = ""
  return tokens
  #print(tokens)

def parse(toks):
  i = 0
  while (i < len(toks)):
    if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING":
      print(toks[i+1][7:].replace("\"","").replace("'",""), end="")
      i+=2

def run(filename):
  data = openFile(filename)
  toks = lex(data)
  parse(toks)

run("file.nuke")
