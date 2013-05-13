from src.gui.config import CONF
from src.plugins.survey.aggregates import AggregatesWidget

def get_config(widget):
    """
    Sets some country specific parameters of the widgets
    TODO:seems to be unused
    """
    country = CONF.get('simulation', 'country')
    if country == 'france':
        if isinstance(widget, AggregatesWidget):
            widget.varlist = ['irpp', 'ppe', 'af', 'cf', 'ars', 'aeeh', 'asf', 'aspa', 'aah', 'caah', 'rsa', 'psa', 'aefa', 'api', 'logt']
            widget.selected_vars = set(['revdisp', 'nivvie'])