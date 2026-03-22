import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

bat_df=pd.read_csv("D:\\PYTHON\\LIBRARIES\\Streamlit\\Mega Project\\Dataset analysis\\odi world cup 2023 dataset\\batting_summary.csv")
ball_df=pd.read_csv("D:\\PYTHON\\LIBRARIES\\Streamlit\\Mega Project\\Dataset analysis\\odi world cup 2023 dataset\\bowling_summary.csv")
match_df=pd.read_csv("D:\\PYTHON\\LIBRARIES\\Streamlit\\Mega Project\\Dataset analysis\\odi world cup 2023 dataset\\match_schedule_results.csv")
player_df=pd.read_csv("D:\\PYTHON\\LIBRARIES\\Streamlit\\Mega Project\\Dataset analysis\\odi world cup 2023 dataset\\world_cup_players_info.csv")

bat_df.drop(index=[161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199],inplace=True)
bat_df.drop(index=[200,202,204,206,208,210,212,214,216,218,220,222,224,226,228,230,232,234,236,238],inplace=True)
bat_df["Strike_Rate"] = pd.to_numeric(bat_df["Strike_Rate"], errors="coerce")

player_df.drop(columns='image_of_player',inplace=True)


st.set_page_config(page_title="2023 ODI World Cup",layout="wide")
st.title("Cricket 2023 ODI World Cup Dashboard")
st.image('D:\PYTHON\LIBRARIES\Streamlit\Mega Project\Dashboard\worldcup2023.png',width=596)

# function for home page
def home_page():
        st.header("Tournament Overview")
        col1,col2,col3,col4,col5=st.columns(5)
# Total Matches, Total Runs, Total Wickets, Highest Team Score, Lowest Team Score
        total_match=len(match_df["Match_no"])
        total_runs=bat_df["Runs"].sum()
        total_wickets=ball_df['Wickets'].sum()
        Highest_runs_score=bat_df.groupby(['Match_no',"Team_Innings"])['Runs'].sum().sort_values(ascending=False).reset_index().head(1)
        Lowest_runs_score=bat_df.groupby(['Match_no',"Team_Innings"])['Runs'].sum().sort_values(ascending=True).reset_index().head(1)
        
        with col1:
            st.metric("Total matches Played",str(total_match)+" matches")
        with col2:
            st.metric("Total runs",str(total_runs)+" runs")
        with col3:
            st.metric("Total wickets",str(total_wickets)+" wickets")
        with col4:
            st.metric("Highest Runs Score",Highest_runs_score['Runs'])
        with col5:
            st.metric("Lowest Runs Score",Lowest_runs_score['Runs'])

# Winner Breakdown (bar chart → number of matches won by each team)
        st.subheader("Number of matches won by each team")
        winner_df=match_df['Winner'].value_counts().reset_index() 
# ploting a bar chart
        fig1,ax1=plt.subplots(figsize=(5,3))
        ax1.bar(winner_df['Winner'],winner_df['count'],color=['#FFCD00','#35CAFE','#0c562e','#000000',"#0aea0d","#052772","#0084C7","#9E0A0AEE","#1A401AFF","#B57507EC"])
        ax1.set_xlabel("Teams")
        ax1.set_ylabel("No.of Matches Won")
        ax1.set_xticklabels(winner_df['Winner'],rotation=60)

        st.pyplot(fig1)

# Venues
        st.subheader("Matches Played in each venue")
        venue_df=match_df['Venue'].value_counts().reset_index()
        fig2,ax2=plt.subplots()
        ax2.pie(venue_df["count"],labels=venue_df["Venue"],autopct="%0.1f%%")
        st.pyplot(fig2)

# adding a column 50s & 100s in dataset of bat_df
def is_50(x):
    if x>=50 and x<100:
        return 1
    else:
        return 0
bat_df["50s"]=bat_df["Runs"].apply(is_50)

def is_100(x):
    if x>=100:
        return 1
    else:
        return 0
bat_df["100s"]=bat_df["Runs"].apply(is_100)

# function for batting analysis
def load_batting():
    st.header("Batting Analysis")
# top 10 batsman
    st.subheader("Top 10 Batsman in Tournament")
    top_batsman=bat_df.groupby("Batsman_Name").agg({"Runs":'sum',"Strike_Rate":'mean'}).sort_values(by='Runs',ascending=False).head(10).reset_index()
    st.dataframe(top_batsman)

# highest score batsman
    st.subheader("Highest Score Batsman")
    high_scores=bat_df.groupby("Batsman_Name")['Runs'].max().sort_values(ascending=False).reset_index().head()
    st.dataframe(high_scores)

# column creation
    col1,col2=st.columns(2)

#most 4s
    fours=bat_df.groupby('Batsman_Name')['4s'].sum().sort_values(ascending=False).reset_index().head(5)
    with col1:
        st.subheader("fours")
        fig,ax=plt.subplots(figsize=(4,4))
        ax.bar(fours["Batsman_Name"],fours['4s'],color=["#0B22A4","#AF079F","#1C980B","#1CB477","#D7DE1C"],width=0.5)
        ax.set_title("Most No of Fourses")
        ax.set_xlabel("Batsman")
        ax.set_ylabel("No.of fours")
        ax.set_xticklabels(fours["Batsman_Name"],rotation=60)

        st.pyplot(fig)

# most 6s
    sixes=bat_df.groupby('Batsman_Name')['6s'].sum().sort_values(ascending=False).reset_index().head(5)
    with col2:
        st.subheader("Sixes")
        fig,ax=plt.subplots(figsize=(4,4))
        ax.bar(sixes["Batsman_Name"],sixes['6s'],color=["#6D0905","#E9DE08","#020301","#07A399","#51034B"],width=0.5)
        ax.set_title("Most No of Sixes")
        ax.set_xlabel("Batsman")
        ax.set_ylabel("No.of sixes")
        ax.set_xticklabels(sixes["Batsman_Name"],rotation=60)

        st.pyplot(fig)

#most boundaries
    boundaries=bat_df.groupby("Batsman_Name")[['4s','6s']].sum()
    boundaries['Total']=boundaries['4s']+boundaries['6s']
    total_boundaries=boundaries.sort_values(by='Total',ascending=False).head()
    st.subheader("Most Boundaries")

    fig,ax=plt.subplots(figsize=(9,4))
    ax.bar(total_boundaries.index,total_boundaries["Total"],color=["#AC92EB","#4FC1E8","#A0D568","#FFCE54","#ED5564"])
    ax.set_title("Most No of Boundaries")
    ax.set_xlabel("Batsman")
    ax.set_ylabel("No.of boundaries")
    ax.set_xticklabels(total_boundaries.index,rotation=60)

    st.pyplot(fig)

# Strike Rate vs Runs Scatter Plot (to see aggressive vs consistent batsmen)
    runs_sr=bat_df.groupby("Batsman_Name").agg({"Runs":'sum',"Strike_Rate":'mean'}).sort_values(by="Runs",ascending=False).head(10)
    st.subheader("Top 10 Batsman aggressive vs consistent batsmen")

    fig1,ax1=plt.subplots(figsize=(10,5))
    ax1.scatter(runs_sr['Runs'],runs_sr["Strike_Rate"])
    ax1.set_xlabel("Runs")
    ax1.set_ylabel("Strike_Rate")
    ax1.set_title("Runs V/S Avg")
    for i in range(runs_sr.shape[0]):
        ax1.text(runs_sr["Runs"].values[i],runs_sr["Strike_Rate"].values[i],runs_sr.index[i])

    st.pyplot(fig1)

# most fifties in tournament
    fifties=bat_df.groupby("Batsman_Name")['50s'].sum().sort_values(ascending=False).head().reset_index()
    st.subheader("Most Fifites")
    st.dataframe(fifties)

# most Hundereds in tournament
    hundereds=bat_df.groupby("Batsman_Name")['100s'].sum().sort_values(ascending=False).head().reset_index()
    st.subheader("Most Hundereds")
    st.dataframe(hundereds)

# Dismissal Types Distribution (pie chart → bowled, LBW, caught, run-out)
    def t_d(out):
        if str(out).lower().startswith("c"):
            return "Caught out"
        elif str(out).lower().startswith("b"):
            return "Bowled"
        elif str(out).lower().startswith("l"):
            return "LBW"
        elif str(out).lower().startswith("r"):
            return "Run out"
        else:
            return None

    bat_df['Type_of_dismissal']=bat_df['Dismissal'].apply(t_d)

    type_dismissal_df=bat_df["Type_of_dismissal"].value_counts().reset_index()

    col3,col4=st.columns(2)
    with col3:
        st.subheader("Dismissal Types Distribution")

        fig2,ax2=plt.subplots(figsize=(4,4))
        ax2.pie(type_dismissal_df['count'],labels=type_dismissal_df['Type_of_dismissal'],autopct='%0.1f%%')
        st.pyplot(fig2)
    
    with col4:
        pass

# creating a dataframe for bowling analysis
bowl=ball_df.groupby("Bowler_Name").agg({'Match_no':'count','Wickets':'sum','Runs':'sum','Economy':'mean'})
bowl['Average']=bowl['Runs']/bowl['Wickets']
bowl.rename(columns={'Match_no':'Matches'},inplace=True)

# function for bowling analysis
def load_bowling():
    st.header("Bowling Analysis")

# bowler Details
# top bowler leaderboard
    st.subheader("Top Bowler in Tournament")
    top_bowler=bowl.sort_values(by='Wickets',ascending=False)[['Matches','Economy','Wickets']].head()
    st.dataframe(top_bowler)
# top bowling Average
    st.subheader("Bowling Average")
    top_average=bowl.sort_values(by='Average',ascending=True)[['Matches','Wickets','Average']].head()
    st.dataframe(top_average)
# top bowler economical 
    st.subheader("Most Economical Bowler")
    top_economical=bowl.sort_values(by='Economy',ascending=True)[['Matches','Wickets','Economy']].head()
    st.dataframe(top_economical)
# most 5 wicket haul
    st.subheader("Most 5w haul")
    def five_haul(x):
        if x>=5:
            return 1
        else:
            return 0
    ball_df['5w_haul']=ball_df['Wickets'].apply(five_haul)
    five_wicket=ball_df.groupby("Bowler_Name")['5w_haul'].sum().sort_values(ascending=False).head()

    col1,col2=st.columns(2)
    with col1:
        st.dataframe(five_wicket)
    with col2:
        fig,ax=plt.subplots(figsize=(4,2))
        ax.bar(five_wicket.index,five_wicket.values,color=['#f14666',"#02576D","#ffcdaa","#3B8130","#1BB5B5"])
        ax.set_title("Most 5w Hauls")
        ax.set_xlabel('Bowlers')
        ax.set_ylabel('No.of 5W hauls')
        ax.set_xticklabels(five_wicket.index,rotation=60)
        st.pyplot(fig)
        
# function for player details
def load_player_details(player_name):
    st.title("Player Details")
    # player name
    st.metric("Player Name:",player_name,border=True)

# player details
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Team Name",player_df[player_df['player_name']==player_name]['team_name'].iloc[0])
    with col2:
        st.metric("Batting Style",player_df[player_df['player_name']==player_name]['battingStyle'].iloc[0])
    with col3:
        st.metric("Bowling Style",player_df[player_df['player_name']==player_name]['bowlingStyle'].iloc[0])
    with col4:
        st.metric("Playing Role",player_df[player_df['player_name']==player_name]['playingRole'].iloc[0])
    
    st.subheader("Description:")
    st.write(player_df[player_df['player_name']==player_name]['description'].iloc[0])

    st.header('Player Stats')

    # player batting stats    
    st.subheader("Batting Stats:")
    # batsman total runs
    batsman=bat_df[['Batsman_Name',"Runs","Balls",'4s','6s','Strike_Rate','50s','100s']]
    bat_runs=batsman.groupby('Batsman_Name')['Runs'].sum().reset_index()
    total_runs=bat_runs[bat_runs['Batsman_Name']==player_name]['Runs'].values

    col5,col6,col7,col8,col9=st.columns(5)
    with col5:
        st.metric("Total Runs",total_runs)

    # batsman half centuries
    bat_50s=batsman.groupby('Batsman_Name')['50s'].sum().reset_index()
    half_century=bat_50s[bat_50s['Batsman_Name']==player_name]['50s'].values
    
    with col6:
        st.metric("Half Century",half_century)
    
    # batsman centuries
    bat_100s=batsman.groupby('Batsman_Name')['100s'].sum().reset_index()
    century=bat_100s[bat_100s['Batsman_Name']==player_name]['100s'].values
    
    with col7:
        st.metric("Century",century)

    # batsman Strike rate
    bat_strike=batsman.groupby('Batsman_Name')['Strike_Rate'].mean().reset_index()
    batsman_strike_rate=bat_strike[bat_strike['Batsman_Name']==player_name]['Strike_Rate'].values

    with col8:
        st.metric("Strike Rate",batsman_strike_rate)
    
    # batsman high score:
    bat_high=batsman.groupby('Batsman_Name')['Runs'].max().reset_index()
    batsman_high_score=bat_high[bat_high['Batsman_Name']==player_name]['Runs'].values

    with col9:
        st.metric("High Score",batsman_high_score)
    
    # Runs per match scored by batsman
    st.write("Runs Per Match")
    runs=bat_df.groupby(['Batsman_Name','Match_no'])['Runs'].sum().reset_index()
    run1=runs[runs['Batsman_Name']==player_name][['Match_no','Runs']]
    st.dataframe(run1)
    
    st.subheader("Bowling Stats")
    col1,col2,col3=st.columns(3)

    bowl.reset_index(inplace=True)

    # total wickets
    total_wicket=bowl[bowl['Bowler_Name']==player_name]['Wickets'].iloc[0]
    with col1:
        st.metric("Total Wickets:",total_wicket)

    # economy
    economy=bowl[bowl['Bowler_Name']==player_name]['Economy'].values
    with col2:
        st.metric("Economy",economy)

    # average
    average=bowl[bowl['Bowler_Name']==player_name]['Average'].values
    with col3:
        st.metric("Average",average)
    
    # wicket per match
    st.write("Wicket per match")
    wicket=ball_df.groupby(['Bowler_Name','Match_no'])['Wickets'].sum().reset_index()
    wicket1=wicket[wicket['Bowler_Name']==player_name][['Match_no','Wickets']]
    st.dataframe(wicket1)

# sidebar
st.sidebar.title("2023 World Cup Analysis")
selected_analysis=st.sidebar.selectbox("Select One",["Home Page","Batting Analysis","Bowling Analysis","Player Details"])

if selected_analysis=='Home Page':
    btn1=st.sidebar.button("Home Page Details")
    if btn1:
        home_page()
elif selected_analysis=='Batting Analysis':
    btn2=st.sidebar.button("Batting Analysis")
    if btn2:
        load_batting()
elif selected_analysis=='Bowling Analysis':
    btn3=st.sidebar.button("Bowling Analysis")
    if btn3:
        load_bowling()
else:
    player_name=st.sidebar.selectbox("Select Player",list(player_df['player_name'].sort_values()))
    btn4=st.sidebar.button("Player infomation")
    if btn4:
        load_player_details(player_name)
