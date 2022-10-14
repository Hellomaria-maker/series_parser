from func import series_pars
from func import genre_stat

"""
    Before starting, add the agent_user and cookie to the config file (conf.yaml)
"""

# Data loading --> genre_data.csv
genre_data = series_pars()

# Data analysis --> genre_plot.png
genre_stat(genre_data)

