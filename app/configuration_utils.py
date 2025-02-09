import os
import json





def configure_app(app):
    # Load environment-specific configuration class
    config_object = f"app.settings.{os.environ.get('FLASK_ENVIRONMENT', 'Development')}Config"
    app.config.from_object(config_object)
    app.secret_key = app.config['SECRET_KEY']


def load_secrets(app):
    #Load OIDC secrets from the client secrets file
    secrets_file = app.config.get('OIDC_CLIENT_SECRETS')
    if secrets_file:
        try:
            with open(secrets_file, 'r') as file:
                oidc_secrets = json.load(file)
                for key, value in oidc_secrets.get('web', {}).items():
                    app.config.setdefault(f"OIDC_{key.upper()}", value)
        except FileNotFoundError:
            app.logger.error(f"OIDC secrets file not found: {secrets_file}")
        except json.JSONDecodeError as e:
            app.logger.error(f"Error decoding JSON in {secrets_file}: {e}")            