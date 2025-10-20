sample_products = [
    {'id': '1', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 50,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '2', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 55, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '3', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 60, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '4', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 65,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '5', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 70,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '6', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 75,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '7', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 80,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '8', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 85, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '9', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 90, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '10', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 95, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '11', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 100,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '12', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 105, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '13', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 110, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '14', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 115,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '15', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 120,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '16', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 125,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '17', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 130,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '18', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 135, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '19', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 140, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '20', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 145, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '21', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 150,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '22', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 155, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '23', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 160, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '24', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 165,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '25', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 170,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '26', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 175,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '27', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 180,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '28', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 185, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '29', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 190, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '30', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 195, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '31', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 200,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '32', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 205, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '33', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 210, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '34', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 215,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '35', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 220,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '36', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 225,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '37', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 230,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '38', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 235, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '39', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 240, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '40', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 245, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '41', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 250,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '42', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 255, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '43', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 260, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '44', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 265,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '45', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 270,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '46', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 275,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '47', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 280,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '48', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 285, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '49', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 290, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '50', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 295, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '51', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 300,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '52', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 305, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '53', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 310, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '54', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 315,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '55', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 320,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '56', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 325,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '57', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 330,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '58', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 335, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '59', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 340, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '60', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 345, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '61', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 350,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '62', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 355, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '63', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 360, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '64', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 365,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '65', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 370,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '66', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 375,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '67', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 380,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '68', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 385, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '69', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 390, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '70', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 395, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '71', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 400,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '72', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 405, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '73', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 410, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '74', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 415,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '75', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 420,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '76', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 425,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '77', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 430,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '78', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 435, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '79', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 440, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '80', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 445, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '81', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 450,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '82', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 455, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '83', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 460, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '84', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 465,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '85', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 470,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '86', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 475,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '87', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 480,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '88', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 485, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '89', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 490, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '90', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 495, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '91', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 500,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '92', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 505, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '93', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 510, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '94', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 515,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '95', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 520,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '96', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 525,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '97', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 530,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '98', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 535, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '99', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 540, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '100', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 545, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '101', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 50,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '102', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 55, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '103', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 60, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '104', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 65,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '105', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 70,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '106', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 75,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '107', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 80,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '108', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 85, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '109', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 90, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '110', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 95, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '111', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 100,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '112', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 105, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '113', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 110, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '114', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 115,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '115', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 120,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '116', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 125,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '117', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 130,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '118', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 135, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '119', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 140, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '120', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 145, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '121', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 150,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '122', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 155, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '123', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 160, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '124', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 165,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '125', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 170,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '126', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 175,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '127', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 180,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '128', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 185, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '129', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 190, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '130', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 195, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '131', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 200,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '132', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 205, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '133', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 210, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '134', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 215,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '135', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 220,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '136', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 225,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '137', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 230,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '138', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 235, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '139', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 240, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '140', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 245, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '141', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 250,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '142', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 255, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '143', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 260, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '144', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 265,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '145', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 270,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '146', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 275,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '147', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 280,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '148', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 285, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '149', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 290, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '150', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 295, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '151', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 300,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '152', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 305, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '153', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 310, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '154', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 315,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '155', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 320,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '156', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 325,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '157', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 330,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '158', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 335, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '159', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 340, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '160', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 345, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '161', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 350,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '162', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 355, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '163', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 360, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '164', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 365,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '165', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 370,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '166', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 375,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '167', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 380,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '168', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 385, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '169', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 390, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '170', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 395, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '171', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 400,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '172', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 405, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '173', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 410, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '174', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 415,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '175', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 420,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '176', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 425,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '177', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 430,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '178', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 435, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '179', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 440, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '180', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 445, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '181', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 450,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '2.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '182', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 455, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '183', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 460, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3600MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '184', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 465,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '500GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '185', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 470,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '186', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 475,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '3440x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '187', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 480,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '188', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 485, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '189', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 490, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '190', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 495, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '191', 'name': 'Intel Core i9 Processor', 'description': 'High-performance processor', 'brand': 'Intel', 'category': 'Processor', 'price': 500,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '4'}, {'name': 'clock_speed', 'value': '3.0 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '192', 'name': 'AMD Ryzen 7 Processor', 'description': 'Powerful multitasking processor', 'brand': 'AMD', 'category': 'Processor', 'price': 505, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'cores', 'value': '5'}, {'name': 'clock_speed', 'value': '3.5 GHz'}, {'name': 'generation', 'value': '11th Gen'}]},
    {'id': '193', 'name': 'Corsair Vengeance 16GB DDR4 Memory', 'description': 'Reliable DDR4 RAM', 'brand': 'Corsair', 'category': 'Memory', 'price': 510, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2400MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '194', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'High-speed SSD', 'brand': 'Samsung', 'category': 'Storage', 'price': 515,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '1000GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '195', 'name': 'Western Digital 2TB HDD HDD', 'description': 'High-capacity hard drive', 'brand': 'Western Digital', 'category': 'Storage', 'price': 520,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'capacity', 'value': '2000GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '196', 'name': 'Dell UltraSharp 24-inch Monitor', 'description': 'Full HD monitor', 'brand': 'Dell', 'category': 'Monitor', 'price': 525,
        'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '197', 'name': 'LG UltraWide 34-inch Monitor', 'description': 'UltraWide monitor for productivity', 'brand': 'LG', 'category': 'Monitor', 'price': 530,
        'tags': ['electronics', 'computer', 'productivity'], 'attributes': [{'name': 'resolution', 'value': '2560x1080'}, {'name': 'refresh_rate', 'value': '75Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '198', 'name': 'Logitech G Pro Mechanical Keyboard', 'description': 'Mechanical keyboard with RGB', 'brand': 'Logitech', 'category': 'Keyboard', 'price': 535, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '199', 'name': 'Razer DeathAdder Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'Razer', 'category': 'Mouse', 'price': 540, 'tags': [
        'electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '20000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '200', 'name': 'HyperX Cloud II Headset', 'description': 'Gaming headset with surround sound', 'brand': 'HyperX', 'category': 'Headset', 'price': 545, 'tags': [
        'electronics', 'computer', 'productivity'], 'attributes': [{'name': 'connection', 'value': 'Wired'}, {'name': 'surround_sound', 'value': '7.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '201', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 75,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'cores', 'value': '8'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '12th Gen'}]},
    {'id': '202', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 82,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '9'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '13th Gen'}]},
    {'id': '203', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 89,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '204', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 96,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '205', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 103, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '206', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 110,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '207', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 117,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '208', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 124, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '209', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 131, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'dpi', 'value': '12000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '210', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 138,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '211', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 145,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '18'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '14th Gen'}]},
    {'id': '212', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 152,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '19'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '15th Gen'}]},
    {'id': '213', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 159,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2666MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '214', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 166,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '215', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 173, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '216', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 180,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '217', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 187,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '218', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 194, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '219', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 201, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '18000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '220', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 208,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '221', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 215,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'cores', 'value': '16'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '12th Gen'}]},
    {'id': '222', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 222,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '17'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '13th Gen'}]},
    {'id': '223', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 229,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3000MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '224', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 236,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '225', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 243, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '226', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 250,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '227', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 257,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '228', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 264, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '229', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 271, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'dpi', 'value': '12000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '230', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 278,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '231', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 285,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '14'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '14th Gen'}]},
    {'id': '232', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 292,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '15'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '15th Gen'}]},
    {'id': '233', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 299,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '234', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 306,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '235', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 313, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '236', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 320,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '237', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 327,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '238', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 334, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '239', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 341, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '18000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '240', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 348,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '241', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 355,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'cores', 'value': '12'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '12th Gen'}]},
    {'id': '242', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 362,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '13'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '13th Gen'}]},
    {'id': '243', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 369,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '2666MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '244', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 376,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '245', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 383, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '246', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 390,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '247', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 397,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '248', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 404, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '249', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 411, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'dpi', 'value': '12000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '250', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 418,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '251', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 425,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '10'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '14th Gen'}]},
    {'id': '252', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 432,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '11'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '15th Gen'}]},
    {'id': '253', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 439,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3000MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '254', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 446,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '255', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 453, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '256', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 460,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '257', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 467,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '258', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 474, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '259', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 481, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '18000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '260', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 488,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '261', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 495,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'cores', 'value': '8'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '12th Gen'}]},
    {'id': '262', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 502,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '9'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '13th Gen'}]},
    {'id': '263', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 509,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '264', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 516,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '265', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 523, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '266', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 530,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '267', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 537,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '268', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 544, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '269', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 551, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'dpi', 'value': '12000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '270', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 558,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '271', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 565,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '18'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '14th Gen'}]},
    {'id': '272', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 572,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '19'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '15th Gen'}]},
    {'id': '273', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 579,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '2666MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '274', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 586,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '275', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 593, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '276', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 600,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '277', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 607,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '278', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 614, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '279', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 621, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '18000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '280', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 628,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '281', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 635,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'cores', 'value': '16'}, {'name': 'clock_speed', 'value': '3.3 GHz'}, {'name': 'generation', 'value': '12th Gen'}]},
    {'id': '282', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 642,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '17'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '13th Gen'}]},
    {'id': '283', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 649,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '64GB'}, {'name': 'speed', 'value': '3000MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '284', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 656,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '2048GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '285', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 663, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '286', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 670,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'VA'}]},
    {'id': '287', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 677,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '288', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 684, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '289', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 691, 'tags': [
        'computer', 'electronics', 'premium'], 'attributes': [{'name': 'dpi', 'value': '12000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '290', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 698,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '291', 'name': 'Intel Xeon Processor', 'description': 'Server-grade processor', 'brand': 'Intel', 'category': 'Processor', 'price': 705,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '14'}, {'name': 'clock_speed', 'value': '2.5 GHz'}, {'name': 'generation', 'value': '14th Gen'}]},
    {'id': '292', 'name': 'AMD Threadripper Processor', 'description': 'High-performance workstation processor', 'brand': 'AMD', 'category': 'Processor', 'price': 712,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'cores', 'value': '15'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '15th Gen'}]},
    {'id': '293', 'name': 'G.SKILL Ripjaws 16GB DDR4 Memory', 'description': 'High-speed DDR4 RAM', 'brand': 'G.SKILL', 'category': 'Memory', 'price': 719,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '294', 'name': 'Crucial P5 Plus 1TB SSD', 'description': 'High-speed NVMe SSD', 'brand': 'Crucial', 'category': 'Storage', 'price': 726,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '512GB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': '2.5 inch'}]},
    {'id': '295', 'name': 'Seagate Barracuda 2TB HDD HDD', 'description': 'Reliable hard drive', 'brand': 'Seagate', 'category': 'Storage', 'price': 733, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'capacity', 'value': '1024GB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '296', 'name': 'Acer Predator 27-inch Monitor', 'description': '4K gaming monitor', 'brand': 'Acer', 'category': 'Monitor', 'price': 740,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '1920x1080'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'TN'}]},
    {'id': '297', 'name': 'ASUS TUF Gaming 32-inch Monitor', 'description': 'High refresh rate gaming monitor', 'brand': 'ASUS', 'category': 'Monitor', 'price': 747,
        'tags': ['computer', 'electronics', 'premium'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '298', 'name': 'Razer BlackWidow Mechanical Keyboard', 'description': 'RGB mechanical keyboard', 'brand': 'Razer', 'category': 'Keyboard', 'price': 754, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Membrane'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '299', 'name': 'SteelSeries Rival Mouse', 'description': 'Ergonomic gaming mouse', 'brand': 'SteelSeries', 'category': 'Mouse', 'price': 761, 'tags': [
        'computer', 'electronics', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '18000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '300', 'name': 'Sony WH-1000XM4 Headset', 'description': 'Noise-cancelling headset', 'brand': 'Sony', 'category': 'Headset', 'price': 768,
        'tags': ['computer', 'electronics', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'surround_sound', 'value': '5.1'}, {'name': 'microphone', 'value': 'Yes'}]},

     {'id': '1', 'name': 'Intel Core i5-10400 Processor', 'description': 'Hexa-core processor for balanced performance', 'brand': 'Intel', 'category': 'Processor', 'price': 150, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'cores', 'value': '6'}, {'name': 'clock_speed', 'value': '2.9 GHz'}, {'name': 'generation', 'value': '10th Gen'}]},
    {'id': '2', 'name': 'AMD Ryzen 5 5600X Processor', 'description': 'Six-core processor with high gaming performance', 'brand': 'AMD', 'category': 'Processor', 'price': 210, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'cores', 'value': '6'}, {'name': 'clock_speed', 'value': '3.7 GHz'}, {'name': 'generation', 'value': '5000 Series'}]},
    {'id': '3', 'name': 'Corsair Vengeance LPX 16GB DDR4 RAM', 'description': 'High-speed memory for gaming and multitasking', 'brand': 'Corsair', 'category': 'Memory', 'price': 80, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'capacity', 'value': '16GB'}, {'name': 'speed', 'value': '3200MHz'}, {'name': 'type', 'value': 'DDR4'}]},
    {'id': '4', 'name': 'Samsung 970 EVO 1TB SSD', 'description': 'Reliable NVMe SSD with high read/write speeds', 'brand': 'Samsung', 'category': 'Storage', 'price': 140, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'capacity', 'value': '1TB'}, {'name': 'interface', 'value': 'NVMe'}, {'name': 'form_factor', 'value': 'M.2'}]},
    {'id': '5', 'name': 'Seagate Barracuda 2TB HDD', 'description': 'High-capacity hard drive for data storage', 'brand': 'Seagate', 'category': 'Storage', 'price': 60, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'capacity', 'value': '2TB'}, {'name': 'interface', 'value': 'SATA'}, {'name': 'form_factor', 'value': '3.5 inch'}]},
    {'id': '6', 'name': 'MSI MAG B550 TOMAHAWK Motherboard', 'description': 'Motherboard with PCIe 4.0 support for Ryzen CPUs', 'brand': 'MSI', 'category': 'Motherboard', 'price': 160, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'socket', 'value': 'AM4'}, {'name': 'chipset', 'value': 'B550'}, {'name': 'form_factor', 'value': 'ATX'}]},
    {'id': '7', 'name': 'Asus ROG Strix X570-E Gaming Motherboard', 'description': 'Premium motherboard with advanced gaming features', 'brand': 'Asus', 'category': 'Motherboard', 'price': 300, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'socket', 'value': 'AM4'}, {'name': 'chipset', 'value': 'X570'}, {'name': 'form_factor', 'value': 'ATX'}]},
    {'id': '8', 'name': 'Gigabyte GeForce GTX 1660 Super GPU', 'description': 'Graphics card with great 1080p gaming performance', 'brand': 'Gigabyte', 'category': 'Graphics Card', 'price': 230, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'memory', 'value': '6GB GDDR6'}, {'name': 'boost_clock', 'value': '1830 MHz'}, {'name': 'interface', 'value': 'PCIe 3.0'}]},
    {'id': '9', 'name': 'NVIDIA GeForce RTX 3070 GPU', 'description': 'High-performance graphics card for 4K gaming', 'brand': 'NVIDIA', 'category': 'Graphics Card', 'price': 500, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'memory', 'value': '8GB GDDR6'}, {'name': 'boost_clock', 'value': '1725 MHz'}, {'name': 'interface', 'value': 'PCIe 4.0'}]},
    {'id': '10', 'name': 'Logitech G502 HERO Gaming Mouse', 'description': 'Gaming mouse with customizable buttons and RGB', 'brand': 'Logitech', 'category': 'Mouse', 'price': 50, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'dpi', 'value': '16000'}, {'name': 'connection', 'value': 'Wired'}, {'name': 'sensor', 'value': 'Optical'}]},
    {'id': '11', 'name': 'SteelSeries Arctis 7 Wireless Gaming Headset', 'description': 'Wireless headset with surround sound for gaming', 'brand': 'SteelSeries', 'category': 'Headset', 'price': 120, 'tags': ['electronics', 'audio', 'gaming'], 'attributes': [{'name': 'connection', 'value': 'Wireless'}, {'name': 'noise_cancellation', 'value': 'Passive'}, {'name': 'microphone', 'value': 'Yes'}]},
    {'id': '12', 'name': 'Razer BlackWidow Elite Mechanical Keyboard', 'description': 'RGB mechanical keyboard with tactile feedback', 'brand': 'Razer', 'category': 'Keyboard', 'price': 100, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'switch_type', 'value': 'Green Switch'}, {'name': 'backlight', 'value': 'RGB'}, {'name': 'connection', 'value': 'Wired'}]},
    {'id': '13', 'name': 'Dell U2720Q 27-inch 4K Monitor', 'description': 'UltraSharp 4K monitor for professional use', 'brand': 'Dell', 'category': 'Monitor', 'price': 500, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'resolution', 'value': '3840x2160'}, {'name': 'refresh_rate', 'value': '60Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '14', 'name': 'BenQ EX2780Q 27-inch QHD Monitor', 'description': 'Gaming monitor with HDR support and high refresh rate', 'brand': 'BenQ', 'category': 'Monitor', 'price': 300, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '2560x1440'}, {'name': 'refresh_rate', 'value': '144Hz'}, {'name': 'panel_type', 'value': 'IPS'}]},
    {'id': '15', 'name': 'Apple MacBook Pro 13-inch (M1)', 'description': 'Powerful laptop with Apple Silicon M1 chip', 'brand': 'Apple', 'category': 'Laptop', 'price': 1300, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'processor', 'value': 'Apple M1'}, {'name': 'memory', 'value': '8GB'}, {'name': 'storage', 'value': '256GB SSD'}]},
    {'id': '16', 'name': 'Microsoft Surface Laptop 4', 'description': 'Thin, stylish laptop with great battery life', 'brand': 'Microsoft', 'category': 'Laptop', 'price': 1000, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'processor', 'value': 'Intel Core i5'}, {'name': 'memory', 'value': '8GB'}, {'name': 'storage', 'value': '512GB SSD'}]},
    {'id': '17', 'name': 'ASUS ZenBook 14 Ultra-Slim Laptop', 'description': 'Compact laptop with high performance', 'brand': 'ASUS', 'category': 'Laptop', 'price': 800, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'processor', 'value': 'AMD Ryzen 5'}, {'name': 'memory', 'value': '8GB'}, {'name': 'storage', 'value': '256GB SSD'}]},
    {'id': '18', 'name': 'HP Pavilion 15 Laptop', 'description': 'Affordable laptop for daily use and light multitasking', 'brand': 'HP', 'category': 'Laptop', 'price': 650, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'processor', 'value': 'Intel Core i3'}, {'name': 'memory', 'value': '8GB'}, {'name': 'storage', 'value': '256GB SSD'}]},
    {'id': '19', 'name': 'Lenovo IdeaPad 3 14-inch Laptop', 'description': 'Budget-friendly laptop with solid performance', 'brand': 'Lenovo', 'category': 'Laptop', 'price': 450, 'tags': ['electronics', 'computer'], 'attributes': [{'name': 'processor', 'value': 'Intel Core i5'}, {'name': 'memory', 'value': '8GB'}, {'name': 'storage', 'value': '1TB HDD'}]},
    {'id': '20', 'name': 'Samsung Odyssey G9 Gaming Monitor', 'description': 'Ultra-wide curved monitor for immersive gaming', 'brand': 'Samsung', 'category': 'Monitor', 'price': 1500, 'tags': ['electronics', 'computer', 'gaming'], 'attributes': [{'name': 'resolution', 'value': '5120x1440'}, {'name': 'refresh_rate', 'value': '240Hz'}, {'name': 'panel_type', 'value': 'QLED'}]},

    
]
