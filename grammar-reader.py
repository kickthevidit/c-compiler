import re

def LexGrammar(src: str):
	rules_re = r"(?P<production_symbol><\S+>)\s*::=[^\S\r\n]+((([^\S\r\n]*(?P<rule_symbol><\S+>)|(?P<rule_keyword>\"\S\"))[^\S\r\n]*)+)"
	rules = re.finditer(rules_re, src)
	return rules


def ReadGrammar(grammar_path: str) -> dict[str : list[str]]:
	with open(grammar_path, 'r') as infile:
		str = infile.read().strip()
		rules_iter = LexGrammar(str)
		rules_dict = { for r in rules_iter}
		for r in rules_iter:

