#!/usr/bin/env python
'''
Converts GitHub-flavored markdown to reStructuredText.
Requires pandoc to be installed.
'''
import re
import optparse
import os.path
import subprocess


CODE_SNIPPET_RE = re.compile(r'''
\`\`\`\w+				# Language name
(?P<code>[^\`]+)		# Code
\`\`\`					# Ending marker
''', re.IGNORECASE | re.VERBOSE)

def fix_code_snippets(md_text):
	''' Strips the GitHub-flavored code snippets
	and leaves standard Markdown indented ones. '''
	def _indent_snippet(match):
		code = match.groupdict()['code']
		code_lines = code.splitlines()
		indented_code_lines = (' ' * 4 + line for line in code_lines)
		return str.join("\n", indented_code_lines)
	return CODE_SNIPPET_RE.sub(_indent_snippet, md_text)


def main():
	cli_parser = optparse.OptionParser()
	cli_parser.add_option("-o", dest = "output",
						  help = "Write output to FILE", metavar = "FILE")
	
	(options, args) = cli_parser.parse_args()
	in_file = args[0]
	out_file = options.output or (os.path.splitext(in_file)[0] + ".rst")
	
	input = open(in_file).read() 
	fixed_input = fix_code_snippets(input)
	
	pandoc_cmd = ['pandoc', '-o', out_file]
	pandoc_process = subprocess.Popen(pandoc_cmd, stdin = subprocess.PIPE)
	pandoc_process.communicate(fixed_input)
	
	result = pandoc_process.wait()
	print "Conversion %s." % ("successful" if result == 0 else ("failed (error=%i)" % result))
	

if __name__ == '__main__':
	main()
