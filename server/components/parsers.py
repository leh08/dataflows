from services.pandas_parser import PandasParser


class Parser:
    def __init__(self, name):
        self.name = name
    
    def create_parser(self):
        """ Get a parser for preparing and transforming a report """
        parser_name = self.parser_name
        
        self.logger.info(parser_name)
        if parser_name == 'Pandas':
            return PandasParser()
        
        else:
            raise ValueError("A parser, " + parser_name + ", wasn't set up to run in this system.")
            