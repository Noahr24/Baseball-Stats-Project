from flask import Blueprint, render_template, request
from flask_login import login_required
import requests
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


        # This is the API call to get hitting stats
        r = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id={player_id}", headers=headers)
        

        # This is setting the API info to a variable for each stat that is wanted
        player_name = response1.json()['player_info']['queryResults']['row']["name_display_first_last_html"]
        player_position = response1.json()['player_info']['queryResults']['row']["primary_position_txt"]
        at_bat = r.json()['sport_career_hitting']['queryResults']["row"]['ab']
        h = r.json()['sport_career_hitting']['queryResults']["row"]['h']
        hr = r.json()['sport_career_hitting']['queryResults']["row"]['hr']
        ba = r.json()['sport_career_hitting']['queryResults']["row"]['avg']
        runs = r.json()['sport_career_hitting']['queryResults']["row"]['r']
        rbi = r.json()['sport_career_hitting']['queryResults']["row"]['rbi']
        sb = r.json()['sport_career_hitting']['queryResults']["row"]['sb']
        obp = r.json()['sport_career_hitting']['queryResults']["row"]['obp']
        slg = r.json()['sport_career_hitting']['queryResults']["row"]['slg']


        # This is appending all of the API info into data so that it can be displayed on the HTML
        data.append(player_name)
        data.append(player_position)
        data.append(at_bat)
        data.append(h)
        data.append(hr)
        data.append(ba)
        data.append(runs)
        data.append(rbi)
        data.append(sb)
        data.append(obp)
        data.append(slg)
        
        r = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type='R'&player_id={player_id}", headers=headers)


    return render_template('pitchers.html', form=form, data=data)