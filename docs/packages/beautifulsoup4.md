# 53 — HTML parsing with Beautiful Soup

> `beautifulsoup4` (imported as `bs4`) parses messy real-world HTML into a
> navigable tree — find tags, extract tables, follow links — without
> needing well-formed XML. Pairs with `requests`/`httpx` for scraping.

---

## install

```bash
pip install beautifulsoup4
```

Install a parser backend too — `lxml` is fastest:

```bash
pip install lxml
```

---

## parse HTML and find elements

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com")
soup = BeautifulSoup(resp.text, "lxml")

title = soup.find("h1")
print(title.text.strip())
```

---

## find multiple elements and extract attributes

```python
links = soup.find_all("a", href=True)
for link in links[:5]:
    print(link["href"], link.text.strip())
```

CSS selectors work too, often more concisely:

```python
prices = soup.select("div.product .price")
for p in prices:
    print(p.text.strip())
```

---

## extract a table into rows

```python
table = soup.find("table", class_="data")
rows = []
for tr in table.find_all("tr")[1:]: # skip header row
    cells = [td.text.strip() for td in tr.find_all("td")]
    rows.append(cells)
print(rows)
```

---

## navigate the tree

```python
node = soup.find("span", class_="value")
print(node.parent.name) # containing tag
print(node.find_next_sibling()) # next element at the same level
```

---

## error handling basics

```python
node = soup.find("h1", class_="missing-class")
if node is None:
    print("element not found — page structure may have changed")
else:
    print(node.text)
```

`.find()` returns `None` rather than raising when nothing matches —
always check before calling `.text` on the result, or you'll hit an
`AttributeError` on `None`.

---

## snippets box

```python
# strip all HTML tags, keep just text
clean_text = soup.get_text(separator=" ", strip=True)
```

```python
# parse a local file instead of a live fetch
with open("page.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")
```

---

## when to use what

| Need | Package |
|---|---|
| Forgiving parser for messy real-world HTML | `beautifulsoup4` |
| Maximum parsing speed, strict XML too | `lxml` (bs4's backend, or standalone) |
| JavaScript-rendered pages | needs a browser automation tool, not covered here |

Next door: feed the extracted rows into `pandas` for cleanup and
analysis.
