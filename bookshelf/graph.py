import pygal
import json
from urllib2 import urlopen  # python 2 syntax
# from urllib.request import urlopen # python 3 syntax
 
 
from flask import Flask
from pygal.style import DarkSolarizedStyle
 
app = Flask(__name__)
 
#----------------------------------------------------------------------
@app.route('/')
def get_weather_data():
   
    
    # create a bar chart
    title = 'entities'
    # bar_chart = pygal.Bar(width=1200, height=600,
    #                       explicit_size=True, title=title, style=DarkSolarizedStyle)
    bar_chart = pygal.StackedLine(width=1200, height=600,
                         explicit_size=True, title=title, fill=True)
 
    bar_chart.x_labels = ['apple','oranges','grapes']
    imp_temps=[20,59,1]
    bar_chart.add('Temps in F', imp_temps)
 
    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """ % (title, bar_chart.render())
    return html
 
 
#----------------------------------------------------------------------
if __name__ == '__main__':    
    app.run()