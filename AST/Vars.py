__author__ = 'antonellacalvia'

from .node import *
from .Func import *
from .Struct import *
from TopCompiler import Scope
import AST as Tree

class Create(Node):
    def __init__(self, name, varType, parser):
        Node.__init__(self, parser)
        self.name = name
        self.names = []

        self.varType = varType
        self.isGlobal = False
        self.extern = False
        self.escapes = False
        self.attachTyp = False
    def __str__(self):
        return self.name + ": "+str(self.varType)

    def compileToJS(self, codegen):

        if type(self.owner) is FuncBraceOpen:
            codegen.append(codegen.createName(self.package+"_"+self.name))
            return

        if self.attachTyp:
            codegen.out_parts.append("var " + self.attachTyp.package+"_"+self.attachTyp.normalName+"_"+self.name+";")
        elif not self.isGlobal: codegen.append("var "+codegen.createName(self.package+"_"+self.name)+";")
        else: codegen.out_parts.append("var "+self.package + "_" + self.name+";")

    def validate(self, parser): pass

class CreateAssign(Node):
    def __init__(self, parser):
        Node.__init__(self, parser)
        self.names = []
        self.extern = False

    def __str__(self):
        return "CreateAssign "

    def compileToJS(self, codegen):
        self.nodes[0].compileToJS(codegen)
        self.nodes[1].compileToJS(codegen)

        self = self.nodes[0]
        if self.attachTyp:
            attachTyp = self.attachTyp

            if self.owner.nodes[1].type is Types.FuncPointer:
                codegen.append(attachTyp.package+"_"+attachTyp.normalName+".prototype."+self.name+"=(function(")
                names = [codegen.getName() for i in self.owner.nodes[1].nodes[0].type.args]
                codegen.append(",".join(names)+"){return ")
                codegen.append(self.package + "_" + self.attachTyp.name+"_"+self.name+"("+",".join(["this"]+names)+")});")
            else:
                codegen.append(attachTyp.package+"_"+attachTyp.normalName+".prototype."+self.name+"="+
                attachTyp.package+"_"+attachTyp.normalName+"_"+self.name+";")

    def validate(self, parser): pass

class Assign(Node):
    def __init__(self, name, parser):
        Node.__init__(self, parser)
        self.name = name
        self.isGlobal = None
        self.extern = False

    def __str__(self):
        return self.name + "="

    def compileToJS(self, codegen):
        if type(self.owner) is Tree.InitStruct:
            self.nodes[1].compileToJS(codegen)
            return
        if self.init:
            name = self.package+"_"+self.name if self.isGlobal else codegen.readName(self.package + "_" + self.name)

            codegen.append(name + " = ")

            if self.extern:
                codegen.append(self.nodes[0].toString()[1:-1])
            else:
                self.nodes[0].compileToJS(codegen)
            codegen.append(";")
        else:
            self.nodes[0].compileToJS(codegen)
            codegen.append("=")
            self.nodes[1].compileToJS(codegen)
            codegen.append(";")

    def validate(self, parser):
        node = self
        package = self.package

        if type(self.owner) is Tree.InitStruct:
            return

        if self.init:
            self.isGlobal = Scope.isGlobal(parser, self.package, self.name)
            createTyp = self.createTyp
        else:
            if type(self.nodes[0]) is Tree.ReadVar:
                if self.nodes[0].imutable:
                    self.nodes[0].error("cannot reassign to immutable variable "+self.nodes[0].name)
            elif type(self.nodes[0]) in [Tree.Field, Tree.ArrRead]:
                createTyp = self.nodes[0].nodes[0].type
                if not Types.isMutable(createTyp):
                    self.nodes[0].error("type "+str(createTyp)+" is not assignable")
            else:
                self.nodes[0].error("invalid syntax")

        if len(node.nodes) == 0:
           self.error( "expecting expression")
        if self.init:
            if len(node.nodes) > 1:
                self.error( "expecting single expression, not multiple")

            typ = node.nodes[0].type
        else:
            if len(node.nodes) > 2:
                self.error("expecting single expression, not multiple")
            typ = node.nodes[1].type

        if typ == Types.Null():
            self.nodes[0].error("cannot assign nothing")

class ReadVar(Node):
    def __init__(self, name, isGlobal, parser):
        Node.__init__(self, parser)
        self.name = name
        self.isGlobal = isGlobal

    def __str__(self):
        return "read " + self.name

    def compileToJS(self, codegen):
        if type(self.owner) is Tree.Field:
            pass #print(self.name)
        codegen.append(codegen.readName(
            self.package + "_" + self.name) if not self.isGlobal else
            (self.package+"_"+self.name if self.package != "" else self.name
        ))

    def validate(self, parser):
        pass