__author__ = 'antonellacalvia'

from .node import *
from TopCompiler import IfExpr

class If(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

        self.returnTo = ""
        self.next = ""
        self.returnVar = ""
        self.var = ""
        self.ternary = False
        self.yielding = False

    def __str__(self):
        return "IF"

    def compileToJS(self, codegen):
        if self.ternary:
            codegen.append("(")
            for i in self.nodes:
                i.compileToJS(codegen)
            codegen.append(")")
        elif self.type != Types.Null() and not self.yielding:
            codegen.append("(function(){")
            for i in self.nodes:
                i.compileToJS(codegen)
            codegen.append("})()")
        else:
            if self.yielding:
                codegen.count += 1
                self.ending = str(codegen.count)

                for i in self.nodes:
                    i.yielding = True

            count = 0
            _l = len(self.nodes)
            while count < _l:
                if self.yielding and count > 1:
                    codegen.append("/*if*/")
                    self.outer_scope.case(codegen, self.next)
                    codegen.append("/*notif*/")

                self.nodes[count].compileToJS(codegen)
                self.nodes[count+1].compileToJS(codegen)

                count += 2

            if self.yielding:
                self.outer_scope.case(codegen, self.ending)


    def validate(self, parser):
        if self.type != Types.Null():
            if len(self.nodes) <= 2:
                self.nodes[-1].nodes[-1].error("expecting else")

class IfCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False

    def __str__(self):
        return "ifCondition"

    def compileToJS(self, codegen):
        if self.owner.ternary:
            if self.owner.nodes[0] != self:
                codegen.append(":(")
            self.nodes[0].compileToJS(codegen)
            codegen.append("?")
        else:
            codegen.append(""+("else " if self.owner.nodes[0] != self else "")+"if(")
            self.nodes[0].compileToJS(codegen)
            codegen.append("){")

    def validate(self, parser):
        if len(self.nodes) != 1:
            self.error( "expecting single boolean expression")

        if self.nodes[0].type != Types.Bool():
            self.nodes[0].error("expecting boolean expression not " + str(self.nodes[0].type))

class Else(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.ternary = False
        self.yielding = False

    def __str__(self):
        return "else"

    def compileToJS(self, codegen):
        if self.yielding:
            codegen.append("{")
        elif self.owner.ternary:
            codegen.append(":(")
        else:
            codegen.append("\nelse{")

    def validate(self, parser): pass

class While(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "While"

    def compileToJS(self, codegen):
        for i in self.nodes:
            i.compileToJS(codegen)

    def validate(self, parser): pass

class WhilePreCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "WhilePreCondition"

    def compileToJS(self, codegen):
        codegen.append("\nwhile(")

    def validate(self, parser): pass

class Break(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return " break"

    def compileToJS(self, codegen):
        codegen.append("break;")

    def validate(self, parser): pass

class Continue(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "continue"

    def compile(self, codegen):
        return "br label "+self.owner.owner.check+"\n"

    def compileToJS(self, codegen):
        codegen.append(" continue;")

    def validate(self, parser): pass

class WhileCondition(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "WhileCondition"

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)
        codegen.append("){")

    def validate(self, parser):
        cond = self
        IfExpr.isBoolCondition(parser, cond)

class WhileBlock(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)

    def __str__(self):
        return "block"

    def compileToJS(self, codegen):
        for i in self.nodes:
            i.compileToJS(codegen)
        codegen.append("}")

    def validate(self, parser):
        checkUseless(self)

class Block(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.noBrackets = False
        self.yielding = False

    def __str__(self):
        return "block"

    def case(self, codegen, number):
        codegen.append("}")

        num = codegen.count + 1

        codegen.count += 1
        codegen.append(self.body._context + "=" + str(num) + ";break;")
        self.owner.next = num


        self.outer_scope.case(codegen, number)
        self.yielding = True

    def compileToJS(self, codegen):
        if not self.noBrackets and self.owner.ternary:
            self.nodes[0].compileToJS(codegen)
            if self == self.owner.nodes[-1]:
                codegen.append(")")
        elif self.type != Types.Null():
            for i in self.nodes[:-1]:
                i.compileToJS(codegen)

            if not self.yielding:
                codegen.append("return ")
                self.nodes[-1].compileToJS(codegen)
                codegen.append(";}")
            else:
                if not (type(self.nodes[-1]) is Tree.FuncCall and self.nodes[-1].nodes[0].type.do):
                    codegen.append(self.body.res+"=")
                self.nodes[-1].compileToJS(codegen)

                if self == self.owner.nodes[-1]:
                    codegen.append(";}")
        else:
            for i in self.nodes:
                i.compileToJS(codegen)

            if not self.noBrackets and not self.yielding: codegen.append(";}")

        if self.yielding:
            codegen.append(";"+self.body._context + "=" + self.owner.ending + ";/*block*/break;")

    def validate(self, parser):
        checkUseless(self)