__author__ = 'antonellacalvia'

from TopCompiler import Parser
from TopCompiler import Error
import AST as Tree
from TopCompiler import Scope
import copy
from TopCompiler import ExprParser
from TopCompiler import VarParser
from TopCompiler import Types
from TopCompiler import MethodParser
import collections as coll

def parserMethodGen(parser, gen, struct):
    sgen = struct.generic

    if len(gen) > len(sgen):
        Error.parseError(parser, str(len(gen)-len(sgen))+" generic arguments too many")
    elif len(gen) < len(sgen):
        Error.parseError(parser, str(len(gen) - len(sgen)) + " generic arguments too few")

    newGen = coll.OrderedDict()
    for a, b in zip(gen, sgen):
        if gen[a].type != Types.All: Error.parseError(parser, "unexpected :")
        newGen[a] = sgen[b]
        Scope.changeType(parser, a, sgen[b])

    return newGen

def generics(parser):
    generic = coll.OrderedDict()

    while parser.thisToken().token != "]":
        name = parser.nextToken().token

        typ = Types.T(name, Types.All)
        if parser.thisToken().type != "identifier":
            Error.parseError(parser, "type name must be an identifier")

        if not parser.nextToken().token in [":", ",", "]"]:
            Error.parseError(parser, "expecting ,")

        if parser.thisToken().token == ":":
            parser.nextToken()
            typ = Types.T(name, Types.parseType(parser))

            if parser.lookInfront().token != "]":
                parser.nextToken()

        Scope.addVar(Tree.PlaceHolder(parser), parser, name, Scope.Type(False, typ))
        generic[name] = typ

        if parser.lookInfront().token == "]":
            parser.nextToken()
            break

    parser.nextToken()
    return generic

def funcHead(parser, decl= False, dontAdd= False, method= False, attachTyp = False):
    Scope.incrScope(parser)
    if not type(parser.currentNode) is Tree.Root and not decl:
        Error.parseError(parser, "unexpected def")
    if parser.tokens[parser.iter+2].token == ".":
        if attachTyp: Error.parseError(parser, "unexpected .")
        parser.nextToken()
        attachTyp = Types.parseType(parser)
        parser.nextToken()
        return MethodParser.methodHead(parser, attachTyp, decl)
    name = parser.nextToken()

    if name.type != "identifier":
        Error.parseError(parser, "function name must be of type identifier, not "+name.type)
    parser.nextToken()

    name = name.token

    g = {}
    if parser.thisToken().token != "(":
        if parser.thisToken().token == "[":
            g = generics(parser)
            if parser.thisToken().token == ".":
                if attachTyp: Error.parseError(parser, "unexpected .")
                if not Scope.varExists(parser, parser.package, name): Error.parseError(parser,
                     "cannot attach method to unknown type main."+name)

                attachTyp = Types.Struct(False, name, parser.structs[parser.package][name].types, parser.package, parserMethodGen(parser, g, parser.structs[parser.package][name]))

                f = funcHead(parser, decl, dontAdd, True, attachTyp)
                Scope.decrScope(parser)

                return f

        if parser.thisToken().token != "(":
            Error.parseError(parser, "expecting (")

    header = Tree.FuncStart(name, Types.Null(), parser)
    header.package = parser.package
    parser.currentNode.addNode(header)

    brace = Tree.FuncBraceOpen(parser)
    brace.name = name
    brace.package = parser.package

    parser.currentNode.addNode(brace)

    parser.currentNode = brace

    if method:
        typ = attachTyp
        self = parser.nextToken()
        if self.type != "identifier": Error.parseError(parser, "binding name must be identifier not "+self.type)
        self = self.token

        selfNode = Tree.Create(self, typ, parser)
        selfNode.package = parser.package
        selfNode.imutable = True

        parser.currentNode.addNode(selfNode)

        if not parser.lookInfront().token in [")", ","]:
            Error.parseError(parser, "expecting comma not "+parser.thisToken().token)


    if name[0].lower() != name[0]:
        Error.parseError(parser, "function name must be lower case")

    returnType = Types.Null()

    parser.paren += 1
    parser.nextToken()

    while parser.paren != parser.parenBookmark[-1] :
        b = parser.thisToken().token
        if b == ",":
            parser.nextToken()
            continue
        elif b == ")":
            parser.paren -= 1
            parser.nextToken()
            continue
        elif b == "(":
            Error.parseError(parser, "unexpected (")
        Parser.declareOnly(parser)
        parser.nextToken()

    t = parser.thisToken()
    if t.token != "=" :
        returnType = Types.parseType(parser)

        if parser.nextToken().token != "=":
            Error.parseError(parser, "expecting =")

    parser.currentNode = brace.owner

    names = [i.name for i in brace.nodes]
    types = [i.varType for i in brace.nodes]

    if method:
        func = Types.FuncPointer(
            types,
            returnType,
            g
        )

        header.method = True
        header.types = types[1:]
        header.attachTyp = attachTyp
        header.normalName = name
        header.name = attachTyp.normalName+"_"+header.normalName

        MethodParser.checkIfOperator(parser, attachTyp, name, func)

        if decl:
            MethodParser.addMethod(brace, parser, attachTyp, name, func)

        return attachTyp.normalName+"_"+name, names, types, header, returnType

    parser.func[parser.package][name] = Types.FuncPointer(
        types,
        returnType,
        g
    )

    if decl:
        if not dontAdd:
            Scope.addFunc(header, parser, name, Types.FuncPointer(types, returnType, g))


    return name, names, types, header, returnType

def funcBody(parser, name, names, types, header, returnType):
    body = Tree.FuncBody(parser)
    body.name = name
    body.returnType = returnType
    body.package = parser.package

    parser.currentNode.addNode(body)
    parser.currentNode = body

    for i in range(len(names)):
        n = Tree.InitArg(names[i], body)
        n.package = parser.package
        n.varType = types[i]
        n.imutable = not Scope.isMutable(parser, parser.package, names[i])
        body.addNode(n)

    parser.nextToken()
    Parser.callToken(parser) #incase next case is newline

    while not Parser.isEnd(parser):
        parser.nextToken()
        t = parser.thisToken().token
        Parser.callToken(parser)

    ExprParser.endExpr(parser)

    parser.currentNode = body.owner

    Scope.decrScope(parser)

def func(parser):
    (name, names, types, header, returnType) = funcHead(parser)
    funcBody(parser, name, names, types, header, returnType)

def funcCallBody(parser, paren):
    def notParen():
        return not Parser.isEnd(parser)

    if paren :
        notEnd = lambda: parser.paren > parser.parenBookmark[-1]
    else:
        notEnd = notParen

    while notEnd():
        t = parser.nextToken()
        if t.token == "," :
            ExprParser.endExpr(parser)
            continue

        Parser.callToken(parser)

    if not paren:
        ExprParser.endExpr(parser)

def callFunc(parser,paren):

    tail = Tree.FuncCall(parser)

    tail.addNode(parser.currentNode.nodes[-1])

    tail.owner = parser.currentNode

    parser.currentNode.nodes[-1] = tail
    parser.currentNode = tail

    if not paren:
        Parser.selectExpr(parser, parser.thisToken())

    funcCallBody(parser, paren)

    ExprParser.endExpr(parser)
    parser.currentNode = tail.owner

def genericT(parser):
    parser.nextToken()
    if len(parser.currentNode.nodes) > 0:
        func = parser.currentNode.nodes.pop()
    else:
        Error.parseError(parser, "unexpected ::")

    generic = Tree.Generic(parser)
    parser.currentNode.addNode(generic)
    generic.addNode(func)

    generic.generic = []

    if parser.thisToken().token != "[":
        Error.parseError(parser, "expecting [")

    parser.nextToken()

    while parser.thisToken().token != "]":
        if parser.thisToken().token == ",":
            parser.nextToken()
            continue

        generic.generic.append(Types.parseType(parser))
        t = parser.thisToken().token
        parser.nextToken()

Parser.stmts["def"] = func
Parser.exprToken["none"] = lambda parser: Error.parseError(parser, "unexpected type none")
Parser.exprToken[","] = lambda  parser: Error.parseError(parser, "unexpected ,")
Parser.exprToken["_"] = lambda parser: parser.currentNode.addNode(Tree.Under(parser))
Parser.exprToken["::"] = genericT