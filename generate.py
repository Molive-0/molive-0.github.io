import shutil, os, tomllib, subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
)

OUTPUT_DIR = "output/"
BLOG_DIR = OUTPUT_DIR + "blog/"
COPY_DIRS = ["dump/", "static/"]

PORTFOLIO_PATH = "portfolio.toml"
ARTICLES_PATH = "articles.toml"
ARTICLES_DIR = "articles/"

shutil.rmtree(OUTPUT_DIR, True)
os.mkdir(OUTPUT_DIR)
for dir in COPY_DIRS:
    shutil.copytree(dir, OUTPUT_DIR + dir)
shutil.copy("CNAME", OUTPUT_DIR + "CNAME")

# Index.html
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
output = template.render(articles)

out_path = BLOG_DIR + "index.html"
with open(out_path, "w") as f:
    f.write(output)

# Articles

template = env.get_template('article.html')

for article in os.listdir(ARTICLES_DIR):
    title = os.path.splitext(article)[0]
    article_out = subprocess.run(["pandoc", ARTICLES_DIR + article, "-t" "HTML"], capture_output=True, text = True)
    output = template.render(title=title, content=article_out.stdout)
    out_path = BLOG_DIR + title + ".html"
    with open(out_path, "w") as f:
        f.write(output)
