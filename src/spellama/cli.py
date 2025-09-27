import click
from nltk.tokenize import sent_tokenize
from spellama.splitting import makeChunks
import Lib.difflib as difflib

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo('Hello World!')


@cli.command()
@click.argument('filename')
def correct(filename): 
    with open(filename, "r") as f:
        contents = f.read()
    sentences = sent_tokenize(contents)

    chunks = makeChunks(sentences)

    betterChunks = [c.correct() for c in chunks]

    res = [c.getScrutinee() for c in betterChunks]

    diff = difflib.unified_diff(sentences, res, fromfile='original', tofile='corrected') 
    COLOR_HEADER = '\x1b[34m'
    COLOR_ADD    = '\x1b[32m' 
    COLOR_REMOVE = '\x1b[31m'
    COLOR_RESET  = '\x1b[37m'

    for line in diff:
        if line.startswith('---') or line.startswith('+++') or line.startswith('@@'):
            click.echo(f"{COLOR_HEADER}{line}{COLOR_RESET}")
        elif line.startswith('+'):
            click.echo(f"{COLOR_ADD}{line}{COLOR_RESET}")
        elif line.startswith('-'):
            click.echo(f"{COLOR_REMOVE}{line}{COLOR_RESET}")
        else:
            click.echo(line)