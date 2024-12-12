def print_hello_world():
    print('Hello, World!')

import cProfile
cProfile.run('print_hello_world','resultado.prof')