import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from IPython.display import HTML
from matplotlib import pyplot as plt
from celluloid import Camera
import plotly.graph_objects as go

import networkx as nx

from IPython.display import HTML
from matplotlib import pyplot as plt
from celluloid import Camera
import collections


import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
import ast
from random import shuffle



email_df = pd.read_csv('Data/emails_tokenized.csv')
employee_df = pd.read_csv('Data/employee_keywords.csv')
network_df = pd.read_csv('Data/network.csv')

jobs = pd.read_csv('Data/Enron_jobs.csv')
job_dict = {}
level_dict = {}
keywords_dict = {}



exec_list = ['CEO','President','Vice President']
network_df['rec_list'] = [ast.literal_eval(x) for x in network_df['rec_list']]
#employee_df['key_words'] = [ast.literal_eval(x) for x in employee_df['key_words']]



email_df = email_df[~email_df['token_subject'].isna()]

exec_list = ['CEO','President','Vice President']

job_count = collections.Counter()
for rank in email_df['sender_level']:
    job_count[rank] +=1


for email,level,job,keyword in zip(employee_df['email_id'],employee_df['job_rank'],employee_df['job_title'],employee_df['key_words']):
    job_dict[email] = job
    level_dict[email] = level
    keywords_dict[email] = keyword

main_emails = list(employee_df['email_id'])

email_df = email_df[[email in main_emails for email in email_df['sender']]]


sender_count_dict = {}
for sender in set(network_df['sender']):
    sender_count_dict[sender] = len(set(network_df[network_df['sender']==sender]['mid']))



email_to_id = {}
id_to_email ={}
count = 0
for user in main_emails:
    email_to_id[user] = count
    id_to_email[count] = user
    count+=1

central_id = email_to_id['jeff.skilling@enron.com']
central_id

user_matrix = np.zeros((len(main_emails),len(main_emails)))

for sender ,rec_list,rec_count in zip(network_df['sender'],network_df['rec_list'],network_df['rec_count']):
    for recer in rec_list:
        user_matrix[email_to_id[sender]][email_to_id[recer]] += (1/rec_count)*sender_count_dict[sender]



G = nx.Graph()

G.add_nodes_from(range(len(user_matrix)))

# create list of edge weights to cut by percentile
edge_values = list(user_matrix)
l =[]
for edges in edge_values:
    l = l + list(edges)
edge_values = l



edge_thresh = np.percentile(edge_values,97.5)
for i in range(len(user_matrix)):
    for j in range(len(user_matrix)):
        #if i ==jeff_sig_id:
                #print('jeff_potential')
        if user_matrix[i][j] > edge_thresh:
            if i ==central_id:
                print('jeff_connection')
            G.add_edge(i,j)

ranks = ['CEO','President','Vice President','Director']

level_num_dict = {}
for node in G.nodes():
    for i in range(len(ranks)):
        if ranks[i] == level_dict[id_to_email[node]]:
            level_num_dict[node] = i
            continue
    if node not in level_num_dict:
        level_num_dict[node] = len(ranks)


rank_list = []
for i in range(10):
    i_range_list = []
    for key,value in level_num_dict.items():
        if level_num_dict[key] ==i:
            i_range_list.append(key)
    rank_list.append(i_range_list)
while [] in rank_list:
    rank_list.remove([])


job_count = collections.Counter()
for rank in jobs['job_rank']:
    job_count[rank] +=1


plotly_color = ['red','orange','yellow','purple','green','black','black','black','black','black','black']
node_size = [900,600,400,300,200,100,100,100,100,100]

colors_plotly = []
sizes_node = []


for node_num in list(G.nodes()):
    colors_plotly.append(plotly_color[level_num_dict[node_num]])
    sizes_node.append(node_size[level_num_dict[node_num]])

pos = {}
for i in range(len(rank_list)):
    x = -1 + i/5
    for j in range(len(rank_list[i])):
        pos[rank_list[i][j]] = (x,1/len(rank_list[i])*j) 
heir_pos = pos


#tree pos
pos = {}
for i in range(len(rank_list)):
    x = -1 + i/5
    for j in range(len(rank_list[i])):
        pos[rank_list[i][j]] = (x,1/(len(rank_list[i]))*j) 

#pos = nx.shell_layout(G,nlist=rank_list)
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)


edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))



node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    
for node in G.node:
    text_string = ''
    text_string = text_string + id_to_email[node]
    text_string = text_string + '<br /> Level: '+  str(level_dict[id_to_email[node]]) + '<br /> Title: ' +str( job_dict[id_to_email[node]]) + '<br />' +keywords_dict[id_to_email[node]]
    node_text.append(text_string)
        

node_trace.marker.color = colors_plotly
node_trace.text = node_text



fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Enron Social Communication Network',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()




plt.show()

