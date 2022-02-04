import pandas as pd
import streamlit as st
from datetime import datetime
import urllib.parse as up
import psycopg2

#Título de la página
st.title('chancle dineros 💸💸')

monto_original = 9834.50

# Arranca la parte ejecutable
def run():

    url = up.urlparse(st.secrets["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,  
    host=url.hostname,
    port=url.port
    )

    #cur = conn.cursor()

    #cur.execute("TRUNCATE gastos RESTART IDENTITY;")
    #conn.commit()

    df = pd.read_sql_query('SELECT * from "gastos"',con=conn, index_col='id')

    #cur.close()
    conn.close()

    container  = st.container()
    total = container.empty()
    total.metric(label="Dinero total restante", value='$' + str(9834.50 - df.amount.sum()), delta= '-$' + str(df.amount.sum()))

    koren = df.loc[df.spender == 'Koren']
    manu = df.loc[df.spender == 'Manu']
    jimo = df.loc[df.spender == 'Jimo']
    
    col1, col2, col3 = container.columns(3)
    dcol1 = col1.empty()
    dcol2 = col2.empty()
    dcol3 = col3.empty()
    dcol1.metric("Koren", "$"+str(round(monto_original/3 - koren.amount.sum(),2)), "-$" + str(round(koren.amount.sum(),2)))
    dcol2.metric("Manu",  "$"+str(round(monto_original/3 - manu.amount.sum(),2)), "-$" + str(round(manu.amount.sum(),2)))
    dcol3.metric("Jimo",  "$"+str(round(monto_original/3 - jimo.amount.sum(),2)), "-$" + str(round(jimo.amount.sum(),2)))

    #cur.execute("CREATE TABLE gastos (id serial PRIMARY KEY, amount integer, name varchar, spender varchar, date date, time time);")
    
    with st.form(key='Nuevo gasto'):
        pwd = st.text_input('contraseña')
        name = st.text_input('Nombre del gasto')
        amount = st.number_input('Monto')
        spender = st.selectbox('¿Quien fue el/la picaro/picara?',('Koren', 'Manu', 'Jimo'))
        date = st.date_input("Día?", datetime.now())
        time = st.time_input('¿Hora?', datetime.now())
        submit_button_type = st.form_submit_button(label='Enviar')
        
        if submit_button_type and pwd.lower()=='patos':
            up.uses_netloc.append("postgres")
            url = up.urlparse(st.secrets["DATABASE_URL"])
            conn = psycopg2.connect(database=url.path[1:],
            user=url.username,
            password=url.password,  
            host=url.hostname,
            port=url.port
            )

            cur = conn.cursor()

            cur.execute("INSERT INTO gastos (amount, name, spender, date, time) VALUES (%s, %s, %s, %s, %s)", (amount, name, spender, date, time))
            conn.commit()
            df = pd.read_sql_query('SELECT * from "gastos"',con=conn, index_col='id')
            cur.close()
            conn.close()
            
            total.metric(label="Dinero total restante", value='$' + str(9834.50 - df.amount.sum()), delta= '-$' + str(df.amount.sum()))
            
            koren = df.loc[df.spender == 'Koren']
            manu = df.loc[df.spender == 'Manu']
            jimo = df.loc[df.spender == 'Jimo']
            
            dcol1.metric("Koren", "$"+str(round(monto_original/3 - koren.amount.sum(),2)), "-$" + str(round(koren.amount.sum(),2)))
            dcol2.metric("Manu",  "$"+str(round(monto_original/3 - manu.amount.sum(),2)), "-$" + str(round(manu.amount.sum(),2)))
            dcol3.metric("Jimo",  "$"+str(round(monto_original/3 - jimo.amount.sum(),2)), "-$" + str(round(jimo.amount.sum(),2)))

            st.balloons()
            
    up.uses_netloc.append("postgres")
    url = up.urlparse(st.secrets["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,  
    host=url.hostname,
    port=url.port
    )

    df = pd.read_sql_query('SELECT * from "gastos"',con=conn)

    st.write(df)
if __name__ == '__main__':
    run()