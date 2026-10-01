import shutil, os, tomllib, subprocess, datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
)
from feedgen.feed import FeedGenerator

URL = "https://mo.molive.live/"
OUTPUT_DIR = "output/"
BLOG_DIR = OUTPUT_DIR + "blog/"
COPY_DIRS = ["dump/", "static/"]

PORTFOLIO_PATH = "portfolio.toml"
ARTICLES_PATH = "articles.toml"
ARTICLES_DIR = "articles/"

# Static

shutil.rmtree(OUTPUT_DIR, True)
os.mkdir(OUTPUT_DIR)
for dir in COPY_DIRS:
    shutil.copytree(dir, OUTPUT_DIR + dir)
shutil.copy("CNAME", OUTPUT_DIR + "CNAME")

# Index

with open(PORTFOLIO_PATH, "rb") as p:
    portfolio = tomllib.load(p)

template = env.get_template('index.html')
output = template.render(portfolio)

out_path = OUTPUT_DIR + "index.html"
with open(out_path, "w") as f:
    f.write(output)

# Articles listing

os.mkdir(BLOG_DIR)
with open(ARTICLES_PATH, "rb") as p:
    articles = tomllib.load(p)

template = env.get_template('blog.html')
articles["article"] = sorted(articles["article"], key=lambda article: article["date"], reverse=True)
for article in articles["article"]:
    article["date_formatted"] = article["date"].date()
    article["href"] = os.path.splitext(article["filename"])[0]
output = template.render(articles)

out_path = BLOG_DIR + "index.html"
with open(out_path, "w") as f:
    f.write(output)

# Articles

template = env.get_template('article.html')

fg = FeedGenerator()
fg.id(URL + "blog/")
fg.title("Molive's blog")
fg.author( {'name':'Molive','email':'molive@stargaze.group'} )
fg.icon(URL + "static/favicon.png")
fg.updated(datetime.datetime.now(datetime.timezone.utc))
fg.link( href=URL + "blog/test.atom", rel='self' )
fg.language('en')
fg.description("The blog of the demoscener Molive")

for article in articles["article"]:
    title = article["title"]
    filename = article["href"]
    article_out = subprocess.run(["pandoc", ARTICLES_DIR + article["filename"], "-t" "HTML"], capture_output=True, text = True)
    output = template.render(title=article["title"], content=article_out.stdout)
    out_path = BLOG_DIR + filename
    with open(out_path, "w") as f:
        f.write(output)
    fe = fg.add_entry()
    fe.id(URL + "blog/" + filename + "/")
    fe.updated(article["updated"])
    fe.author( {'name':'Molive','email':'molive@stargaze.group'} )
    fe.description(article["description"])
    fe.title(title)
    fe.published(article["date"])
    fe.content(article_out.stdout, URL + "blog/" + filename + "/")
    fe.link( href=URL + "blog/" + filename + "/", rel='self' )
    tags = []
    for tag in article["tags"]:
        tags.append({"term":tag})
    fe.category(tags)

fg.atom_file(BLOG_DIR + 'atom.xml')
fg.rss_file(BLOG_DIR + 'rss.xml')
