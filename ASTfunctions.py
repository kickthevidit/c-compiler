import re
import symbol

SYMBOLS = ["program", "function", "statement", "expression", "id"]

LITERALS = ["#keyword", "#int"]

GRAMMAR_DICT = {"<program>": ("<function>",),
                "<function>": ("int", "<id>", "(", ")", "{", "<statement>", "}", ";"),
                "<id>": ("#keyword",),
                "<statement>": ("return", "<exp>", ";"),
                "<exp>": ("#int",)}


class ASTNode:
    """ An Abstract Syntax Tree class to parse lexed code."""
    children = []
    symbol_name = ""
    fields = []

    def __init__(self, symbol_name_: str, children_: list,  fields_: list = []):
        self.children = children_
        if (len(symbol_name_)) == 0:
            raise RuntimeError(
                "compiler->parser->ASTNode->__init__: symbol_name_ is empty")
        self.symbol_name = symbol_name_
        self.fields = fields_

    def AddChild(self, child):
        # check if child is in ASTNodes
        self.children.append(child)

    def _PrettyPrintHelper(self, child_spacing: str) -> str:
        out = f"{child_spacing}({self.symbol_name}: {[x.symbol_name for x in self.children]},{self.fields})\n"
        for e, child in enumerate(self.children):
            out += child._PrettyPrintHelper(child_spacing+'\t')
        return out

    def PrettyPrint(self):
        """ Pretty Print AST """
        print('-'*20, '\n', f"Printing {self.symbol_name}", '\n' + '-'*20+'\n')
        print(self._PrettyPrintHelper('│'))
        print()


def Program(function_declaration: ASTNode) -> ASTNode:
    if function_declaration.symbol_name != "function":
        raise RuntimeError(
            "compiler->parser->Program: function declaration is wrong")


def parse_program(tokens: re.Match) -> ASTNode:
    a = ASTNode()
    for x in GRAMMAR_DICT["<program>"]:
        a.AddChild(rule_to_func[x](tokens))
    print()


def parse_function(tokens: re.Match) -> ASTNode:
    print()


def parse_statement(tokens: re.Match) -> ASTNode:
    print()


def parse_exp(tokens: re.Match) -> ASTNode:
    print()


rule_to_func = {"<program>": parse_program,
                "<function>": parse_function,
                "<statement>": parse_statement,
                "<exp>": parse_exp}
