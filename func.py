import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import yaml

import matplotlib.pyplot as plt
import seaborn as sns


def series_pars(save_to_csv: bool = True):
    """
       Feature to download series genre data from the Kinopoisk website.
       Args:
            save_to_csv (bool): if True save data to csv
    """

    config = yaml.load(open(r"conf.yaml"), Loader=yaml.Loader)
    series_list = []

    for page in range(1, 6):
        url_template = f"https://www.kinopoisk.ru/lists/movies/series-top250/?page={page}"
        r = requests.get(url_template, headers={'User-Agent': config['user_arent'],
                                                'cookie': config['cookie']})
        series_soup = bs(r.text, 'lxml')
        series_info = series_soup.findAll(class_='desktop-list-main-info_truncatedText__IMQRP')
        for series in series_info[::2]:
            series_str = series.string.strip().replace('\xa0', '%').replace('\u2022', '%')
            series_str = series_str.split('%')
            series_list.append(series_str[1])

    genre_data = pd.DataFrame(series_list, columns=['genre'])

    if save_to_csv:
        genre_data.to_csv('genre_data.csv')

    return genre_data


def genre_stat(genre_data, save_to_png: bool = True):
    """
       Feature to statistical analysis of genre data.
       Args:
           genre_data (DataFrame): data preloaded in series_pars function
           save_to_png (bool): if True save plot to png
    """

    plt.figure(figsize=(16, 10))

    ax1 = sns.countplot(x="genre", data=genre_data, palette='coolwarm')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=40, ha="right", fontsize=12)
    plt.title(
        "Статистика жанров",
        fontsize=15
    )

    if save_to_png:
        plt.savefig("genre_plot.png")
