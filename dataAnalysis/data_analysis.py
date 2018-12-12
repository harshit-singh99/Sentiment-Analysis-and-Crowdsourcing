import pandas as pd
import random
import numpy
from nltk.corpus import stopwords
import matplotlib as mpl
#mpl.use('Cairo')
mpl.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dirc = os.path.join(BASE_DIR,'static') 
sns.set(rc={'figure.figsize':(13,4.27)})
plt.rcParams["xtick.labelsize"] = 7
stops = set(stopwords.words("english"))    
stops = stops.union(set(['film','movie','restaurant']))

def get_len_min_max_mean(lst):
    total = len(lst)
    avgl = lst.mean()
    return total , avgl

def get_most_frequent(n,lst):
    wordcount = list(pd.Series(' '.join(lst).split()).value_counts()[:n].keys())
    return wordcount

def get_stats_for_df(dataF):
    reviews, avg = get_len_min_max_mean(dataF['text length'])#send to django
    wc = get_most_frequent(50,dataF['text'])#send to django
    df_stats = {'count':reviews,'avg_text_len':avg,'freq_words' : wc}
    return dict(df_stats)

def cleantext(string):
    text = string.lower()
    text = text.replace(" v ", " very ")
    text = text.replace(" r ",' are ')
    text = text.split()
    text = [w for w in text if not w in stops and len(w)>=2]
    text = " ".join(text)
    return text    

def plot_pie(complete,rtype,pietype,name):
    plt.figure() 
    labels = complete[rtype].value_counts().keys()
    sizes = complete[rtype].value_counts().values
    colors = [ 'red','blue','lime','orange','yellow','brown','grey','green','chocolate','violet','aqua']
    patches, texts, autotexts = plt.pie(sizes, colors = colors,  shadow=True, startangle=90,autopct='%1.1f%%',)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(dirc + '/'+ rtype +'_graphs/'+name+'_all_'+pietype+'_pie.png')
    plt.close()

def plot_graphs(rtype,complete,reviw_type_df,name):
    plt.figure()
    pc = sns.countplot(x='polarity', data=reviw_type_df)
    pc.get_figure().savefig( dirc + '/'+rtype + "_graphs/"+name+"_polarity_counts.png")
    plt.close()
    plt.figure()
    gender_c = sns.countplot(x='polarity',hue = 'gender', data=reviw_type_df)
    gender_c.get_figure().savefig(dirc + '/'+rtype + "_graphs/"+name+"_polarity_counts_gender.png")
    plt.close()
    plt.figure()
    pct = sns.boxplot(x='polarity', y='text length', data=reviw_type_df)
    pct.get_figure().savefig(dirc + '/'+rtype +"_graphs/"+name+"_polarity_textlen.png")
    plt.close()
    plt.figure()
    cmr = sns.countplot(x=rtype, data=complete)
    cmr.get_figure().savefig(dirc + '/'+rtype + "_graphs/"+name+"_all_reviews.png")
    plt.close()
    plt.figure()
    temp = sns.countplot(x=rtype, hue = 'polarity', data=complete, )
    temp.get_figure().savefig(dirc + '/'+rtype +"_graphs/"+name+"_all_polarity.png")
    plt.figure()
    cct = sns.boxplot(x=rtype, y='text length',hue = 'polarity', data=complete)
    cct.get_figure().savefig(dirc + '/'+rtype +"_graphs/"+name+"_all_text.png")
    plt.close()
    plot_pie(complete,rtype,'reviews',name)
    posdf = complete[complete['polarity'] == 'p']
    plot_pie(posdf,rtype,'positive',name)

def get_stats(complete, analysis_for_rtype,rtype):
    if 'location' in list(complete.columns):
        analysis_for_location = complete[complete[rtype] == analysis_for_rtype]['location'].unique()[0]
        complete = complete[complete['location'] == analysis_for_location]
    complete['text length'] = complete['text'].apply(len)
    complete
    mvdf = complete[complete[rtype] == analysis_for_rtype].copy()
    mvdf['text'] = mvdf['text'].map(lambda x : cleantext(x))
    mvpdf = mvdf[mvdf['polarity'] == 'p']
    mvndf = mvdf[mvdf['polarity'] == 'n']
    total_stats = get_stats_for_df(mvdf)
    pos_stats = get_stats_for_df(mvpdf)
    neg_stats = get_stats_for_df(mvndf)
    plot_graphs(rtype,complete,mvdf,analysis_for_rtype)
    return total_stats,pos_stats,neg_stats
