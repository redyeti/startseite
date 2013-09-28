from lxml import etree
import re

# --- create extension function namespace ---

xfn = etree.FunctionNamespace("https://github.com/redyeti/startseite/xml/xfn-function-space")
xfn.prefix = "xfn"

def extension(fn):
	"""Add a function to the extension namespace"""
	xfn[fn.__name__] = fn
	return fn

# --- create extension functions ---

@extension
def search(context, pattern, string, group):
	"""
	Search for pattern in string and return group with number group.
	"""
	res = re.search(pattern, string)
	if res:
		return res.groups()[int(group)]
	else:
		return None

@extension
def null(context):
	"""Return None resp. null"""
	return None

re_ws = re.compile(r"[\s\n\r]+")

@extension
def br2x(context, nodelist, x="\n", sep="\n"):
	"""
	Return the text contained in nodelist (with whitespaced normalized) and
	replace all br with x. Separate elements with sep.
	"""
	out = ""
	for node in nodelist:
		for element in node.xpath(".//node()"):
			if isinstance(element, basestring):
				out += re_ws.sub(" ", element)
			elif element.tag == "br":
				out += x
	return out
