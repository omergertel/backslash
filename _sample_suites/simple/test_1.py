import slash


def test_1():
    pass

def test_2():
    slash.logger.warning('This is a warning')

def test_3():
    slash.skip_test('skipped')

@slash.hooks.session_start.register
def emit_warning():
    slash.logger.warning('Session warning here')
