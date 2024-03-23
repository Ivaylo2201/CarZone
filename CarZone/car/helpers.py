def get_manufacturer(brand: str) -> str | None:
    manufacturers: dict = {
        'audi': 'Volkswagen',
        'vw': 'Volkswagen',
        'seat': 'Volkswagen',
        'lamborghini': 'Volkswagen',
        'porsche': 'Volkswagen',
        'toyota': 'Toyota',
        'fiat': 'Fiat',
        'bmw': 'BMW',
        'mercedes-benz': 'Mercedes-Benz',
        'nissan': 'Nissan',
        'hyundai': 'Hyundai',
        'kia': 'Hyundai',
        'volvo': 'Volvo',
        'mazda': 'Mazda',
        'renault': 'Renault',
        'peugeot': 'Peugeot',
        'citroen': 'Citroen',
        'maserati': 'Maserati',
        'ferrari': 'Ferrari'
    }

    try:
        return manufacturers[brand]
    except (KeyError):
        return None
