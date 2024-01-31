import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import itertools
import time as t
from datetime import datetime

df = pd.read_csv('cougar_songs.csv', index_col=False)
st.set_page_config(page_icon=':bar_chart:')

with st.container():

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

        st.markdown('''
            **Total:** :red[{}] minutes'''.format(round(sum/60, 2)))
    if options == []:
        st.markdown('''
         **Total:** :red[0] minutes''')
