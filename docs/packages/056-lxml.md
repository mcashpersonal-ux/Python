# 54 — Fast HTML/XML with lxml

> `lxml` is a C-speed HTML/XML library — either used directly with
> XPath/CSS selectors, or as the fast parser backend under
> `beautifulsoup4`. Reach for it directly when performance on large
> documents matters.

---

## install

```bash
pip install lxml
```

---

## parse HTML and select with XPath

```python
from lxml import html

tree = html.fromstring(open("page.html", encoding="utf-8").read())

titles = tree.xpath("//h2[@class='title']/text()")
print(titles)
```

XPath (`//h2[@class='title']/text()`) is more powerful than CSS selectors
for complex conditions (position, sibling relationships, text content
matching) at the cost of a steeper learning curve.

---

## select with CSS instead

```python
from lxml.cssselect import CSSSelector

sel = CSSSelector("div.product .price")
prices = [el.text_content().strip() for el in sel(tree)]
```

---

## parse XML and use namespaces

```python
from lxml import etree

tree = etree.parse("data.xml")
ns = {"ns": "http://example.com/schema"}
values = tree.xpath("//ns:reading/@value", namespaces=ns)
```

XML namespaces must be declared in the `namespaces=` dict with a prefix
you choose — it doesn't have to match the document's own prefix.

---

## build XML

```python
from lxml import etree

root = etree.Element("readings")
child = etree.SubElement(root, "reading", sensor="line1")
child.text = "23.4"

xml_bytes = etree.tostring(root, pretty_print=True)
print(xml_bytes.decode())
```

---

## error handling basics

```python
from lxml import etree

try:
    tree = etree.parse("data.xml")
except etree.XMLSyntaxError as e:
    print("malformed XML:", e)
```

For HTML, `lxml.html` is lenient by design (it recovers from broken
markup) — errors are rarer there than with strict XML parsing.

---

## snippets box

```python
# parse HTML straight from a requests response
from lxml import html
import requests

resp = requests.get("https://example.com")
tree = html.fromstring(resp.content)
```

```python
# use as beautifulsoup4's backend for a friendlier API
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.text, "lxml")
```

---

## when to use what

| Need | Package |
|---|---|
| Max speed, XPath, large documents | `lxml` |
| Friendlier API for messy HTML | `beautifulsoup4` (with lxml as backend) |
| Simple well-formed XML, no extra dependency | stdlib `xml.etree.ElementTree` |

Next door: extract structured data with XPath, then validate it with
`pydantic` before use.
