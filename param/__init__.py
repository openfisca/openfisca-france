from src.gui.config import CONF

def get_config(widget):
    '''
    Sets some country specific parameters of the widgets
    '''
    country = CONF.get('simulation', 'country')
    if country == 'france':
        if isinstance(widget, AggregateOutputWidget):
            widget.varlist = ['irpp', 'ppe', 'af', 'cf', 'ars', 'aeeh', 'asf', 'aspa', 'aah', 'caah', 'rsa', 'aefa', 'api', 'logt']
            widget.selected_vars = set(['revdisp', 'nivvie'])