from . import app, db
from .models import Page
from flask import render_template, url_for, request
import re


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route('/<page>', methods=['POST', 'GET'])
def one_slash(page):
    return render_template('index.html')\

@app.route('/<page>/<page2>', methods=['POST', 'GET'])
def two_slash(page, page2):
    return render_template('index.html')

@app.route('/<page>/<page2>/<page3>', methods=['POST', 'GET'])
def three_slash(page, page2, page3):
    return render_template('index.html')\

@app.route('/<page>/<page2>/<page3>/<page4>', methods=['POST', 'GET'])
def four_slash(page, page2, page3, page4):
    return render_template('index.html')\

@app.route('/_request/', methods=['POST', 'GET'])
def request_page():

    url = '.'.join(request.args.get('url').split('/')[3:]) or 'home'
    page = Page.query.filter_by(url=url).first()
    if page is not None:
        if request.args.get('tex') == 'True':
            return page.tex
        else:
            return page.body
    else:
        return '0'

@app.route('/_post/', methods=['POST', 'GET'])
def post_page():
    url = '.'.join(request.form.get('url').split('/')[3:]) or 'home'
    print('\n\n\n\n\n',url)
    tex = request.form.get('tex')
    body = parse_tex(tex)

    p = Page.query.filter_by(url=url).first()
    if not p:
        p = Page(url=url, tex=tex, body=body)
        db.session.add(p)
    else:
        p.tex = tex
        p.body = body

    db.session.commit()

    return p.body


def parse_tex(tex):
    tex = '<p>' + tex + '</p>'
    links = re.finditer('(\[[\s\S]+\]\([\s\S]+\))', tex)

    tex = re.sub('(\n\n)','</p><p>',tex)

    for link in links:
        span = link.span()
        text = re.search('(?<=\[)([\s\S]+)(?=\])', link.group(0)).group(0)
        href = re.search('(?<=\()([\s\S]+)(?=\))', link.group(0)).group(0)
        tex = tex[:span[0]] + '<a href="%s">%s</a>' % (href, text) + tex[span[1]:]

    while True:
        h = re.search('(?<==)[^=]+?(?==)', tex)
        if not h:
            break

        span = h.span()
        tmp = re.match('(<h[0-9]>[\s\S]+?</h[0-9]>)', tex[span[0]:span[1]])
        if tmp:
            i = int(tmp.group(0)[2])
            tex = tex[:(span[0]-1)] + '<h%i>%s</h%i>' % (i+1, h.group(0)[4:-5], i+1) + tex[(span[1]+1):]
        else:
            tex = tex[:(span[0]-1)] + '<h1>%s</h1>' % h.group(0) + tex[(span[1]+1):]

    return tex