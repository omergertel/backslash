import click

import logbook

from .bootstrapping import requires_env, from_project_root

_logger = logbook.Logger(__name__)

@click.command()
@click.argument('name')
@click.argument('args', nargs=-1)
@requires_env('app', 'develop')
def suite(name, args):
    import slash
    import gossip

    from slash.frontend.slash_run import slash_run
    from backslash.contrib.slash_plugin import BackslashPlugin

    plugin = BackslashPlugin('http://127.0.0.1:8000')

    @gossip.register('backslash.session_start')
    def configure(session):
        session.add_subject('system1', product='Microwave', version='1.0', revision='100')

    slash.plugins.manager.install(plugin, activate=True)

    slash_run([from_project_root('_sample_suites', name)] + list(args))
