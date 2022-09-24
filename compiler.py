from ast import AST
import sys
import re
from inspect import currentframe, getframeinfo

from ASTfunctions import ASTNode, GRAMMAR_DICT, LITERALS


def println(frameinfo) -> None:
    line = frameinfo.lineno
    print("Line No: ", line)


def lex(source: str) -> list[re.Match]:
    print("lexing...")
    # token_re = r"(?P<curly_open>{)|(?P<curly_closed>})|(?P<paren_open>\()|(?P<paren_closed>\))|(?P<semicolon>;)|(?P<decimal_numeric>[0-9]+)|(?P<keyword>int|return)|(?P<identifier>[a-zA-z]\w*)"
    token_re = r"(?P<curly_open>{)|(?P<curly_closed>})|(?P<paren_open>\()|(?P<paren_closed>\))|(?P<semicolon>;)|(?P<decimal_numeric>[0-9]+)|(?P<int>int)|(?P<return>return)|(?P<identifier>[a-zA-z]\w*)"
    tokens = re.finditer(token_re, source)
    """ if (len(tokens) == 0): raise RuntimeError(f"compiler->lexer: no tokens found in your program shown below\n{'*'*15+source}")
	print(type(tokens))
	print(f"tokens: {tokens}")
	for x in tokens:
		print(x.groups())
		print(x.group()) """
    print("lexing complete...")
    return list(tokens)


def IsRegex(comparator: str, reg: str) -> bool:
    return re.match(comparator, reg) is not None


def IsRule(group_name: str) -> bool:
    """ IsRule: checks if the string is formatted as a rule or not """
    # TODO: check if regex is right online
    comparator = r"<[a-zA-Z]+>"
    # print("checking",group_name, ': ', re.match(comparator, group_name))
    return re.match(comparator, group_name) is not None


def IsIdentifier(id: str) -> bool:
    """IsIdentifier: Returns if the string is an identifier (eg. a variable name) in the C++ compiler"""
    re_id = r"[a-zA-z]\w+"
    return IsRegex(id, re_id)


def IsInt(id: str) -> bool:
    """Checks if a string is in the proper format for an int"""
    re_id = r"[0-9]+"
    return IsRegex(id, re_id)


def UpdateToken(token: re.Match, tokens: list[re.Match], i: int) -> tuple([int, re.match]):
    if (i == len(tokens)-1):
        # raise SyntaxError( "compiler->parse->UpdateToken->Syntax Error: ran out of tokens")
        return (-1, token)
    i, token = i+1, tokens[i+1]
    print("token updated: ", token.group())
    return (i, token)


def parse(tokens: list[re.Match], symbol: str, i: int) -> tuple([ASTNode, re.match]):
    """ Recursively go through all tokens in the program and add them to an AST tree defined by a single ASTNode """
    print('-'*35, '\n', "parsing...\n", end='')
    n = ASTNode(symbol, [])
    token = tokens[i]

    print(symbol, token.group(), i)

    for rule in GRAMMAR_DICT[symbol]:
        print(f"rule 1: {rule} ~ {token.group()}")
        if (rule == "<id>" and IsIdentifier(token.group())):
            i, token = UpdateToken(token, tokens, i)
            return n
        elif (rule == "<int>" and IsInt(token.group())):  # TODO: unused so remove or fix
            i, token = UpdateToken(token, tokens, i)
            continue
        elif (not IsRule(rule)):
            # The rule should be a literal or a keyword or a variable name
            print("is not rule")
            # TODO: Check for Literals and return value or return value

            if rule in LITERALS:
                n = ASTNode(symbol, [], [token.group()])
                println(getframeinfo(currentframe()))
                i, token = UpdateToken(token, tokens, i)
                continue
            elif (token.group() != rule):
                raise SyntaxError(
                    f"compiler->parse->Unexpected Keyword: \"{token.group()}\" given when expected keyword \"{rule}\"")
            else:
                println(getframeinfo(currentframe()))
                i, token = UpdateToken(token, tokens, i)
        else:
            print(f"now parsing {token.group()}")
            n_ast, token_n = parse(tokens, rule, i)
            n.AddChild(n_ast)
            print(symbol, len(GRAMMAR_DICT[rule]))
            println(getframeinfo(currentframe()))
            print(token.group(), token_n.group())
            while token != token_n:
                i, token = UpdateToken(token, tokens, i)

    return n, token

    # grammar: tokens to symbols
    # AST: symbols to processing calculations


if __name__ == "__main__":
    print("Compiler Starting...")
    if (len(sys.argv) != 2):
        raise RuntimeError(
            f"compiler->main: invalid amount of arguments ({len(sys.argv)}) for program")
    else:
        source_file = sys.argv[1]
        assembly_file = source_file.split('.')[0] + ".s"

        assembly_format = """
.globl _main
_main:
movl	${}, &eax
ret
	"""

    with open(source_file, 'r') as infile, open(assembly_file, 'w') as outfile:
        source = infile.read().strip()
        tokens = lex(source)
        print([a.group() for a in tokens])
        ast = parse(tokens, "<program>", 0)[0]
        ast.PrettyPrint()
        outfile.write(assembly_format)
