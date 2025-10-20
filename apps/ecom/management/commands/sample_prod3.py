sample_products = [
    # Processors
    {
        'id': 'INTL001',
        'name': 'Intel Core i9-13900K',
        'description': 'Flagship desktop processor with exceptional multi-threaded performance',
        'brand': 'Intel',
        'category': 'Components',
        'subcategory': 'Processors',
        'price': 589.99,
        'tags': ['desktop', 'gaming', 'high-end', 'overclockable'],
        'attributes': [
            {'name': 'cores', 'value': '24 (8P + 16E)'},
            {'name': 'threads', 'value': '32'},
            {'name': 'base_clock', 'value': '3.0 GHz'},
            {'name': 'boost_clock', 'value': '5.8 GHz'},
            {'name': 'cache', 'value': '36MB L3'},
            {'name': 'tdp', 'value': '125W'},
            {'name': 'socket', 'value': 'LGA 1700'},
            {'name': 'generation', 'value': '13th Gen'}
        ]
    },
    {
        'id': 'AMD001',
        'name': 'AMD Ryzen 9 7950X',
        'description': 'High-performance desktop processor with Zen 4 architecture',
        'brand': 'AMD',
        'category': 'Components',
        'subcategory': 'Processors',
        'price': 549.99,
        'tags': ['desktop', 'gaming', 'high-end', 'overclockable'],
        'attributes': [
            {'name': 'cores', 'value': '16'},
            {'name': 'threads', 'value': '32'},
            {'name': 'base_clock', 'value': '4.5 GHz'},
            {'name': 'boost_clock', 'value': '5.7 GHz'},
            {'name': 'cache', 'value': '64MB L3'},
            {'name': 'tdp', 'value': '170W'},
            {'name': 'socket', 'value': 'AM5'},
            {'name': 'generation', 'value': 'Zen 4'}
        ]
    },
    
    # Graphics Cards
    {
        'id': 'NVID001',
        'name': 'NVIDIA GeForce RTX 4090',
        'description': 'Flagship graphics card with DLSS 3.0 and ray tracing capabilities',
        'brand': 'NVIDIA',
        'category': 'Components',
        'subcategory': 'Graphics Cards',
        'price': 1599.99,
        'tags': ['gaming', 'high-end', '4K', 'ray-tracing'],
        'attributes': [
            {'name': 'memory', 'value': '24GB GDDR6X'},
            {'name': 'memory_speed', 'value': '21 Gbps'},
            {'name': 'cuda_cores', 'value': '16384'},
            {'name': 'boost_clock', 'value': '2.52 GHz'},
            {'name': 'tdp', 'value': '450W'},
            {'name': 'power_connector', 'value': '16-pin'}
        ]
    },
    {
        'id': 'AMD002',
        'name': 'AMD Radeon RX 7900 XTX',
        'description': 'High-performance graphics card with FSR 3.0 technology',
        'brand': 'AMD',
        'category': 'Components',
        'subcategory': 'Graphics Cards',
        'price': 999.99,
        'tags': ['gaming', 'high-end', '4K'],
        'attributes': [
            {'name': 'memory', 'value': '24GB GDDR6'},
            {'name': 'memory_speed', 'value': '20 Gbps'},
            {'name': 'stream_processors', 'value': '6144'},
            {'name': 'boost_clock', 'value': '2.5 GHz'},
            {'name': 'tdp', 'value': '355W'},
            {'name': 'power_connector', 'value': '8-pin x2'}
        ]
    },

    # Motherboards
    {
        'id': 'ASUS001',
        'name': 'ASUS ROG Maximus Z790 Hero',
        'description': 'Premium Intel Z790 motherboard with extensive features',
        'brand': 'ASUS',
        'category': 'Components',
        'subcategory': 'Motherboards',
        'price': 629.99,
        'tags': ['gaming', 'high-end', 'overclocking'],
        'attributes': [
            {'name': 'socket', 'value': 'LGA 1700'},
            {'name': 'chipset', 'value': 'Intel Z790'},
            {'name': 'form_factor', 'value': 'ATX'},
            {'name': 'memory_slots', 'value': '4'},
            {'name': 'max_memory', 'value': '128GB'},
            {'name': 'pcie_slots', 'value': '3'}
        ]
    },
    
    # Memory (RAM)
    {
        'id': 'GSKL001',
        'name': 'G.SKILL Trident Z5 RGB',
        'description': 'High-performance DDR5 RAM with RGB lighting',
        'brand': 'G.SKILL',
        'category': 'Components',
        'subcategory': 'Memory',
        'price': 189.99,
        'tags': ['gaming', 'high-speed', 'RGB'],
        'attributes': [
            {'name': 'capacity', 'value': '32GB (2x16GB)'},
            {'name': 'speed', 'value': 'DDR5-6000'},
            {'name': 'timing', 'value': 'CL36'},
            {'name': 'voltage', 'value': '1.35V'}
        ]
    },

    # Storage
    {
        'id': 'SMSN001',
        'name': 'Samsung 990 PRO',
        'description': 'High-performance PCIe 4.0 NVMe SSD',
        'brand': 'Samsung',
        'category': 'Components',
        'subcategory': 'Storage',
        'price': 169.99,
        'tags': ['storage', 'high-speed', 'NVMe'],
        'attributes': [
            {'name': 'capacity', 'value': '2TB'},
            {'name': 'interface', 'value': 'PCIe 4.0 x4'},
            {'name': 'form_factor', 'value': 'M.2 2280'},
            {'name': 'sequential_read', 'value': '7,450 MB/s'},
            {'name': 'sequential_write', 'value': '6,900 MB/s'}
        ]
    },

    # Power Supplies
    {
        'id': 'CORS001',
        'name': 'Corsair HX1000i',
        'description': 'Fully modular 80 PLUS Platinum power supply',
        'brand': 'Corsair',
        'category': 'Components',
        'subcategory': 'Power Supplies',
        'price': 259.99,
        'tags': ['power-supply', 'modular', 'high-efficiency'],
        'attributes': [
            {'name': 'wattage', 'value': '1000W'},
            {'name': 'efficiency', 'value': '80 PLUS Platinum'},
            {'name': 'modularity', 'value': 'Fully Modular'},
            {'name': 'fan_size', 'value': '140mm'}
        ]
    },

    # Cases
    {
        'id': 'LIAN001',
        'name': 'Lian Li O11 Dynamic EVO',
        'description': 'Premium mid-tower case with excellent airflow',
        'brand': 'Lian Li',
        'category': 'Components',
        'subcategory': 'Cases',
        'price': 169.99,
        'tags': ['case', 'mid-tower', 'premium'],
        'attributes': [
            {'name': 'form_factor', 'value': 'Mid Tower'},
            {'name': 'motherboard_support', 'value': 'E-ATX, ATX, Micro-ATX, Mini-ITX'},
            {'name': 'dimensions', 'value': '465mm x 285mm x 459mm'},
            {'name': 'max_gpu_length', 'value': '420mm'}
        ]
    },

    # Monitors
    {
        'id': 'LGEL001',
        'name': 'LG 27GP950-B',
        'description': '27-inch 4K gaming monitor with HDMI 2.1',
        'brand': 'LG',
        'category': 'Peripherals',
        'subcategory': 'Monitors',
        'price': 799.99,
        'tags': ['gaming', '4K', 'HDR'],
        'attributes': [
            {'name': 'size', 'value': '27"'},
            {'name': 'resolution', 'value': '3840x2160'},
            {'name': 'refresh_rate', 'value': '160Hz'},
            {'name': 'panel_type', 'value': 'Nano IPS'},
            {'name': 'response_time', 'value': '1ms GtG'}
        ]
    },

    # Keyboards
    {
        'id': 'WOOT001',
        'name': 'Wooting 60HE',
        'description': 'Analog mechanical keyboard with Hall effect switches',
        'brand': 'Wooting',
        'category': 'Peripherals',
        'subcategory': 'Keyboards',
        'price': 199.99,
        'tags': ['gaming', 'mechanical', 'analog'],
        'attributes': [
            {'name': 'form_factor', 'value': '60%'},
            {'name': 'switch_type', 'value': 'Lekker (Hall Effect)'},
            {'name': 'connection', 'value': 'USB-C'},
            {'name': 'backlight', 'value': 'RGB'}
        ]
    },

    # Mouse
    {
        'id': 'LOGC001',
        'name': 'Logitech G Pro X Superlight',
        'description': 'Ultra-lightweight wireless gaming mouse',
        'brand': 'Logitech',
        'category': 'Peripherals',
        'subcategory': 'Mice',
        'price': 159.99,
        'tags': ['gaming', 'wireless', 'lightweight'],
        'attributes': [
            {'name': 'sensor', 'value': 'HERO 25K'},
            {'name': 'weight', 'value': '63g'},
            {'name': 'battery_life', 'value': '70 hours'},
            {'name': 'connection', 'value': 'Wireless'},
            {'name': 'dpi', 'value': '25600'}
        ]
    }
]