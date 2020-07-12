#%%
from typing import List, Tuple
import glob
import xml.dom.minidom as dom
import os
import invoke
from invoke import task

chapters = [
    ("article/0.pre", 0),
    ("article/1.file", 1),
    ("article/2.search", 2),
    ("article/3.git", 3),
    ("article/4.auto", 4),
    ("article/5.environments", 5),
    ("article/6.view", 6),
    ("article/7.keyboard-shortcut", 7),
    ("article/8.other", 8),
    ("article/9.favorite", 9),
    ("article/99.end", 0),
    ("article/99.author", 0),
]

#%%
@task(default=True)
def build(c):

    with open(f"contents.html") as f:
        d: dom.Document = dom.parse(f)
    ul: dom.Node = d.getElementsByTagName("ul")[0]
    for n in list(ul.childNodes):
        ul.removeChild(n)

    for chap in chapters:
        build_html(c, chap)
        title, sub_tiles = convert_html(invoke.Context, chap)
        li = d.createElement("li")
        ul.appendChild(li)
        a = d.createElement("a")
        li.appendChild(a)
        a.setAttribute("href", f"{chap[0]}.xml.html")
        a.setAttribute("class", "tocxref")
        t = d.createTextNode(title)
        a.appendChild(t)
        if sub_tiles:
            ul2 = d.createElement("ul")
            li.appendChild(ul2)
            for sub_title in sub_tiles:
                li2 = d.createElement("li")
                ul2.appendChild(li2)
                t2 = d.createTextNode(sub_title)
                li2.appendChild(t2)

    with open(f"contents.html", "w") as f:
        d.writexml(f)
    c.run("./node_modules/.bin/prettier --write contents.html")


#%%
def build_html(c, chap):
    markdown_pdf = "node_modules/.bin/markdown-pdf"
    c.run(f"{markdown_pdf} html settings.yaml {chap[0]}.md")


def convert_html(c, chap) -> Tuple[str, List[str]]:
    with open(f"{chap[0]}.html") as f:
        html_text = f.read()
    cwd = os.getcwd()
    html_text = html_text.replace(f"file://{cwd}", "..")
    d = dom.parseString(html_text)

    title = ""
    sub_tiles = []
    # if chap[1] > 0:
    if True:
        # タイトルを挿げ替え
        for tag in d.getElementsByTagName("h1"):
            title_text = tag.firstChild.data
            if chap[1] > 0:
                title = f"{chap[1]}. {title_text}"
            else:
                title = f"{title_text}"
            tag.firstChild.data = title
        d.getElementsByTagName("title")[0].firstChild.data = title

        for i, tag in enumerate(d.getElementsByTagName("h2")):
            if chap[1] > 0:
                sub_title = f"{chap[1]}.{i+1} {tag.firstChild.data}"
            else:
                sub_title = f"{tag.firstChild.data}"
            tag.firstChild.data = sub_title
            sub_tiles.append(sub_title)
    else:
        d.getElementsByTagName("title")[0].firstChild.data = ""

    with open(f"{chap[0]}.xml.html", "w") as f:
        d.writexml(f)
    return title, sub_tiles


@task
def open_vivliostyle(c):
    ver = "2019.8.101"
    url = "https://github.com/vivliostyle/vivliostyle/releases/download/2019.8.101/vivliostyle-js-2019.8.101.zip"
    if not os.path.exists("vivliostyle-viewer"):
        c.run(f"curl -OL {url}")
        c.run(f"unzip vivliostyle-js-{ver}.zip")
        c.run(f"mv vivliostyle-js-{ver}/viewer vivliostyle-viewer")
        c.run(f"rm -rf vivliostyle-js-{ver} vivliostyle-js-{ver}.zip")
    page = "http://127.0.0.1:8000/vivliostyle-viewer/vivliostyle-viewer.html#b=http://127.0.0.1:8000/contents.html&renderAllPages=true&userStyle=data:,/*%3Cviewer%3E*/%0A@page%20%7B%20size:%20A5;%20%7D%0A/*%3C/viewer%3E*/"
    print(page)
    # c.run(
    #     'open /Applications/Google\\ Chrome.app "http://127.0.0.1:8000/vivliostyle-viewer/vivliostyle-viewer.html#b=http://127.0.0.1:8000/contents.html&renderAllPages=true&userStyle=data:,/*%3Cviewer%3E*/%0A@page%20%7B%20size:%20A5;%20%7D%0A/*%3C/viewer%3E*/"',
    #     warn=True,
    #     hide=True,
    # )

    c.run("npx http-server -p 8000 -c-1")

if __name__ == "__main__":
    build(invoke.Context())
