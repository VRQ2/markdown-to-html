from tkinter.filedialog import askopenfilename
import os

def _process_single_line(line):
  output = ""

  ST_TEXT = "text"
  ST_AST = "*"
  ST_UND = "_"
  ST_MONO = "`"

  s_i = False
  s_b = False
  s_m = False
  s_u = False

  state = ST_TEXT

  i = -1
  while True:
    i += 1
    if i > len(line):
      break

    if i == len(line):
      ch = None
    else:
      ch = line[i]

    if state == ST_TEXT:
      if ch == "_":
        state = ST_UND
        continue

      if ch == "*":
        state = ST_AST
        continue

      if ch == "`":
        state = ST_MONO
        continue

      if ch is not None:
        output += ch
      continue

    if state == ST_MONO:
      s_m = not s_m
      if s_m:
        output += "<code>"
      else:
        output += "</code>"
      state = ST_TEXT
      i -= 1
      continue

    if state == ST_AST:
      if ch == "*":
        s_b = not s_b
        if s_b:
          output += "<b>"
        else:
          output += "</b>"
        state = ST_TEXT
        continue

      s_i = not s_i
      if s_i:
        output += "<i>"
      else:
        output += "</i>"
      state = ST_TEXT
      i -= 1
      continue

    if state == ST_UND:
      if ch == "_":
        s_u = not s_u
        if s_u:
          output += "<u>"
        else:
          output += "</u>"
        state = ST_TEXT
        continue

      s_i = not s_i
      if s_i:
        output += "<i>"
      else:
        output += "</i>"
      state = ST_TEXT
      i -= 1
      continue

  return output

def _markdown_process_line(line, ctx):
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

  if line == "---":
    return "<hr>"

  if line == "" and ctx['p']:
    p = f"<p>{ctx['p']}</p>"
    ctx['p'] = ""
    return p

  line = _process_single_line(line)

  if ctx['p']:
    ctx['p'] = ctx['p'] + '\n' + line
  else:
    ctx['p'] = line

  return ""


def markdown_to_html(md):
  ctx = {
    "p": ""
  }
  html = []
  for line in md.splitlines():
    html.append(_markdown_process_line(line, ctx))

  html.append(_markdown_process_line("", ctx))

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
