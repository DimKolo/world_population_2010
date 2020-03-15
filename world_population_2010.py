import json
import pygal
from country_codes import get_country_code
from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS

# Список заполняется данными.
filename = 'population_data.json'
with open(filename) as f:
    pop_data = json.load(f)

# Построение словаря с данными численности населения каждой страны за 2010 год.
cc_populations = {}
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_populations[code] = population

# Группировка стран по 3 уровням населения.
cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
for cc, pop in cc_populations.items():
    if pop < 10000000:
        cc_pops_1[cc] = pop
    elif pop < 1000000000:
        cc_pops_2[cc] = pop
    else:
        cc_pops_3[cc] = pop

# Проверка количества стран на каждом уровне.
print(len(cc_pops_1), len(cc_pops_2), len(cc_pops_3))

wm_style = RS('#336699', base_style=LCS)
wm = pygal.maps.world.World(style=wm_style)
wm.title = 'Население земли в 2010 году, по странам'
wm.add('0 - 10 млн', cc_pops_1)
wm.add('10 млн - 1 млрд', cc_pops_2)
wm.add('>1 млрд', cc_pops_3)
wm.render_to_file('world_population_2010.svg')