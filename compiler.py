from secrets import token_bytes
import sys
import re

import ASTfunctions

def lex(source: str):
	# token_re = r"(?P<curly_open>{)|(?P<curly_closed>})|(?P<paren_open>\()|(?P<paren_closed>\))|(?P<semicolon>;)|(?P<decimal_numeric>[0-9]+)|(?P<keyword>int|return)|(?P<identifier>[a-zA-z]\w*)"
	token_re = r"(?P<curly_open>{)|(?P<curly_closed>})|(?P<paren_open>\()|(?P<paren_closed>\))|(?P<semicolon>;)|(?P<decimal_numeric>[0-9]+)|(?P<int>int)|(?P<return>return)|(?P<identifier>[a-zA-z]\w*)"
	token_object = re.compile(token_re)
	print(token_object.groupindex)
	tokens = re.finditer(token_re, source)
	# if (len(tokens) == 0): raise RuntimeError(f"compiler->lexer: no tokens found in your program shown below\n{'*'*15+source}")
	print(type(tokens))
	print(f"tokens: {tokens}")
	for x in tokens:
		print(x.groups())
	return tokens


def parse(tokens): # takes an iterable, returns an ast
	print()

if __name__=="__main__":
	print("Compiler Starting...")
	if (len(sys.argv) != 2):
		raise RuntimeError(f"compiler->main: invalid amount of arguments ({len(sys.argv)}) for program")
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
		outfile.write(assembly_format)
