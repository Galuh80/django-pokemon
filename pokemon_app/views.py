import random
from datetime import datetime
import requests
from django.shortcuts import render

def home(request):
    if 'search' in request.GET:
        search_query = request.GET['search']
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{search_query.lower()}')
        if response.status_code == 200:
            pokemon = response.json()
            return render(request, 'pokemon_app/home.html', {'pokemon': pokemon})
    return render(request, 'pokemon_app/home.html')

def pokemon_detail(request, name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
    if response.status_code == 200:
        pokemon = response.json()
        return render(request, 'pokemon_app/pokemon_detail.html', {'pokemon': pokemon})
    return render(request, 'pokemon_app/home.html', {'error': 'Pokemon not found'})

def ability_detail(request, name):
    response = requests.get(f'https://pokeapi.co/api/v2/ability/{name.lower()}')
    if response.status_code == 200:
        ability = response.json()
        return render(request, 'pokemon_app/ability_detail.html', {'ability': ability})
    return render(request, 'pokemon_app/home.html', {'error': 'Ability not found'})

def gacha(request):
    if request.method == 'POST':
        location = request.POST.get('location', '')
        response = requests.get(f'https://pokeapi.co/api/v2/location-area/{location.lower()}')
        if response.status_code == 200:
            location_data = response.json()
            pokemon_encounters = location_data['pokemon_encounters']
            
            current_hour = datetime.now().hour
            is_night = 18 <= current_hour < 6
            
            valid_encounters = [
                encounter for encounter in pokemon_encounters
                if any(method['time'] == 'night' if is_night else method['time'] == 'day'
                       for method in encounter['version_details'][0]['encounter_details'])
            ]
            
            if valid_encounters:
                chosen_encounter = random.choice(valid_encounters)
                pokemon_name = chosen_encounter['pokemon']['name']
                
                # Fetch pokemon details
                pokemon_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
                if pokemon_response.status_code == 200:
                    pokemon = pokemon_response.json()
                    
                    # Adjust gender ratio
                    gender_rate = pokemon.get('gender_rate', -1)
                    if gender_rate != -1:
                        female_ratio = (gender_rate / 8) * 1.5  # Increase female ratio by 50%
                        is_female = random.random() < female_ratio
                        gender = 'Female' if is_female else 'Male'
                    else:
                        gender = 'Unknown'
                    
                    return render(request, 'pokemon_app/gacha_result.html', {'pokemon': pokemon, 'gender': gender})
            
            return render(request, 'pokemon_app/gacha.html', {'error': 'No Pokemon found in this location at this time'})
        
    return render(request, 'pokemon_app/gacha.html')