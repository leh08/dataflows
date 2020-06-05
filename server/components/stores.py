from services.redshift import Redshift


class Store:
    def __init__(self, name):
        self.name = name
    
    def create_store(self):
       def get_store(self):
            target = self.target
            
            if target == 'Redshift':
                return Redshift()
            
            else:
                raise ValueError("A target, " + target + ", wasn't set up to run in this system.")
             

