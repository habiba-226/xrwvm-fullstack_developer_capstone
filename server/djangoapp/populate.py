from .models import CarMake, CarModel


def initiate():
    # Car Make Data
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        # Use get_or_create to avoid duplicates
        car_make, created = CarMake.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        car_make_instances.append(car_make)

    # Car Model Data
    car_model_data = [
        {
            "name": "Pathfinder",
            "type": "SUV",
            "year": 2023,
            "make": car_make_instances[0],
            "dealer_id": 1
        },
        {
            "name": "Qashqai",
            "type": "SUV",
            "year": 2023,
            "make": car_make_instances[0],
            "dealer_id": 1
        },
        {
            "name": "XTRAIL",
            "type": "SUV",
            "year": 2023,
            "make": car_make_instances[0],
            "dealer_id": 1
        },
        {
            "name": "A-Class",
            "type": "HATCHBACK",
            "year": 2023,
            "make": car_make_instances[1],
            "dealer_id": 1
        },
        {
            "name": "C-Class",
            "type": "SEDAN",
            "year": 2023,
            "make": car_make_instances[1],
            "dealer_id": 1
        },
        {
            "name": "E-Class",
            "type": "SEDAN",
            "year": 2023,
            "make": car_make_instances[1],
            "dealer_id": 1
        },
        {
            "name": "A4",
            "type": "SEDAN",
            "year": 2023,
            "make": car_make_instances[2],
            "dealer_id": 1
        },
        {
            "name": "A5",
            "type": "SEDAN",
            "year": 2023,
            "make": car_make_instances[2],
            "dealer_id": 1
        },
        {
            "name": "A6",
            "type": "SEDAN",
            "year": 2023,
            "make": car_make_instances[2],
            "dealer_id": 1
        },
        {
            "name": "Sorrento",
            "type": "SUV",
            "year": 2023,
            "make": car_make_instances[3],  # Assuming Kia for the Sorrento
            "dealer_id": 1
        }
    ]

    # Create CarModel instances
    for data in car_model_data:
        # Use get_or_create to avoid duplicates
        car_model, created = CarModel.objects.get_or_create(
            name=data['name'],
            defaults={
                'type': data['type'],
                'year': data['year'],
                'make': data['make'],
                'dealer_id': data['dealer_id']
            }
        )
