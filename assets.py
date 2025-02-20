from flask_assets import Environment, Bundle

def set_bundles(app):
    bundles = {
        'css_liste': Bundle('css/commun.css', 'css/liste.css'),

        'css_details': Bundle('css/details.css', 'css/commun.css'),

        'base_css': Bundle(
            'scss/style.scss',
            filters='pyscss',
            output = 'gen/base.css'
        )
    }

    assets = Environment(app)
    assets.register(bundles)