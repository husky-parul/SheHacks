# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]


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
                book = get_model().create(data)
        else:
            data={}
            data['entity']='UNK'
            data['sentiment']=sentiment.score
            book = get_model().create(data)
       
        
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