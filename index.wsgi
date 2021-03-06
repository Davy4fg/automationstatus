# coding: UTF-8
import os

import sae
import web

from weixinInterface import *

urls = (
'/weixin','WeixinInterface',
'/hi.*','HiInterface',
'/dev1','Dev1Interface',
'/main','MainInterface',
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

#app = web.application(urls, globals()).wsgifunc()        
#application = sae.create_wsgi_app(app)
app = web.application(urls, globals()).wsgifunc() 
app.debug = True    
application = sae.create_wsgi_app(app)   
#app.run()
