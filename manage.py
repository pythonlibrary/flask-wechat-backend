import os
import click

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@click.group()
def cli():
    pass

@click.command()
def run():
    app.run(debug=True, host="0.0.0.0", port=80)

cli.add_command(run)

if __name__ == '__main__':
    cli()

