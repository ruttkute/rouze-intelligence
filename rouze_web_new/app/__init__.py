import os
from flask import Flask

def create_app():
    # Get absolute path to this file's directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to rouze_web_new/, then to templates and static
    base_dir = os.path.dirname(app_dir)
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static'),
        static_url_path='/static'
    )

    # Config
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    return app

# Create app instance
app = create_app()
