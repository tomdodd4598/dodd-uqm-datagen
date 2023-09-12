import math
import random
import typing

from dataclasses import dataclass
from PIL import Image

random.seed(25565)


def clamp(x, a, b):
    return a if x < a else (b if x > b else x)


def random_latitude():
    return round(56.9774696 * math.asin(random.uniform(-1.0, 1.0)))


def random_longitude():
    return round(random.uniform(-179.49, 180.49))


@dataclass
class MineralType:
    name: str
    category: str
    value: int
    density: int


mineral_types = {}

mineral_value_map = {
    'Common': 1,
    'Corrosive': 2,
    'Base Metal': 3,
    'Noble Gas': 4,
    'Rare Earth': 5,
    'Precious': 6,
    'Radioactive': 8,
    'Exotic': 25,
}


@dataclass
class LifeformType:
    name: str
    behaviour: str
    intelligence: int
    value: int
    health: int
    speed: int
    danger: int


lifeform_types = []

lifeform_behaviour_map = {
    'Sessile': 's',
    'Wanderer': 'w',
    'Coward': 'c',
    'Hunter': 'h',
}

lifeform_intelligence_map = {
    'N/A': 0,
    'Low': 1,
    'Moderate': 2,
    'High': 3,
}

lifeform_speed_map = {
    'Static': 0,
    'Slow': 1,
    'Med': 2,
    'Fast': 3,
}

lifeform_danger_map = {
    'Harmless': 0,
    'Low': 1,
    'Moderate': 2,
    'EXTREME': 3,
}


def get_planet_lifeform_types(count):
    types = []
    for _ in range(count):
        lifeform_type = random.choice(lifeform_types)
        while lifeform_type.name == 'Evil One' \
                or lifeform_type.name == 'Brainbox Bulldozers' \
                or lifeform_type.name == 'ZEX\'s Beauty':
            lifeform_type = random.choice(lifeform_types)
        types.append(lifeform_type)
    return types


@dataclass
class PlanetType:
    name: str
    size: str
    surface: str
    color: str
    tectonics: (int, int)
    density: (float, float)
    weather: (int, int)
    minerals: list


planet_types = []


def get_planet_type():
    planet_type = random.choice(planet_types)
    if planet_type.name == 'Emerald' or planet_type.name == 'Ruby' or planet_type.name == 'Sapphire':
        if random.getrandbits(1):
            planet_type = random.choice(planet_types)

    while planet_type.name == 'Rainbow' or planet_type.name == 'Shattered':
        planet_type = random.choice(planet_types)

    return planet_type


def get_moon_type():
    moon_type = random.choice(planet_types)
    if moon_type.name == 'Emerald' or moon_type.name == 'Ruby' or moon_type.name == 'Sapphire':
        if random.getrandbits(1):
            moon_type = random.choice(planet_types)

    while moon_type.size == 'l' or moon_type.name == 'Rainbow' or moon_type.name == 'Shattered':
        moon_type = random.choice(planet_types)

    return moon_type


planet_size_map = {
    'Small': 's',
    'Large': 'm',
    'Giant': 'l',
}

planet_surface_map = {
    'Cratered': 'Cratered',
    'Topo': 'Smooth',
    'Gas': 'Gaseous',
}

planet_color_map = {
    'Blue': 'b',
    'Cyan': 'c',
    'Green': 'g',
    'Orange': 'o',
    'Purple': 'p',
    'Red': 'r',
    'Violet': 'v',
    'White': 'w',
    'Yellow': 'y',
    'Various': 'various',
    'Rainbow': 'rainbow',
}

planet_tectonics_map = {
    'No': (1, 1),
    'Low': (2, 3),
    'Med': (4, 5),
    'High': (6, 7),
    'Super': (8, 8),
}

planet_density_map = {
    'Gas': (0.50, 1.50),
    'Light': (1.75, 3.25),
    'Low': (2.75, 4.25),
    'Normal': (3.75, 5.25),
    'High': (4.75, 6.25),
    'Super': (5.75, 7.25),
}

planet_weather_map = {
    'Nothing': (1, 1),
    'Light': (2, 3),
    'Medium': (4, 5),
    'Heavy': (6, 7),
    'Super Thick': (8, 8),
}


def parse_planet_minerals(part):
    minerals = []
    infos = part.split(', ')
    for info in infos:
        name, amount = info.split('(')
        desc = amount[:-1]
        mineral_type = mineral_types[name.strip()]
        mineral_quantity = planet_mineral_quantity_map[desc]
        mineral_quality = planet_mineral_quality_map[desc]
        minerals.append((mineral_type, mineral_quantity, mineral_quality))
    return minerals


star_color_map = {
    'Red': 'r',
    'Orange': 'o',
    'Yellow': 'y',
    'Green': 'g',
    'White': 'w',
    'Blue': 'b',
}

# star_mid_colors = ['o', 'y', 'w']


def get_star_color(c):
    # return random.choice(star_mid_colors) if c == 'Green' else star_color_map[c]
    return star_color_map[c]


star_temperature_map = {
    'r': (2100.0, 3699.9),
    'o': (3800.0, 4899.9),
    'y': (5000.0, 6299.9),
    'g': (5500.0, 5999.9),
    'w': (6700.0, 10199.9),
    'b': (11400.0, 78399.9),
}

star_size_map = {
    'Dwarf': 's',
    'Giant': 'm',
    'Super-Giant': 'l',
}

star_radius_map = {
    's': (0.25, 8.0),
    'm': (18.0, 160.0),
    'l': (600.0, 1550.0),
}


def get_star_luminosity(temperature, radius):
    t2 = temperature * temperature
    return 3.45490e11 * t2 * t2 * radius * radius


def get_star_mass(luminosity):
    luminosity /= 3.828e26
    return 0.772551 * luminosity ** 0.3 + 0.0000503279 * math.sqrt(luminosity) +\
        3.12500e-5 * luminosity * math.tanh(1.0e-7 * luminosity)


system_planet_max_count_map = {
    's': 9,
    'm': 9,
    'l': 9,
}

system_planet_chance_map = {
    's': 0.6,
    'm': 0.8,
    'l': 1.0,
}


def get_planet_tectonics_modifier(i):
    return random.randint(0, (8 - i) // 4)


def get_planet_weather_modifier(i):
    return random.randint(0, i // 4)


def get_planet_orbit(star_radius, i):
    j = i + 1.0
    z = 0.05 / j
    return 0.05 * j * j * j * (1.0 + random.uniform(-z, z)) * math.sqrt(star_radius)


def get_moon_orbit(planet_radius, j):
    k = j + 1.0
    z = 0.075 / k
    return 15.0 * k * k * (1.0 + random.uniform(-z, z)) * planet_radius ** 0.125


def get_planet_atmosphere(weather):
    if weather == 1:
        return 0.0
    f = weather - 1.5
    f = random.uniform(f - 0.5, f + 0.5)
    return 2.0 * f * f


def get_planet_temperature(luminosity, orbit, atmosphere):
    t4 = luminosity / (6.363135e16 * orbit * orbit)
    modifier = 5.522
    if atmosphere < 126.0:
        modifier = 0.1485 * atmosphere ** (1.1185 - math.log1p(0.04 * math.sqrt(atmosphere)))
    if modifier > 1.0:
        modifier = math.sqrt(modifier)
    return math.sqrt(math.sqrt(t4 * (1.0 + modifier)))


planet_radius_map = {
    's': (0.16, 0.38),
    'm': (0.62, 2.2),
    'l': (3.4, 14.8),
}

moon_radius_modifier_map = {
    's': (0.08, 0.24),
    'm': (0.24, 0.72),
}


def get_moon_radius(size, planet_radius):
    return random.uniform(*moon_radius_modifier_map[size]) * planet_radius


def get_planet_mass(density, radius):
    return 4.18879020478639 * density * radius * radius * radius


def get_planet_day(weather, mass):
    z = 0.0232174 + mass ** -0.298527
    return 0.5 * (z + max(0.0, random.gauss(weather, weather)) ** z)


def get_planet_tilt():
    return int(random.gauss(0.0, 180.0)) % 180


def get_moon_tilt(planet_tilt):
    return int(random.gauss(planet_tilt, 180.0)) % 180


def get_planet_fuel_use(type_name, radius, mass):
    f = 0.5 * math.sqrt(mass / radius)
    if type_name == 'Magnetic':
        f *= 2.0
    return f


def get_planet_lifeform_quantity(atmosphere, temperature):
    if atmosphere > 0.0 and temperature > 283.0:
        a = min(atmosphere, 1.0 / atmosphere) - 0.025
        b = math.log(1.0 + 80.1711 * temperature)
        if a > 0 and temperature < 284.197 + 3.60038 * b * b:
            a *= 20.0
            if a < 1.0:
                return 1 if a > 2.0 * random.random() else 0
            else:
                return random.randint(0, int(a))
    return 0


moon_max_count_map = {
    's': 1,
    'm': 2,
    'l': 4,
}

moon_chance_map = {
    's': 0.4,
    'm': 0.6,
    'l': 0.8,
}

moon_size_map = {
    's': ['s'],
    'm': ['s', 'm'],
}

planet_mineral_quantity_map = {
    'Trace': (0, 1),
    'Light': (0, 4),
    'Medium': (0, 4),
    'Heavy': (0, 4),
    'Huge': (0, 8),
}

planet_mineral_quality_map = {
    'Trace': (1, 10),
    'Light': (1, 10),
    'Medium': (6, 15),
    'Heavy': (11, 20),
    'Huge': (11, 20),
}

system_mineral_bonus_map = {
    's': (0, 2),
    'm': (2, 6),
    'l': (6, 10),
}


@dataclass
class PlanetData:
    number: int
    type_name: str
    surface: str
    orbit: float
    atmosphere: float
    temperature: float
    weather: int
    tectonics: int
    mass: float
    radius: float
    gravity: float
    day: float
    tilt: int
    fuel_use: float
    minerals: list
    lifeforms: list
    moons: list
    direction: int
    initial_angle: float


def planet_str(p, is_moon):
    minerals = ';;'.join([f'{m[0].name},{m[1]},{m[2]},{m[3]}' for m in p.minerals])
    lifeforms = ';;'.join([f'{life.name}' for life in p.lifeforms])
    moons = '' if is_moon else '^^'.join([planet_str(m, True) for m in p.moons])
    s = '::' if is_moon else '??'
    return f'{p.number}{s}{p.type_name}{s}{p.surface}{s}{p.orbit}{s}{p.atmosphere}{s}{p.temperature}{s}{p.weather}{s}' \
           f'{p.tectonics}{s}{p.mass}{s}{p.radius}{s}{p.gravity}{s}{p.day}{s}{p.tilt}{s}{p.fuel_use}{s}' \
           f'{minerals}{s}{lifeforms}{s}{moons}{s}{p.direction}{s}{p.initial_angle}'


def get_planet(is_moon, i, star_size, star_radius, star_luminosity, system_rotation, radius=None, tilt=None):
    planet_type = get_moon_type() if is_moon else get_planet_type()
    type_name = planet_type.name
    size = random.choice(moon_size_map[planet_type.size]) if is_moon else planet_type.size
    surface = planet_type.surface
    # color = planet_type.color
    tectonics = random.randint(*planet_type.tectonics)
    density = random.uniform(*planet_type.density)
    weather = random.randint(*planet_type.weather)

    tectonics += get_planet_tectonics_modifier(i)
    tectonics = clamp(tectonics, 1, 8)
    weather += get_planet_weather_modifier(i)
    weather = clamp(weather, 1, 8)

    orbit = get_planet_orbit(star_radius, i)
    if radius is None:
        radius = random.uniform(*planet_radius_map[size])
    else:
        radius = get_moon_radius(size, radius)
    direction = -system_rotation if random.getrandbits(3) == 0 else system_rotation

    atmosphere = get_planet_atmosphere(weather)
    temperature = get_planet_temperature(
        star_luminosity, orbit, atmosphere
    )
    mass = get_planet_mass(density, radius)
    gravity = mass / (radius * radius)
    day = get_planet_day(weather, mass)
    if tilt is None:
        tilt = get_planet_tilt()
    else:
        tilt = get_moon_tilt(tilt)

    initial_angle = random.uniform(0.0, 6.28318530718)
    fuel_use = get_planet_fuel_use(type_name, radius, mass)

    minerals = []
    for mineral_type, mineral_quantity, mineral_quality in planet_type.minerals:
        for _ in range(random.randint(*mineral_quantity)):
            quality = random.randint(*mineral_quality)
            quality += random.randint(*system_mineral_bonus_map[star_size])
            latitude = random_latitude()
            longitude = random_longitude()
            minerals.append((mineral_type, quality, latitude, longitude))

    lifeforms = []
    lifeform_quantity = get_planet_lifeform_quantity(
        atmosphere, temperature
    )
    planet_lifeform_types = get_planet_lifeform_types(
        1 + int(math.sqrt(lifeform_quantity))
    )
    for _ in range(lifeform_quantity):
        lifeforms.append(random.choice(planet_lifeform_types))

    moons = []
    if not is_moon:
        moon_probability = moon_chance_map[star_size]
        for j in range(moon_max_count_map[size]):
            if random.random() < moon_probability:
                moon = get_planet(True, i, star_size, star_radius, star_luminosity, system_rotation, radius, tilt)
                moon.number = j
                moon.orbit = get_moon_orbit(radius, j)
                moons.append(moon)

    return PlanetData(
        0, type_name, surface,
        orbit, atmosphere, temperature, weather, tectonics, mass, radius, gravity, day, tilt,
        fuel_use, minerals, lifeforms,
        moons, direction, initial_angle
    )


def main():
    # Mineral types
    with open('raw_minerals.txt') as r:
        lines = r.readlines()
        for line in lines:
            line = line.rstrip()
            if line:
                parts = line.split('\t')
                name = parts[0]
                category = parts[1].split('.png ')[1]
                density = int(parts[3])
                mineral_types[name] = MineralType(name, category, mineral_value_map[category], density)

    # Lifeform types
    with open('raw_lifeforms.txt') as r:
        lines = r.readlines()
        for line in lines:
            line = line.rstrip()
            if line:
                parts = line.split('\t')
                name = parts[0]
                behaviour = lifeform_behaviour_map[parts[2]]
                intelligence = lifeform_intelligence_map[parts[3]]
                value = int(parts[4])
                health = int(parts[5])
                speed = lifeform_speed_map[parts[6]]
                danger = lifeform_danger_map[parts[7]]
                lifeform_types.append(LifeformType(name, behaviour, intelligence, value, health, speed, danger))

    # Planet types
    with open('raw_planets.txt') as r:
        lines = r.readlines()
        for line in lines:
            line = line.rstrip()
            if line:
                parts = line.split('\t')
                name = parts[0]
                size, surface = parts[1].split(', ')
                size, surface = planet_size_map[size], planet_surface_map[surface]
                color = planet_color_map[parts[2]]
                tectonics = planet_tectonics_map[parts[3]]
                density, weather = parts[4].split(', ')
                density, weather = planet_density_map[density], planet_weather_map[weather]
                minerals = parse_planet_minerals(parts[5])
                planet_types.append(PlanetType(name, size, surface, color, tectonics, density, weather, minerals))

    # Systems
    with open('raw_stars.txt') as r, open('systems.txt', 'w') as w:
        lines = r.readlines()
        for line in lines:
            line = line.rstrip()
            if line:
                parts = line.split('\t')
                color, size = parts[2], parts[3]
                if color and size:
                    coords = parts[4].split(' : ')
                    if len(coords) == 2:
                        # Star
                        star_name = (parts[1] + ' ' + parts[0]).lstrip()
                        star_x, star_y = coords
                        star_color = get_star_color(color)
                        star_temperature = random.uniform(*star_temperature_map[star_color])
                        star_size = star_size_map[size]
                        star_radius = random.uniform(*star_radius_map[star_size])
                        star_luminosity = get_star_luminosity(star_temperature, star_radius)
                        star_mass = get_star_mass(star_luminosity)
                        system_rotation = 1 if random.getrandbits(1) else -1

                        # Planets
                        planets = []
                        planet_probability = system_planet_chance_map[star_size]
                        for i in range(system_planet_max_count_map[star_size]):
                            if random.random() < planet_probability:
                                planets.append(
                                    get_planet(False, i, star_size, star_radius, star_luminosity, system_rotation)
                                )

                        for i, planet in enumerate(planets):
                            planet.number = i + 1
                            for j, moon in enumerate(planet.moons):
                                moon.number = j + 1

                        planets = '||'.join([planet_str(p, False) for p in planets])

                        w.write(f'{star_name}&&{star_x}&&{star_y}&&'
                                f'{star_color}&&{star_temperature}&&{star_size}&&{star_radius}&&{star_luminosity}&&'
                                f'{star_mass}&&{planets}\n')

    # Ships
    with open('raw_ships.txt') as r, open('ships.txt', 'w') as w:
        lines = r.readlines()
        for line in lines:
            line = line.rstrip()
            if line:
                parts = line.split(';;')
                name = parts[0]
                crew = '??'.join(parts[1].split(','))
                battery = float(parts[2])
                battery_regen = 24.0 * float(parts[3]) / (1.0 + float(parts[4]))
                mass = 28080.0 * float(parts[5])
                max_vel = 24.0 * float(parts[6])
                max_ang_vel = 9.425 / (1.0 + float(parts[7]))

                im = Image.open(f'raw_ships/{name}-big-000.png')
                pix: typing.Any = im.load()

                width, height = im.size
                cx, cy = width / 2, height / 2

                area, moi = 0.0, 0.0
                for x in range(width):
                    for y in range(height):
                        da = 0.0100392157 * pix[x, y][3]
                        area += da
                        dx, dy = 0.5 + x - cx, 0.5 + y - cy
                        moi += da * (dx * dx + dy * dy + 0.16666666666666666)

                density = mass / area
                moi *= density

                sqrt_area = math.sqrt(area)
                thrust = 0.0 * sqrt_area * max_vel + 0.1 * area * max_vel * max_vel
                area_3_2 = area * sqrt_area
                ang_thrust = 0.0 * area_3_2 * max_ang_vel + 0.04 * area * area_3_2 * max_ang_vel * max_ang_vel

                w.write(f'{name.title()}&&{crew}&&{mass}&&{moi}&&{area}&&{thrust}&&{ang_thrust}&&'
                        f'{battery}&&{battery_regen}\n')


if __name__ == '__main__':
    main()
