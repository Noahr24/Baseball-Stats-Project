from flask import Blueprint, render_template, request
from flask_login import login_required
import requests
from baseball_api.forms import Player

team = Blueprint('team', __name__, template_folder='player_templates')


@team.route('/players', methods=['GET', 'POST'])
@login_required
def players():
    form = Player()
    data = {}
    if request.method == 'POST':
        player = form.name.data
        #Start API call here
        headers = {"Content-Type": "application/json"}
        data = requests.get(f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='{player}", headers=headers)

    return render_template('players.html', form=form, data=data)


