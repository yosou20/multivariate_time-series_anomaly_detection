#from uts_ad import residual_outlier_detection
#from uts_ad import plot_anomaly_data22
from uts_ad import*
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
import random as randn
import seaborn as sns
from matplotlib.dates import DateFormatter

# utils for deeplearning

import cufflinks as cf
import plotly.graph_objs as go
import plotly.offline as py
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected= True)
cf.go_offline()