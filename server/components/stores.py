from services.redshift import Redshift

def get_store(name):
    if name == 'Redshift':
        return Redshift()
    
    else:
        raise ValueError("A target, " + name + ", wasn't set up to run in this system.")
             

