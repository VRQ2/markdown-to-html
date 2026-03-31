from tkinter.filedialog import askopenfilename
import os

def markdown_process_line(line):

	if line.startswith("######"):
		return f"<h6>{line[6:]}</h6>"

	if line.startswith("#####"):
		return f"<h5>{line[5:]}</h5>"

	if line.startswith("####"):
		return f"<h4>{line[4:]}</h4>"

	if line.startswith("###"):
		return f"<h3>{line[3:]}</h3>"

	if line.startswith("##"):
		return f"<h2>{line[2:]}</h2>"

	if line.startswith("#"):
		return f"<h1>{line[1:]}</h1>"

	if line.startswith("---"):
		return f"<hr>"

	if line == "" ctx['p']:
		p = f"<p>{ctx['p']}</p>"
		ctx['p'] = ""
		return p

	if ctx['p']:
		ctx['p']= ctx['p']+ '\n' + line
	else:
		ctx['p'] = line
	return ""

	p = []

	ST_P = "p"
	ST_UL = "+"

	state = ST_P

	for ch in line:

		if state == ST_P:
			pass
		if state == ST_UL:
			return f"<ul><li>{line[1:]}</li></ul>"
	return ""


def markdown_to_html(md):
	ctx = {
	"p":"",
	} #context
	html = []
	for line in md.splitlines():
		html.append(markdown_process_line(line))
	return ''.join(html)

#TODO: add alternative convert file when none selected

markdown_alt = """

# Alternative heading

## Alternative sub-heading

Paragraphs are separated
by a blank line.

Text attributes _italic_, **bold**, 'monospace'.

Horizontal rule:

---

"""

file_to_convert = askopenfilename(filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt")])


if file_to_convert:
	with open(file_to_convert, "r", encoding="utf-8") as f:
		markdown = f.read()

	html = markdown_to_html(markdown)

	with open("md.html", "w", encoding="utf-8") as f:
		f.write(html)
