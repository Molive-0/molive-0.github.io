import shutil, os, tomllib, subprocess, datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
)
from feedgen.feed import FeedGenerator

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
articles["article"] = sorted(articles["article"], key=lambda article: article["date"], reverse=True)
for article in articles["article"]:
    article["date_formatted"] = article["date"].date()
output = template.render(articles)

out_path = BLOG_DIR + "index.html"
with open(out_path, "w") as f:
    f.write(output)

# Articles

template = env.get_template('article.html')

fg = FeedGenerator()
fg.id('https://mo.molive.live/blog')
fg.title("Molive's blog")
fg.author( {'name':'Molive','email':'molive@stargaze.group'} )
fg.logo("https://mo.molive.live/static/favicon.png")
fg.icon("https://mo.molive.live/static/favicon.png")
fg.updated(datetime.datetime.now(datetime.timezone.utc))
fg.link( href='https://mo.molive.live/blog/test.atom', rel='self' )
fg.language('en')
fg.description("The blog of the demoscener Molive")

for article in articles["article"]:
    title = article["title"]
    filename = os.path.splitext(article["filename"])[0]
    article_out = subprocess.run(["pandoc", ARTICLES_DIR + article["filename"], "-t" "HTML"], capture_output=True, text = True)
    output = template.render(title=article["title"], content=article_out.stdout)
    out_path = BLOG_DIR + filename + ".html"
    with open(out_path, "w") as f:
        f.write(output)
    fe = fg.add_entry()
    fe.id("https://mo.molive.live/blog/" + filename)
    fe.updated(article["updated"])
    fe.author( {'name':'Molive','email':'molive@stargaze.group'} )
    fe.description(article["description"])
    fe.title(title)
    fe.source("https://mo.molive.live/blog/" + filename + ".html")
    fe.published(article["date"])
    fe.content(article_out.stdout)

atomfeed = fg.atom_str(pretty=True) # Get the ATOM feed as string
rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
fg.atom_file(BLOG_DIR + 'atom.xml') # Write the ATOM feed to a file
fg.rss_file(BLOG_DIR + 'rss.xml') # Write the RSS feed to a file
