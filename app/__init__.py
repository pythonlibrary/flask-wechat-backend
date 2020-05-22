from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from .apiv1 import api_v1 
from config import config
from app.core.articles import update_articles



def create_app(config_name):
    scheduler = BackgroundScheduler()
    
    config[config_name].start_hook()

    app = Flask(__name__)
    app.register_blueprint(api_v1)

    app.config.from_object(config[config_name])  # Read config from config.py

    app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }

    # Ugly implementation for saving scheduler object and articles cache
    setattr(app, 'articles', None)
    setattr(app, 'ap_scheduler', scheduler)

    post_sitemap = app.config.get('SITEMAP_URL')

    # run task right away at the startup
    update_articles(post_sitemap, app)
    app.ap_scheduler.add_job(update_articles, 'interval', [post_sitemap, app], days=10)
    app.ap_scheduler.start()

    config[config_name].init_app(app)  # call init_app from config

    return app

