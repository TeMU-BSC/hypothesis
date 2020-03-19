import click
from hypothesis.annotations import annotations


@click.command()
@click.option('--annotations', default=False)
@click.option('--users', default=False)
@click.option('--groups', default=False)
def main(annotations,users,groups):
    if annotations:
        pass
    elif users:
        pass
    elif groups:
        pass
    else:
        print("You must select a option: --annotations, --users, --groups\n[--help] to see help menu.")





if __name__ == '__main__':
    main()