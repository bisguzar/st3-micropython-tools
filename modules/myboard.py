import textwrap

BUFFER_SIZE = 32


class myBoard():
    def __init__(self, connection):
        self._connection = connection

    def list_dir(self, dir='/'):

        run = """
            try:
                import os
            except ImportError:
                import uos as os
            print(os.listdir('{0}'))
        """.format(dir)

        self._connection.enter_raw_repl()

        try:
            out = self._connection.exec(textwrap.dedent(run))
        except PyboardError as ex:
            # Check if this is an OSError #2, i.e. directory doesn't exist and
            # rethrow it as something more descriptive.
            if ex.args[2].decode('utf-8').find('OSError: [Errno 2] ENOENT') != -1:
                raise RuntimeError('No such directory: {0}'.format(directory))

        self._connection.exit_raw_repl()

        return out