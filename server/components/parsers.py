from services.pandas_parser import PandasParser

def get_parser(parser_name):
    """ Get a parser for preparing and transforming a report """
    parser_name = parser_name

    if parser_name == 'Pandas':
        return PandasParser()
    
    else:
        raise ValueError("A parser, " + parser_name + ", wasn't set up to run in this system.")
            