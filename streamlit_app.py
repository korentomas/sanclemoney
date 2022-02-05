import pandas as pd
import streamlit as st
from datetime import datetime
import urllib.parse as up
import psycopg2

monto_original = 9834.50


#Título de la página
st.title('chancle dineros 💸💸')

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
    
    #cur.execute("DROP TABLE IF EXISTS gastos")
    #cur.execute("CREATE TABLE gastos (id serial PRIMARY KEY, amount integer, name varchar, spender text[], time timestamp);")
    #conn.commit()
    #cur.close()
    
    df = pd.read_sql_query('SELECT * from "gastos"',con=conn, index_col='id')

    
    conn.close()

    container  = st.container()
    total = container.empty()
    total.metric(label="Dinero total restante", value='$' + str(9834.50 - df.amount.sum()), delta= '-$' + str(df.amount.sum()))
    
    col1, col2, col3 = container.columns(3)
    dcol1 = col1.empty()
    dcol2 = col2.empty()
    dcol3 = col3.empty()

    df_koren = df.loc[['Koren' in x for x in df.spender]]
    df_manu = df.loc[['Manu' in x for x in df.spender]]
    df_jimo = df.loc[['Jimo' in x for x in df.spender]]

    new_list = []
    for _, row in df_koren.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_koren['amount'] = new_list

    new_list = []
    df_koren['spender'] = [x[x.index('Koren')] for x in df_koren.spender]
    
    new_list = []
    for _, row in df_manu.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_manu['amount'] = new_list

    new_list = []
    df_manu['spender'] = [x[x.index('Manu')] for x in df_manu.spender]

    new_list = []
    for _, row in df_jimo.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_jimo['amount'] = new_list

    new_list = []
    df_jimo['spender'] = [x[x.index('Jimo')] for x in df_jimo.spender]

    new_list = []
    for _, row in df_koren.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_koren['amount'] = new_list

    new_list = []
    for _, row in df_manu.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_manu['amount'] = new_list

    new_list = []
    for _, row in df_jimo.iterrows():
        new_list.append(row.amount / len(row.spender))
    df_jimo['amount'] = new_list

    dcol1.metric("Koren", "$"+str(round(monto_original/3 - df_koren.amount.sum(),2)), "-$" + str(round(df_koren.amount.sum(),2)))
    dcol2.metric("Manu",  "$"+str(round(monto_original/3 - df_manu.amount.sum(),2)), "-$" + str(round(df_manu.amount.sum(),2)))
    dcol3.metric("Jimo",  "$"+str(round(monto_original/3 - df_jimo.amount.sum(),2)), "-$" + str(round(df_jimo.amount.sum(),2)))
    
    with st.form(key='Nuevo gasto'):
        pwd = st.text_input('contraseña')
        name = st.text_input('Nombre del gasto')
        amount = st.number_input('Monto')
        spender = st.multiselect('¿Quien fue?', ['Koren', 'Manu', 'Jimo'])
        submit_button_type = st.form_submit_button(label='Enviar')
        
        if submit_button_type and pwd.lower()=='patos':
            time = datetime.now()

            up.uses_netloc.append("postgres")
            url = up.urlparse(st.secrets["DATABASE_URL"])
            conn = psycopg2.connect(database=url.path[1:],
            user=url.username,
            password=url.password,  
            host=url.hostname,
            port=url.port
            )
                
            cur = conn.cursor()

            cur.execute("INSERT INTO gastos (amount, name, spender, time) VALUES (%s, %s, %s, %s)", (amount, name, spender, time))
            conn.commit()
            df = pd.read_sql_query('SELECT * from "gastos"',con=conn, index_col='id')
            cur.close()
            conn.close()

            total.metric(label="Dinero total restante", value='$' + str(9834.50 - df.amount.sum()), delta= '-$' + str(df.amount.sum()))
            
            df_koren = df.loc[['Koren' in x for x in df.spender]]
            df_manu = df.loc[['Manu' in x for x in df.spender]]
            df_jimo = df.loc[['Jimo' in x for x in df.spender]]

            new_list = []
            for _, row in df_koren.iterrows():
                new_list.append(row.amount / len(row.spender))
            df_koren['amount'] = new_list

            new_list = []
            df_koren['spender'] = [x[x.index('Koren')] for x in df_koren.spender]
            
            new_list = []
            for _, row in df_manu.iterrows():
                new_list.append(row.amount / len(row.spender))
            df_manu['amount'] = new_list

            new_list = []
            df_manu['spender'] = [x[x.index('Manu')] for x in df_manu.spender]

            new_list = []
            for _, row in df_jimo.iterrows():
                new_list.append(row.amount / len(row.spender))
            df_jimo['amount'] = new_list

            new_list = []
            df_jimo['spender'] = [x[x.index('Jimo')] for x in df_jimo.spender]

            dcol1.metric("Koren", "$"+str(round(monto_original/3 - df_koren.amount.sum(),2)), "-$" + str(round(df_koren.amount.sum(),2)))
            dcol2.metric("Manu",  "$"+str(round(monto_original/3 - df_manu.amount.sum(),2)), "-$" + str(round(df_manu.amount.sum(),2)))
            dcol3.metric("Jimo",  "$"+str(round(monto_original/3 - df_jimo.amount.sum(),2)), "-$" + str(round(df_jimo.amount.sum(),2)))

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

    buffer = 0
    df_koren['acc_amount'] = 0
    for index, row in df_koren.iterrows():
        buffer = buffer + row.amount
        df_koren.loc[index, 'acc_amount'] = buffer
    
    buffer = 0
    df_manu['acc_amount'] = 0
    for index, row in df_manu.iterrows():
        buffer = buffer + row.amount
        df_manu.loc[index, 'acc_amount'] = buffer

    buffer = 0
    df_jimo['acc_amount'] = 0
    for index, row in df_jimo.iterrows():
        buffer = buffer + row.amount
        df_jimo.loc[index, 'acc_amount'] = buffer

    df_divided = pd.concat([df_koren, df_manu, df_jimo], ignore_index=True).sort_values(by='time',ascending=True)

    df_divided.index += 1

    st.write("aaa")
    st.write(df_divided)
    clean_spender = [x[0] for x in df_divided.spender]
    df_divided['spender'] = clean_spender

    st.vega_lite_chart(df_divided,{
    "description": "money over time.",
    "mark": "line",
    "encoding": {
        "x": {"timeUnit": "day hours minutes", "field": "time", "type": "temporal"},
        "y": {"field": "acc_amount", "type": "quantitative"},
        
        "color": {
            "type": "nominal",
            "field": "spender",
    }},}, use_container_width= True, height=400)

    with st.form(key='Gasto a eliminar'):
        pwd = st.text_input('contraseña')
        id = st.number_input('id', min_value=1, step=1)
        
        del_button = st.form_submit_button(label='Borrar')
        if del_button and pwd.lower()=='patos':
            up.uses_netloc.append("postgres")
            url = up.urlparse(st.secrets["DATABASE_URL"])
            conn = psycopg2.connect(database=url.path[1:],
            user=url.username,
            password=url.password,  
            host=url.hostname,
            port=url.port
            )

            cur = conn.cursor()
            cur.execute("DELETE FROM gastos WHERE id = %s;", [id])
            conn.commit()
            cur.close()
            conn.close()



if __name__ == '__main__':
    run()