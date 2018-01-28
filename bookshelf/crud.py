# 2018 SheHacks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

from bookshelf import get_model
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Blueprint, redirect, render_template, request, url_for, Markup
import datetime
import pygal
import json
from urllib2 import urlopen  # python 2 syntax
#from urllib.request import urlopen # python 3 syntax
 
 
from flask import Flask
from pygal.style import DarkSolarizedStyle


crud = Blueprint('crud', __name__)
categories={'physical appearance':['head','hair','eye','beautiful','beauty','weight','height','clothes','health','gym','mirror','weight gain','age','wellbeing','age','voice'],
'social anxiety':['people','anxiety attacks','group','fear','conversation','anyone','self-confidence','embarrassment','anxiety','person','individuals'],
'professional life':['career','money','wage','work schedule','work','apprenticeship','job','opportunity','salary','manager'],
'relationship':['friends','boyfriend','partner','husband','family','son','daughter','sister','brother','mother','father','relationship','friends','friendship'],
'life':['life','holidays','beginning','place','house']}

SENTIMENTS={}

# [START list]
@crud.route("/")
def list():
    
    token = request.args.get('page_token', None)
  
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list()
    cumm_sentiment={}
  
    for book in books:
        if book.get('entity'):
            entity_val=book['entity']
            sentiment_val=[]
            if cumm_sentiment.get(entity_val):
                sentiment_val=cumm_sentiment.get(entity_val)
                sentiment_val.append(book.get('sentiment'))
                cumm_sentiment[entity_val]=sentiment_val
            else:
                cumm_sentiment.update({entity_val:[book.get('sentiment')]})
       
            
   
    new_book=[]
    visited=[]
    SENTIMENTS=cumm_sentiment
    for book in books:
        new_date="-".join(book['date'].split(":", 2)[:2])

        if new_date not in visited:
            visited.append(new_date)
            new_book.append(book)

   
  
    print '1: _______________: ',cumm_sentiment
    print '2: **************: ', SENTIMENTS
    NEW_BOOK=new_book
    return render_template(
        "list.html",
        books=new_book,
        next_page_token=next_page_token)
# [END list]




@crud.route("/home", methods=['POST','GET'])
def home():
    title = 'entities'
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list()
    cumm_sentiment={}
  
    for book in books:
        if book.get('entity'):
            entity_val=book['entity']
            sentiment_val=[]
            if cumm_sentiment.get(entity_val):
                sentiment_val=cumm_sentiment.get(entity_val)
                sentiment_val.append(book.get('sentiment'))
                cumm_sentiment[entity_val]=sentiment_val
            else:
                cumm_sentiment.update({entity_val:[book.get('sentiment')]})

    line = pygal.Line()
    line.title = 'Sentiments data' #set chart title
    line.x_labels = map(str, range(0, 6)) #set the x-axis labels.
    print 'am i alive************', cumm_sentiment
    for cat,val in cumm_sentiment.iteritems():
        print 'cat: ******',cat, "\n val: ",val
        line.add(cat, val) #set values.
    print line
    line.render_in_browser()
    return 'string'


@crud.route("/cummulative", methods=['POST','GET'])
def cummulative():
    title = 'entities'
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list()
    cumm_sentiment={}
    min_date="-".join(books[0]['date'].split(":", 2)[:2])
    max_date=""
    for book in books:
        if book.get('entity'):
            entity_val=book['entity']
            sentiment_val=[]
            if cumm_sentiment.get(entity_val):
                sentiment_val=cumm_sentiment.get(entity_val)
                sentiment_val.append(book.get('sentiment'))
                cumm_sentiment[entity_val]=sentiment_val
            else:
                cumm_sentiment.update({entity_val:[book.get('sentiment')]})
 
            if min_date > "-".join(book['date'].split(":", 2)[:2]):
                min_date="-".join(book['date'].split(":", 2)[:2])
            if max_date < "-".join(book['date'].split(":", 2)[:2]):
                max_date="-".join(book['date'].split(":", 2)[:2])

    new_cat_dict={}
    #looping through sentiments
    for sentiment, senti_val in cumm_sentiment.iteritems():
        #looping throg categories
        for cat, cat_val in categories.iteritems():
            
            if sentiment in cat_val:
                if new_cat_dict.get(cat):
                    new_cat_dict_val=new_cat_dict.get(cat)
                    new_cat_dict_val=new_cat_dict_val+senti_val
                    new_cat_dict[cat]=new_cat_dict_val
                else:
                    new_cat_dict.update({cat:senti_val})

    print '/new_cat_dict !!!!!!!!!!!!!!!: ',new_cat_dict
    print 'min_date: ',min_date, 'max_date: ', max_date


    line = pygal.Line()
    line.title = 'Sentiments data' #set chart title
    min_date=min_date.split(' ')[1]
    min_date=min_date.split('-')[0]
    max_date=max_date.split(' ')[1]
    max_date=max_date.split('-')[0]
  
    line.x_labels = map(str, range(1, 19)) #set the x-axis labels.
    for cat,val in new_cat_dict.iteritems():
       
        line.add(cat, val) #set values.

    print line
    line.render_in_browser()
    return 'string',cumm_sentiment

@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        data_txt = request.form.to_dict(flat=True)
        
        # Create a Cloud Natural Language client.
        client = language.LanguageServiceClient()

        # Retrieve inputs and create document object
        text = data_txt['description']
        title = data_txt['title']
        document = language.types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

        # Retrieve response from Natural Language's analyze_entities() method
        response = client.analyze_entities(document=document)
        entities = response.entities

        # Retrieve response from Natural Language's analyze_sentiment() method
        response = client.analyze_sentiment(document=document)
        sentiment = response.document_sentiment


        if entities:
            for i in entities:
                data={}
                data['entity']=i.name
                data['sentiment']=sentiment.score
                data['description']=text
                data['title']=title
                print '%%%%%%%%%%%%%%%%%%%%%: ',str(datetime.datetime.now())
                ddd=str(datetime.datetime.now())
                date_str=unicode(ddd, "utf-8")
                data['date']=date_str
                book = get_model().create(data)
                print 'book: ',book
        else:
            data={}
            data['entity_val']='UNK'
            data['sentiment']=sentiment.score
            book = get_model().create(data)
            print 'book: ',book
       
        
        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
