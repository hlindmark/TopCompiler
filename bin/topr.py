import js2py

from TopCompiler import CodegenJS as CodeGen
from TopCompiler import Lexer
from TopCompiler import Parser
from TopCompiler import ResolveSymbols
from TopCompiler import PackageParser
from TopCompiler import topc
import AST as Tree

import sys

def main():
    tokens = [[]]
    parser = Parser.Parser(tokens, [("main", "anonymous")])
    parser.compiled = {}
    parser.opt = 0
    parser.externFuncs = {"main": []}
    parser.repl = True
    PackageParser.packDec(parser, "main", pack=True)

    js = js2py.EvalJs()
    js.eval(CodeGen.getRuntimeNode())

    text = ""
    while True:
        line =  input("> ")
        text = line+"\n"
        topc.filenames_sources = {"main": {"anonymous": text}}
        try:
            tokens[0] = Lexer.tokenize(line, "anonymous")

            #ResolveSymbols.insert(parser, parser, only= True)
            parser.package = "main"
            parser.opackage = "main"

            t = parser.tokens
            f = parser.filename

            for i in range(3):
                ResolveSymbols._resolve(parser, tokens[0], "anonymous", i)

            parser.currentNode = Tree.Root()

            parser.tokens = t
            parser.filename = f

            parsed = parser.parse()

            compiled = (parsed, {"main": []})

            code = CodeGen.CodeGen("main", parsed, {"main": []}).toEval()
            #print(code)
            print(parsed.nodes[-1].type, ":", js.eval(code))
            tokens[0] = []
            parser.currentNode = Tree.Root()

        except EOFError as e:
            print(e)
            parser.iter += 1
main()
