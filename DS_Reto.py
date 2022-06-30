#Incluir librerías para desarrollo de programa/app/página web
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from altair.vegalite.v4.schema.channels import Tooltip
import altair as alt
import warnings #Se incluye warnings ya que estuvo enviando un error relativo a la ejecución del script en el shell de streamlit
warnings.filterwarnings('ignore') #Se ignoran los warnings relativos a los filtros

#Leer en un DataFrame de pandas la información del archivo csv
df = pd.read_csv('employee_data.csv')

#Filtrar el DataFrame en uno nuevo para solo tener la información necesaria del reto
employee_data = df[['name_employee', 'birth_date', 'age', 'gender', 'marital_status', 'hiring_date', 'position', 'salary', 'performance_score', 'last_performance_date', 'average_work_hours', 'satisfaction_level', 'absences']]

#Se crean tres columnas para poder centrar el logotipo de la empresa (en este caso, logo del ITESM)
col1, col2, col3 = st.columns([10,10,10])
with col1:
    st.write('')
with col2:
    st.image('itesm_logo.png', caption = 'Logo de Empresa', width = 150) # <-- Código de streamlit para incluir la imagen. Se redimensiona para no ocupar mucho espacio de pantalla
with col3:
    st.write('')

st.header ('Desempeño Colaboradores - Socialize Your Knowledge') # <-- Código de streamlit para incluir el encabezado de la app
st.markdown ('**Bienvenido** al dashboard de información de ***Socialize Your Knowledge*** :flag-mx: :wink:') # <-- Se utiliza la función markdown de streamlit para dar un poco de formato al texto e incluir emojis

#Generar una selección de botones en streamlit para elegir el género y mostrarlo en la barra lateral
st.sidebar.markdown ('1) Selecciona el género del empleado   :arrow_heading_down:')
gender_sel = st.sidebar.radio (label = 'M - Masculino | F - Femenino', options = employee_data['gender'].unique(), horizontal = True)
#Se hace una pequeña función IF para mostrar un mensaje dependiendo del género seleccionado
if gender_sel == 'M ':
    st.sidebar.markdown ('Has seleccionado el género **masculino** :man-raising-hand:')
else:
    st.sidebar.markdown ('Has seleccionado el género **femenino** :woman-raising-hand:')

st.sidebar.write('---------------------')
#Generar un slider para determinar el rango basado en la columna performance_score
st.sidebar.markdown ('2) Selecciona el rango de desempeño :arrow_down:')
perf_range = st.sidebar.slider('Mover los puntos de referencia', min_value = float(employee_data['performance_score'].min()), max_value = float(employee_data['performance_score'].max()), value = (0.0, float(employee_data['performance_score'].max())))
st.sidebar.write ('Has seleccionado el rango entre ', perf_range[0], 'y ', perf_range[1])
st.sidebar.write('---------------------')

#Generar uan caja de selección para el estado civil de los empleados
st.sidebar.markdown ('3) Selecciona el estado civil :arrow_down:')
marital_sel = st.sidebar.selectbox (label = 'Estado civil', options = employee_data['marital_status'].unique())
if marital_sel == 'Single':
    st.sidebar.markdown ('Has seleccionado **soltera/o**')
elif marital_sel == 'Married':
    st.sidebar.markdown ('Has seleccionado **casada/o**')
elif marital_sel == 'Divorced':
    st.sidebar.markdown ('Has seleccionado **divorciada/o**')
elif marital_sel == 'Separated':
    st.sidebar.markdown ('Has seleccionado **separada/o**')
else:
    st.sidebar.markdown ('Has seleccionado **viuda/o**')

#Generar gráfica para mostrar distribución de puntajes
st.subheader ('Histograma de Número de Empleados por Calificación de Desempeño')
fig_box = px.histogram(employee_data[employee_data['gender'] == gender_sel], x = 'performance_score', title = 'Por género')
fig_box.update_layout (xaxis_title = 'Desempeño', yaxis_title = 'Número de Empleados')
fig_box2 = px.histogram (employee_data[employee_data['marital_status'] == marital_sel], x = 'performance_score',
title ='Por estado civil')
fig_box2.update_layout (xaxis_title = 'Desempeño', yaxis_title = 'Número de Empleados')
col4, col5 = st.columns([80,80])
col4.plotly_chart(fig_box, use_container_width=True)
col5.plotly_chart(fig_box2, use_container_width=True)

#Generar gráfica de barras para mostrar el promedio de horas por estado civil
st.subheader('Gráfico de Barras del Promedio de Horas Trabajadas por Estado Civil')
bar_hrs = alt.Chart(employee_data).mark_bar().encode(alt.X ('marital_status', title = 'Estado Civil'), alt.Y ('mean(average_work_hours)', title = 'Promedio de Horas Trabajadas'), tooltip = [alt.Tooltip('mean(average_work_hours)')], color = alt.value('purple'))
st.altair_chart(bar_hrs, use_container_width=True)

#Generar gráfico edad de los empleados respecto al salario percibido
st.subheader('Gráfico para mostrar lel rango de salarios para cada grupo de edad')
age_salary = alt.Chart(employee_data).mark_boxplot(extent = 'min-max').encode(alt.X ('age', title = 'Edad', scale = alt.Scale(domain = (28,70))), alt.Y ('salary', title = 'Salario'), tooltip = [alt.Tooltip('age'), alt.Tooltip('salary')], color = alt.value('green'), opacity = alt.value(0.5))
st.altair_chart(age_salary, use_container_width=True)

#Generar gráfico de relación del promedio de horas trabajadas vs puntaje de desempeño
st.subheader('Relación entre promedio de horas trabajadas y puntaje de desempeño')
fig_scat = px.scatter(employee_data, x = 'performance_score', y = 'average_work_hours', color = 'gender', size = 'salary', symbol = 'gender', color_discrete_map={'M ': 'RebeccaPurple', 'F': 'MediumPurple'}, template = 'simple_white')
fig_scat.update_layout (xaxis_title = 'Desempeño', yaxis_title = 'Promedio de horas trabajadas')
st.plotly_chart(fig_scat, use_container_width=True)

#Código para escribir conclusiones
st.subheader('Conclusiones')
st.write('Con base en la información mostrada, se puede concluir lo siguiente:')
st.markdown ('1) Independientemente del género o el estado civil de los empleados, la mayor parte de la población se encuentra en un valor de desempeño de **3**')
st.markdown ('2) No hay ninguna diferencia significativa de horas trabajadas por cada grupo de **Estado Civil**')
st.markdown ('3) Los rangos de salarios presentan un rango importante ne todos los grupos de edades. Los empleados de 67 años **presentan los salarios más altos en todos los grupos de edades**')
st.markdown ('4) **No hay relación** entre las horas trabajadas y la evaluación de desempeño de los empleados')
