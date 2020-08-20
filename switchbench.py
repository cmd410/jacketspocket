"""Benchmark for swictchcase

requires: ggplot
"""

from io import StringIO
from contextlib import suppress, redirect_stdout
from timeit import timeit
from typing import Tuple
from ggplot import *
import pandas as pd

from switchcase import *




if __name__ == '__main__':
    hello_there = 'Hello there'
    bye = 'Bye'
    fox = 'Fox'
    hello = 'Hello'
    gbye = 'GoodBye'
    foxie = 'Foxie'
    i23 = 23
    i = 125
    f = 125.0
    l = []
    b = False
    tuple222 = ((((),()),((),())),(((),()),((),())))
    tuple22 = (((),()),((),()))
    unhandeled = 'Surprise!!!'

    test_cases = [
        hello_there, bye,
        fox, hello,
        gbye, foxie,
        i23, i, f, l, b,
        tuple222, tuple22,
        unhandeled
    ]

    test_var = tuple222

    #Number of iterations per test
    n = 100000

    def switch_test():
        with suppress(ValueError):
            with Switch(test_var) as case:
                @case('Hello there')
                def hello_case():
                    print('Hi! How are you?')
                
                @case('Bye')
                def bye_case():
                    print('GoodBye')
                
                @case('Fox')
                def fox_case():
                    print('fire')
                
                @case('Hello')
                def hello2_case():
                    print('Hi! How are you?')
                
                @case('GoodBye')
                def bye2_case():
                    print('GoodBye')
                
                @case('Foxie')
                def fox2_case():
                    print('fire')

                @case(23)
                def case_23():
                    print('its 23')

                @case(int)
                def integer_case():
                    print('its an integer!')
                
                @case(float)
                def float_case():
                    print('it floats!')
                
                @case(list)
                def list_case():
                    print('list here')
                
                @case(bool)
                def bool_case():
                    print('Its a bool!')
                
                @case(Shape(Tuple, 2, 2, 2))
                def shaped2_tuple_case():
                    print('its a 2x2x2 tuple!')

                @case(Shape(Tuple, 2, 2))
                def shaped_tuple_case():
                    print('its a 2x2 tuple!')

                @case(Default)
                def default_case():
                    raise ValueError('Unexpected value passed')
    
    def elif_test():
        with suppress(ValueError):
            if test_var == 'Hello there':
                print('Hi! How are you?')
            elif test_var == 'Bye':
                print('GoodBye')
            elif test_var == 'Fox':
                print('fire')
            elif test_var == 'Hello':
                print('Hi! How are you?')
            elif test_var == 'GoodBye':
                print('GoodBye')
            elif test_var == 'Foxie':
                print('fire')
            elif test_var == 23:
                print('its 23')
            elif isinstance(test_var, int):
                print('its an integer!')
            elif isinstance(test_var, list):
                print('list here')
            elif isinstance(test_var, float):
                print('it floats!')
            elif isinstance(test_var, bool):
                print('Its a bool!')
            elif isinstance(test_var, Tuple):
                if len(test_var) == 2:
                    if len(test_var[0]) == len(test_var[1]) == 2:
                        if len(test_var[0][0]) == len(test_var[0][1]) == len(test_var[1][0]) == len(test_var[1][1]) == 2:
                            print('its a 2x2x2 tuple!')
                        else:
                            print('its a 2x2 tuple!')
                    else:
                        raise ValueError('Unexpected value passed')
                else:
                    raise ValueError('Unexpected value passed')
            else:
                raise ValueError('Unexpected value passed')
    
    def run_speed_test(print_data=True):
        
        with redirect_stdout(StringIO()):
            swtich_time = timeit(switch_test, number=n)
            elif_time = timeit(switch_test, number=n)

        if print_data:
            print(f'Input Data: {repr(test_var)}')
            print(f'Switch:\n\t{swtich_time/n} sec/call avg')
            print(f'\tTotal time: {swtich_time}, Call count: {n}\n')
            print(f'Elif:\n\t{elif_time/n} sec/call avg')
            print(f'\tTotal time: {elif_time}, Call count: {n}\n')

            print(f'Switch is {swtich_time/n - elif_time/n} sec/call slower')
        
        return swtich_time, elif_time

    s_times = []
    e_times = []
    for i, test in enumerate(test_cases):
        test_var = test
        st, et = run_speed_test(False)
        s_times.append(st/n)
        e_times.append(et/n)
        print(f'Test#{i}:\n\tInput Data: {repr(test_var)}\n\t{st - et} delta seconds')

    sdata = pd.DataFrame({
        'Data': 'Switch',
        'Data_color': 'steelblue',
        'Time per call': s_times,
        'Test N': [i for i in range(len(s_times))]
    })

    edata = pd.DataFrame({
        'Data': 'Elif',
        'Data_color': 'red',
        'Time per call': e_times,
        'Test N': [i for i in range(len(e_times))]
    })

    diff_data = pd.DataFrame({
        'Data': 'Switch Overhead',
        'Data_color': 'grey',
        'Time per call': [s - e for e, s in zip(e_times, s_times)],
        'Test N': [i for i in range(len(e_times))]
    })

    data = pd.concat([sdata, edata, diff_data])

    p = ggplot(aes('Test N', 'Time per call', 'Data'), data=data)
    p += geom_line()
    p += geom_point(size=6)
    p.show()
