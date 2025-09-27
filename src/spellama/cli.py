import click
import nltk
from spellama.splitting import makeChunks
import Lib.difflib as difflib

@click.group()
@click.version_option()
def cli():
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError: 
        click.echo("Need to download nltk dataset...")
        nltk.download('punkt_tab')


@cli.command()
@click.version_option()
@click.argument('file', type=click.File())
@click.option("--blocks-before", "numBlocksBefore", type=click.INT,  default=1, help="The number of front-padding blocks given to the corrector")
@click.option("--blocks-after", "numBlocksAfter", type=click.INT,  default=1, help="The number of back-padding blocks given to the corrector")
@click.option("--diff", "-d", is_flag=True, help="If set, presents a diff with the original file, rather than the raw correction")
def correct(file, numBlocksBefore, numBlocksAfter, diff) : 
    contents = file.read()
    sentences = nltk.tokenize.sent_tokenize(contents)

    chunks = makeChunks(sentences, numBlocksBefore, numBlocksAfter)

    betterChunks = [c.correct() for c in chunks]

    res = [c.getScrutinee() for c in betterChunks]

    if (diff):
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
    else:
        click.echo(" ".join(res))