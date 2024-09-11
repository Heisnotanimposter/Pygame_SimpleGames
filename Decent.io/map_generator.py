import random
import noise  # Perlin noise library

def generate_map(width=50, height=30, use_perlin=True):
    map_data = []
    scale = 10.0  # Scale of the noise
    octaves = 4  # Number of levels of detail
    persistence = 0.5  # Amplitude of octaves
    lacunarity = 2.0  # Frequency of octaves
    seed = random.randint(0, 100)

    for y in range(height):
        row = []
        for x in range(width):
            if use_perlin:
                # Generate Perlin noise value for each tile
                noise_val = noise.pnoise2(x / scale, y / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed)
                if noise_val < -0.2:
                    tile_type = "water"
                elif noise_val < 0.0:
                    tile_type = "grass"
                elif noise_val < 0.2:
                    tile_type = "forest"
                else:
                    tile_type = "mountain"
            else:
                # Simple random terrain generation
                tile_type = random.choice(["grass", "water", "mountain"])
            row.append(tile_type)
        map_data.append(row)

    return map_data
