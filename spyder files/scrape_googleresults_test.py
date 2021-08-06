# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle
import os

url = r'https://www.google.co.uk/search?q=Tyrone+Mings'

ra = requests.get(url)
soupa = BeautifulSoup(ra.content, "lxml")