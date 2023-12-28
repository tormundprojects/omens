import streamlit as st
import pandas as pd 

path_db="database/omens_database.csv"

@st.cache_data
def get_db():
    return pd.read_csv(path_db)

df = get_db()
df["season"] = df["season"].astype("string")

with st.sidebar:
    st.subheader("Filtros")
    base_min = st.number_input("Qual Minuto base?",min_value=0,max_value=90)
    placar_home = st.number_input("Qual Placar Mandante?",min_value=0,max_value=5)
    placar_away = st.number_input("Qual Placar Visitante?",min_value=0,max_value=5)
    country = st.selectbox("Pais", df["country"].unique())
    league = st.selectbox("Qual Liga?",df[df["country"]==country]["league"].unique())
    min_home_odds = st.number_input("Min Odds Casa",min_value=1.,max_value=1000.,step=0.05,format="%.2f",value=1.1,)
    max_home_odds = st.number_input("Max Odds Casa",min_value=1.,max_value=1000.,step=0.05,format="%.2f",value=1.8,)
    min_over25_odds = st.number_input("Min Odds Over25",min_value=1.,max_value=1000.,step=0.05,format="%.2f",value=1.1,)
    max_over25_odds = st.number_input("Max Odds Over25",min_value=1.,max_value=1000.,step=0.05,format="%.2f",value=1.8,)
    home_min_ppg = st.number_input("Min PPG Mandante",min_value=0.,max_value=3.,step=0.1,value=2.)
    home_max_ppg = st.number_input("Max PPG Mandante",min_value=0.,max_value=3.,step=0.1,value=3.)
    
    team_name = st.selectbox("Qual Time",df[(df["league"]==league) & (df["country"]==country)]["home_name"].unique())
    home_option = st.checkbox("Mandante")
    away_option = st.checkbox("Visitante")
    container = st.container()
    #all_seasons = st.checkbox("Todas Temporadas")
    #if all_seasons:        
    seasons = st.multiselect("Qual Temporada?",
                                        df[(df["league"]==league) & (df["country"]==country)]["season"].unique(),
                                        df[(df["league"]==league) & (df["country"]==country)]["season"].unique()
                                        )
    #else:
    #    seasons = container.multiselect("Qual Temporada?",df[(df["league"]==league) & (df["country"]==country)]["season"].unique())

st.subheader("Minuto " + str(base_min)+ " com o Placar em "+ str(placar_home) + " vs " + str(placar_away))
if (home_option & away_option):
    df_filtered = df.loc[
    (df["homeScore"+str(base_min)]==placar_home) & 
    (df["awayScore"+str(base_min)]==placar_away) &
    ((df["country"]==country))& ((df["league"]==league)) &
    (df["home_ppg"]>= home_min_ppg) & (df["home_ppg"]<= home_max_ppg) &
    (df["odds_ft_1"]>= min_home_odds) & (df["odds_ft_1"]<= max_home_odds) &
    (df["odds_ft_over25"]>= min_over25_odds) & (df["odds_ft_over25"]<= max_over25_odds) &
    ((df["home_name"]==team_name) | (df["away_name"]==team_name))&
    (df["season"].isin(seasons))
    ].reset_index()
elif( home_option):    
    df_filtered = df.loc[
    (df["homeScore"+str(base_min)]==placar_home) & 
    (df["awayScore"+str(base_min)]==placar_away) &
    ((df["country"]==country))& ((df["league"]==league)) &
    (df["home_ppg"]>= home_min_ppg) & (df["home_ppg"]<= home_max_ppg) &
    (df["odds_ft_1"]>= min_home_odds) & (df["odds_ft_1"]<= max_home_odds) &
    (df["odds_ft_over25"]>= min_over25_odds) & (df["odds_ft_over25"]<= max_over25_odds) &
    ( ( df["home_name"]==team_name))&
    (df["season"].isin(seasons))
    ].reset_index()
elif(away_option):    
    df_filtered = df.loc[
    (df["homeScore"+str(base_min)]==placar_home) & 
    (df["awayScore"+str(base_min)]==placar_away) &
    ((df["country"]==country))& ((df["league"]==league)) &
    (df["home_ppg"]>= home_min_ppg) & (df["home_ppg"]<= home_max_ppg) &
    (df["odds_ft_1"]>= min_home_odds) & (df["odds_ft_1"]<= max_home_odds) &
    (df["odds_ft_over25"]>= min_over25_odds) & (df["odds_ft_over25"]<= max_over25_odds) &
    ( ( df["away_name"]==team_name))&
    (df["season"].isin(seasons))
    ].reset_index()
else:
    df_filtered = df.loc[
    (df["homeScore"+str(base_min)]==placar_home) & 
    (df["awayScore"+str(base_min)]==placar_away) &    
    ((df["country"]==country))& ((df["league"]==league)) &
    (df["home_ppg"]>= home_min_ppg) & (df["home_ppg"]<= home_max_ppg) &
    (df["odds_ft_1"]>= min_home_odds) & (df["odds_ft_1"]<= max_home_odds) &
    (df["odds_ft_over25"]>= min_over25_odds) & (df["odds_ft_over25"]<= max_over25_odds) &
    (df["season"].isin(seasons))
    ].reset_index()
tot_jogos =len(df_filtered)
st.write("Jogos: ", tot_jogos)

gols0=0
gols1=0
gols2=0
gols3=0
gols4=0
gols_home0=0
gols_home1=0
gols_home2=0
gols_home3=0
gols_away0=0
gols_away1=0
gols_away2=0
gols_away3=0
filtered_home_win = 0
filtered_draw_win = 0
filtered_away_win = 0
for index,row in df_filtered.iterrows():
    if row["homeGoalCount"]>row["awayGoalCount"]:
        filtered_home_win+=1
    elif row["homeGoalCount"]<row["awayGoalCount"]:
        filtered_away_win+=1
    else:
        filtered_draw_win+=1
    tot_goal = row["totalGoalCount"]-(placar_home+placar_away)
    if(tot_goal == 0):
        gols0+=1
        gols_home0+=1
        gols_away0+=1
    elif(tot_goal==1):
        gols1+=1
    elif(tot_goal==2):
        gols2+=1
    elif(tot_goal==3):
        gols3+=1
    else:
        gols4+=1
       
over1 = tot_jogos-gols0
over2 = tot_jogos-gols0-gols1
over3 = tot_jogos-gols0-gols1-gols2
over4 = tot_jogos-gols0-gols1-gols2-gols3

st.write("Sem gols: ", gols0,"Odds minima: ", 1000 if(gols0 == 0 ) else round(1/ (gols0/tot_jogos),2))            
st.write("1 Gol: ", over1,"Odds minima: ", 1000 if(over1 == 0 ) else round(1/(over1/tot_jogos),2))            
st.write("2 Gols: ", over2,"Odds minima: ", 1000 if(over2 == 0 ) else round(1/(over2/tot_jogos),2))
st.write("3 Gols: ", over3,"Odds minima: ", 1000 if(over3 == 0 ) else round(1/(over3/tot_jogos),2))            
st.write("4+ Gols: ", over4,"Odds minima: ", 1000 if(over4 == 0 ) else round(1/(over4/tot_jogos),2))            

st.write("Vitória Mandante:", 0 if tot_jogos == 0 else round(filtered_home_win/tot_jogos,2))
st.write("Vitória Empate:", 0 if tot_jogos == 0 else round(filtered_draw_win/tot_jogos,2))
st.write("Vitória Visitante:", 0 if tot_jogos == 0 else round(filtered_away_win/tot_jogos,2))
df_filtered[["home_name","away_name","season","homeScore"+str(base_min),"awayScore"+str(base_min),"homeGoalCount","awayGoalCount"]]
