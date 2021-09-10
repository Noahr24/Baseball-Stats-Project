from flask import Blueprint, render_template, request
from flask_login import login_required
import requests
from requests.sessions import extract_cookies_to_jar
from baseball_api.forms import Player
import json
import pprint

pitchers = Blueprint('pitchers', __name__, template_folder='pitcher_templates')


@pitchers.route('/pitchers', methods=['GET', 'POST'])
@login_required
def players():
    form = Player()
    data = []
    if request.method == 'POST':
        name_part = form.name.data
        #Start API call here
        headers = {"Content-Type": "application/json"}
        response = requests.get(f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='{name_part}%25'", headers=headers)


        # This pulls the player id to use to pull up stats
        player_id = response.json()['search_player_all']['queryResults']['row']['player_id']
        

        # This is the API call to gets player_info
        response1 = requests.get(f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id={player_id}", headers=headers)


        # This is the API call to get Pitching stats
        r = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id={player_id}", headers=headers)
        

        # This is setting the API info to a variable for each stat that is wanted
        player_name = response1.json()['player_info']['queryResults']['row']["name_display_first_last_html"]
        player_position = response1.json()['player_info']['queryResults']['row']["primary_position_txt"]
        w = r.json()['sport_career_pitching']['queryResults']["row"]['w']
        l = r.json()['sport_career_pitching']['queryResults']["row"]['l']
        era = r.json()['sport_career_pitching']['queryResults']["row"]['era']
        g = r.json()['sport_career_pitching']['queryResults']["row"]['g']
        gs = r.json()['sport_career_pitching']['queryResults']["row"]['gs']
        sv = r.json()['sport_career_pitching']['queryResults']["row"]['sv']
        ip = r.json()['sport_career_pitching']['queryResults']["row"]['ip']
        so = r.json()['sport_career_pitching']['queryResults']["row"]['so']
        whip = r.json()['sport_career_pitching']['queryResults']["row"]['whip']


        # This is appending all of the API info into data so that it can be displayed on the HTML
        data.append(player_name)
        data.append(player_position)
        data.append(w)
        data.append(l)
        data.append(era)
        data.append(g)
        data.append(gs)
        data.append(sv)
        data.append(ip)
        data.append(so)
        data.append(whip)
        
        r = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id={player_id}", headers=headers)


    return render_template('pitchers.html', form=form, data=data)