import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import itertools
import time as t
from datetime import timedelta

st.set_page_config(page_icon='📊', page_title='Setlist Generator')

df = pd.read_csv('cougar_songs.csv', index_col=False)

covers = pd.read_csv('jammin.csv', index_col=False)
# covers = covers.iloc[:,2:7]
covers['Name'] = covers['Track Name']
covers['Count'] = 1

seconds, ms = divmod(covers['Duration (ms)'], 1000)
minutes, seconds = divmod(seconds, 60)
length = []

for i, j in zip(minutes, seconds):
    length.append('{}'.format(i) + ':' '{:02d}'.format(j))

covers['Length'] = length

st.dataframe(covers.groupby(['Key']).count()['Count'])

with st.container():

    checkbox = st.checkbox('Include cover songs *(decide **BEFORE** making the selections)*:')
    if checkbox:
        df = pd.concat([df, covers], join='inner')
    
    options = st.multiselect(
        'Choose Song(s) Here',
        df['Name'].to_list())
    table = []
    
    if options != []:
        for i in options:
            table.append(pd.DataFrame(zip(df.loc[df['Name']=='{}'.format(i)]['Name'], df.loc[df['Name']=='{}'.format(i)]['Length']), columns=['Name', 'Length']))

        table = pd.concat(table, ignore_index=True)
        table.index = table.index + 1
    
        # Getting total length
        def get_sec(time_str):
            m, s = time_str.split(':')
            return int(m) * 60 + int(s)
        
        sum = 0
        for j in table['Length']:
            sum = sum + get_sec(j)
        st.table(table)

        m, s = divmod(sum, 60)

        st.markdown('''
            **Total:** :red[{}] minutes :red[{}] seconds'''.format(m, s))
        # st.dataframe(covers.groupby(['Artist Name(s)'].count()['Count'])
                 
        
    if options == []:
        st.markdown('''
         **Total:** :red[0] minutes''')
