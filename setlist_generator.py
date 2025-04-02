import streamlit as st  # pip install streamlit=1.12.0
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode # pip install streamlit-aggrid==0.2.3
import itertools
import time as t
from datetime import timedelta
import plotly.figure_factory as ff
from datetime import date
import plotly.graph_objs as go

today = date.today()
formatted_date_2 = today.strftime("%B/%d/%Y") # Day/month/year


st.set_page_config(page_icon='📊', page_title='Setlist Generator')
st.title('Song Selection:')
# Getting total length
def get_sec(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

sum = 0

m, s = divmod(sum, 60)

onRowDragEnd = JsCode("""
function onRowDragEnd(e) {
    console.log('onRowDragEnd', e);
}
""")

getRowNodeId = JsCode("""
function getRowNodeId(data) {
    return data.id
}
""")

onGridReady = JsCode("""
function onGridReady() {
    immutableStore.forEach(
        function(data, index) {
            data.id = index;
            });
    gridOptions.api.setRowData(immutableStore);
    }
""")

onRowDragMove = JsCode("""
function onRowDragMove(event) {
    var movingNode = event.node;
    var overNode = event.overNode;

    var rowNeedsToMove = movingNode !== overNode;

    if (rowNeedsToMove) {
        var movingData = movingNode.data;
        var overData = overNode.data;

        immutableStore = newStore;

        var fromIndex = immutableStore.indexOf(movingData);
        var toIndex = immutableStore.indexOf(overData);

        var newStore = immutableStore.slice();
        moveInArray(newStore, fromIndex, toIndex);

        immutableStore = newStore;
        gridOptions.api.setRowData(newStore);

        gridOptions.api.clearFocusedCell();
    }

    function moveInArray(arr, fromIndex, toIndex) {
        var element = arr[fromIndex];
        arr.splice(fromIndex, 1);
        arr.splice(toIndex, 0, element);
    }
}
""")


data = pd.read_csv('cougar_songs.csv')[['Name','Length','Key']]

gb1 = GridOptionsBuilder.from_dataframe(data)
gb1.configure_column(field='Name', width=600, editable=True, filter=True)
gb1.configure_column(field='Length', flex=3, editable=True, filter=True)
gb1.configure_column(field='Key', flex=3, editable=True, filter=True)
gb1.configure_selection(selection_mode='multiple', use_checkbox=True)
gridOptions = gb1.build()

data = AgGrid(data,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=True
)

# st.dataframe(data['selected_rows'])

if data['selected_rows'] is not None:
    st.subheader("Setlist")

    selected = pd.DataFrame(data['selected_rows'].reset_index(drop=True))
    selected.index = selected.index + 1

    gb2 = GridOptionsBuilder.from_dataframe(selected)
    gb2.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = True, 
                            rowDragMultiRow=True)
    gb2.configure_column('Name', rowDrag = True, rowDragEntireRow = True, width=600)
    gb2.configure_column(field='Length', flex=3)
    gb2.configure_column(field='Key', flex=3)
    gb2.configure_grid_options(rowDragManaged = True, onRowDragEnd = onRowDragEnd,
                            deltaRowDataMode = True, getRowNodeId = getRowNodeId, 
                            onGridReady = onGridReady, animateRows = True, 
                            onRowDragMove = onRowDragMove)
    gridOptions2 = gb2.build()



    
    AgGrid(selected,
           gridOptions=gridOptions2,
           allow_unsafe_jscode=True,
           theme='balham',
           fit_columns_on_grid_load=True)
    
    for i in selected['Length']:
        sum = sum + get_sec(i)
    st.markdown('''
        **Total:** :red[{}] minutes'''.format(round(sum/60, 2)))
    
    check = st.checkbox('Include Venue in Filename/Title')
    if check:
        venue=st.text_input('Venue Name:')
        title = '{} {}'.format(venue, today)
    else:
        title = '{}'.format(today)
    
    def createImage(df):
        df[''] = ''
        df[' '] = ''
        fig = ff.create_table(df, index=False)
        fig.layout.width = 250
        fig.layout.update({'title': '{}'.format(title)})
        fig.update_layout({'margin': {'t': 50}})
        for i in range(len(fig.layout.annotations)):
            fig.layout.annotations[i].font.size = 15
            fig.layout.annotations[0].font.color = '#41466b'
        fig.update_xaxes(color = '#FCFCFC')
        fig.write_image("image.png", scale=2)
        
    
    createImage(selected['Name'].reset_index())

# Download button
    
else:
    pass
''
with open("image.png", "rb") as file:
        
        st.download_button(
            "Download Image",
            data=file,
            file_name="setlist {}.png".format(formatted_date_2),
            mime="setlist/png",
            icon=":material/download:",
            on_click='rerun'
        )
