import folium


from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entity = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        if localtime(pokemon_entity.disappeared_at) > localtime() > localtime(pokemon_entity.appeared_at):
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(f'/media/{pokemon_entity.Pokemon.image}'),
            )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'/media/{pokemon.image}'),
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    related_pokemons = requested_pokemon.next_evolutions.all()
    next_evolution = {}
    for related_pokemon in related_pokemons:
        if related_pokemon:
            next_evolution = {
                'title_ru': related_pokemon.title,
                'pokemon_id': related_pokemon.id,
                'img_url': request.build_absolute_uri(f'/media/{related_pokemon.image}'),
            }

    previous_evolution = {}
    if requested_pokemon.evolution:
        previous_evolution = {
            'title_ru': requested_pokemon.evolution.title,
            'pokemon_id': requested_pokemon.evolution.id,
            'img_url': request.build_absolute_uri(f'/media/{requested_pokemon.evolution.image}'),
        }
    pokemon_info = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(f'/media/{requested_pokemon.image}'),
        'description': requested_pokemon.description,
        'next_evolution': next_evolution,
        'previous_evolution': previous_evolution,
    }
    pokemons_entity = PokemonEntity.objects.filter(Pokemon__id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entity:
        if localtime(pokemon_entity.disappeared_at) > localtime() > localtime(pokemon_entity.appeared_at):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(f'/media/{pokemon_entity.Pokemon.image}'),
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
