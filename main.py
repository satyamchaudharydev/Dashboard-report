import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
from datetime import date
from query.fetchSchools import fetchSchool_query
from query.fetchCourses import fetchCourses_query
from fetchData import fetchData
from query.fetchFeedbacks import fetchFeedback_query
from query.fetchTeachers import fetchTeachers_query
from python_graphql_client import GraphqlClient
from filteredFeedbackData import getFilteredFeedbackData
from datetime import datetime
from utils.rounded import getRoundedNum 
# local style.css in assest
external_stylesheets = ['assets/style.css']
# init app
app = Dash(__name__,
                external_stylesheets=external_stylesheets,
        )
server = app.server

schools = [
    'Dps@1public School',
    'Dps@2public School',
    'Dps@3public School',
    'Dps@4public School',
    'Dps@5public School',
]

courses = [
    'Web dev',
    'Python',
    'Canva',
    'Ms Access',
]
teacher = [
    'Teacher 1',
    'Teacher 2',
    'Teacher 3',
    'Teacher 4',
    'Teacher 5',
    'Teacher 6',
]
dummy_Data  = {
        'completed': 80,
        'notSubmitted': 20,
    }

schoolData = fetchData(fetchSchool_query())
coursesData = fetchData(fetchCourses_query())
getFeedbacksData = fetchData(fetchFeedback_query())
# fetchTeacherData = fetchData(fetchTeachers_query())

schoolData = schoolData['data']['schools']
coursesData = coursesData['data']['coursePackages']
feedbacksData = getFilteredFeedbackData(getFeedbacksData['data']['sessionFeedbacks'])
# csv
feedbacksData = pd.DataFrame(feedbacksData)

# filter feedbacks Data

school_options = [{'label': i['name'], 'value': i['name']} for i in schoolData]
course_options = [{'label': i['title'], 'value': i['title']} for i in coursesData]

teacher_options = [{'label': i, 'value': i} for i in teacher[:6]]

submission_status = {
    'completed': '80%',
    'notSubmitted': '20%',
}

fig = px.pie(
        names=dummy_Data.keys(),
        values=dummy_Data.values(),
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=.3,
        width=400,
        height=300,
    )

# load data
df = pd.read_csv('intro_bees.csv')

# create app layout
app.layout = html.Div([
    html.H1('Csat Data ', style={'text-align': 'center'}),  
    html.Br(),
    html.Div(className='filter_container', children=[
        dcc.Dropdown(id="slct-schools",
                placeholder="Select School",
                options=school_options,
                multi=False,
        ),
        dcc.Dropdown(id="slct-course",
                    options=course_options,
                    placeholder="Select Course",
                    multi=False,
        ),
        dcc.Dropdown(id="slct-teachers",
                    placeholder="Select Teacher",
                    options=teacher_options,
                    multi=False,
        ),
        dcc.Dropdown(id="slct-grades",
                    placeholder="Select Grade",
                    # options=teacher_options,
                    multi=False,
        ),
        dcc.DatePickerRange(
            id='data-picker',
            month_format='MMM Do, YY',
            end_date_placeholder_text='MMM Do, YY',
            start_date=date(2017, 6, 21)
        ),
    ]),
    html.Hr(),
    html.Br(),
    html.Div(className='overview_container', children=[
    html.Div(
        className='overview_card mini_card', children=[
            html.H3('Average Rating'),
            html.Div(
                id='overview_card_submission', children=[
                    html.H1('0'),
                ]
            )

        ]
     ),
    html.Div(
        className='overview_card', children=[
            html.H3('Submission Overview'),
            html.P('Total Submission: 0',
                    id='total_submission'
            ),
            html.Div(
                id='avg_rating'
            )
           
        ]
     ), 
   
    html.Div(
        className='overview_card mini_card time-overview', children=[
            html.H3( 'Average TimeTaken'),
            # h1 having class big-text and text is time
            html.H1('20s', className='big-text',id="avg_time_taken")
        ]
     ), 
    ]
    ),
    html.Hr(className='seperator'),
    html.Br(),
    html.Div(id='output_container',children=[
        html.H2('Data Table'),
        html.Div(id='output_table', children=[
            dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in feedbacksData.columns],
                data=feedbacksData.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'scroll'},
                style_cell={
                    'overflow': 'hidden',
                    'font-family': 'Arial',
                    'font-size': '15px',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
            )
        ])

    ]),
    # dcc.Graph(id='my_bee_app', figure={})   
])


# setting data of dropdown id="slct-teachers" dropdown on the basis of slct-schools
@app.callback(
    Output('overview_card_submission', 'children'),
    Output('avg_time_taken', 'children'),
    Output('avg_rating', 'children'),
    Output('output_table','children'),
    Output('slct-teachers','options'),
    Output('slct-grades','options'),
    Output('total_submission','children'),
    Input('slct-schools', 'value'),
    Input('slct-course','value'),
    Input('slct-teachers','value'),
    Input('slct-grades','value'),
    Input('data-picker' , 'start_date'),
    Input('data-picker' , 'end_date'),
)
def set_teacher_options(selected_school,selected_course,slct_teachers,slct_grades,start_date,end_date):
    filtered_school_id = [i['id'] for i in schoolData if i['name'] == selected_school][0]

    teacher_options = fetchData(fetchTeachers_query(filtered_school_id))
    classesList = []
    class_options = []
    for i in teacher_options['data']['school']['classes']:
        if(len(i)):
            classesList.append(i['grade'])
    
    if(len(classesList)): 
        classesList = list(set(classesList))
        classesList.sort(key=lambda x: int(x[5:]))
        class_options= [{'label': i, 'value': i} for i in classesList]
  
    if(len(teacher_options['data']['school']['teachers']) > 0):
        teacher_options = [{'label': i['user']['name'], 'value': i['user']['name']} for i in teacher_options['data']['school']['teachers']]
    else:
        teacher_options = [{'label': 'No Teachers', 'value': 'No Teachers'}]    

    filtered_feedbacksData = []
    ratings = []
    time_takens = []
    for i in getFeedbacksData['data']['sessionFeedbacks']:
        # if schoolId and grandeName is true then filter on the basis of schoolId and grandeName
        if(i['batch']['school']['id'] == filtered_school_id and ( 
            (slct_grades and i['batch']['grade']['name'] == slct_grades) or (not slct_grades)  
        )):
            filtered_feedbacksData.append(i)
    submission_status = {
        'completed': 0,
        'partially': 0
    }
    
    for i in filtered_feedbacksData:
        if(i['rating'] > 0):
            submission_status['completed'] += 1
        else:
            submission_status['partially'] += 1
    # averageTimeTaken  = getAverageTimeTaken(filtered_feedbacksData)
    if(len(filtered_feedbacksData)):

        for i in getFilteredFeedbackData(filtered_feedbacksData):
            if(i['rating'] != 'Not Given'):
                ratings.append(i['rating'])
            time_takens.append(i['timeTaken'])


    averageTimeTaken = sum(time_takens)/len(time_takens) if len(time_takens) else 0
    
    averageTimeTaken = str(averageTimeTaken) + '(s)'
    filtered_feedbacksData = pd.DataFrame(getFilteredFeedbackData(filtered_feedbacksData))
    if(len(filtered_feedbacksData)): 
        output_table = html.Div(id='output_table', children=[
            dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in filtered_feedbacksData.columns],
                data=filtered_feedbacksData.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'scroll'},
                style_cell={
                    'overflow': 'hidden',
                    'font-family': 'Arial',
                    'font-size': '15px',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                },
            )
        ])
    else :
        output_table = html.Div(id='output_table', children=[
            # no data is available
            html.H1('No Data Available')

        ])  

    fig = px.pie(
        names=submission_status.keys(),
        values=submission_status.values(),
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=.3,
        width=400,
        height=300,
    )      
    # filter if type is str 
    avg_rating = getRoundedNum(sum(ratings)/len(ratings)) if len(ratings) else 0

    rating_fig = px.bar(
        x=[i for i in range(1,6)],
        y= [ratings.count(i) for i in range(1,6)],
        color_discrete_sequence=px.colors.sequential.RdBu,
        width=400,
        height=300,
        labels={'x':'Rating', 'y':'Count'},
        orientation='v'
    )
    rating_fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
            dtick = 1
        )
    )


    total_submission = 'Total Submission is:' + str(len(filtered_feedbacksData))
    submission_fig = dcc.Graph(figure=rating_fig) if(len(filtered_feedbacksData)) else html.H1('No Data Available')

    return html.P(avg_rating,className='big-text'), averageTimeTaken,submission_fig, output_table,teacher_options,class_options,total_submission


            
   
def filteredTableData(schoolId,courseId,teacherId):
    return fetchData(fetchFeedback_query(
        schoolId,
    ), {'schoolId': schoolId})

def getAverageTimeTaken(data):
    total = 0
    if(len(data) > 0):
        for i in data:
            total += i['timeTaken']
        return total/len(data)


# run
if __name__ == '__main__':
    app.run_server(debug=True)
