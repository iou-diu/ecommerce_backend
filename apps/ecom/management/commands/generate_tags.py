from django.core.management.base import BaseCommand
from apps.ecom.models import Tag  # Adjust the import based on your app structure

class Command(BaseCommand):
    help = 'Populate the database with common eCommerce tags related to computer products'

    def handle(self, *args, **kwargs):
        # List of tags
        tags_list = [
            'laptop', 'gaming laptop', 'business laptop', 'ultrabook', '2-in-1 laptop', 'notebook', 'desktop pc', 
            'all-in-one pc', 'mini pc', 'workstation', 'gaming desktop', 'processor', 'intel processor', 'amd processor', 
            'motherboard', 'intel motherboard', 'amd motherboard', 'gpu', 'graphics card', 'nvidia graphics card', 
            'amd graphics card', 'ram', 'ddr4 ram', 'ddr5 ram', 'ssd', 'nvme ssd', 'sata ssd', 'hdd', 'hard drive', 
            'external hard drive', 'usb drive', 'flash drive', 'power supply', 'psu', 'computer case', 'mid-tower case', 
            'full-tower case', 'mini-tower case', 'liquid cooling', 'air cooling', 'cpu cooler', 'thermal paste', 'pc fans', 
            'gaming mouse', 'gaming keyboard', 'mechanical keyboard', 'membrane keyboard', 'gaming chair', 'monitor', 
            'gaming monitor', 'curved monitor', 'ultrawide monitor', '4k monitor', '1080p monitor', '1440p monitor', 
            'mouse pad', 'headphones', 'gaming headset', 'wireless headset', 'webcam', 'microphone', 'external sound card', 
            'sound bar', 'speakers', 'networking', 'router', 'wifi router', 'ethernet switch', 'network cable', 'patch cable', 
            'fiber optic cable', 'adapter', 'usb hub', 'usb-c hub', 'external dvd drive', 'bluetooth adapter', 'laptop stand', 
            'monitor stand', 'cable management', 'printer', 'laser printer', 'inkjet printer', 'scanner', 'projector', 'ups', 
            'surge protector', 'battery backup', 'laptop battery', 'laptop charger', 'power bank', 'smartphone accessories', 
            'phone case', 'screen protector', 'phone charger', 'wireless charger', 'earbuds', 'true wireless earbuds', 
            'headphones', 'noise-cancelling headphones', 'tablet', 'android tablet', 'windows tablet', 'tablet case', 
            'tablet keyboard', 'smartwatch', 'wearable', 'fitness tracker', 'tv', 'smart tv', '4k tv', 'home theater', 
            'tv stand', 'vr headset', 'virtual reality', 'augmented reality', 'gaming console', 'playstation', 'xbox', 
            'nintendo switch', 'game controller', 'gaming accessories', 'gaming chair', 'gaming desk', 'game capture card', 
            'streaming equipment', 'streaming camera', 'green screen', 'tripod', 'lighting kit', 'portable storage', 
            'backup storage', 'nas', 'network-attached storage', 'server', 'rackmount server', 'tower server', 
            'server components', 'server ram', 'server hard drive', 'server ssd', 'cloud storage', 'software', 
            'operating system', 'windows 10', 'windows 11', 'antivirus', 'microsoft office', 'adobe creative cloud', 
            'autocad', 'photoshop', 'premiere pro', 'gaming laptop accessories', 'laptop cooling pad', 'docking station', 
            'external gpu', 'graphics card case', 'custom pc', 'custom pc build', 'pre-built pc', 'budget gaming pc', 
            'high-end gaming pc', 'esports pc', 'productivity pc', 'home office pc', 'graphic design pc', 'video editing pc', 
            'photo editing pc', 'streaming pc', 'software development pc', '3d rendering pc', 'cryptocurrency mining rig', 
            'mining gpu', 'crypto wallet', 'networking equipment', 'wireless access point', 'home automation', 'smart home', 
            'smart light', 'smart lock', 'smart thermostat', 'security camera', 'wireless security camera', 'doorbell camera', 
            'smart speaker', 'amazon echo', 'google nest', 'smart display', 'smart outlet', 'smart power strip', 
            'electric scooter', 'hoverboard', 'drone', 'drone camera', 'gaming monitor stand', 'vertical monitor stand', 
            'ergonomic accessories', 'laptop bag', 'backpack', 'camera accessories', 'dslr camera', 'mirrorless camera', 
            'camera lens', 'tripod mount', 'gopro accessories', 'action camera', '3d printer', 'filament', '3d printing pen', 
            'raspberry pi', 'arduino', 'microcontroller', 'electronics kits', 'robotics kits', 'vr accessories', 
            'smartphone gimbal', 'camera gimbal', 'portable hard drive', 'sd card', 'micro sd card', 'memory card reader', 
            'digital camera', 'dslr', 'mirrorless', 'prime lens', 'zoom lens', 'telephoto lens', 'fisheye lens', 'drone accessories', 
            'gopro mount', 'action camera mount', 'lens filters', 'camera batteries', 'battery charger', 'camera flash', 
            'photography lighting', 'gimbal stabilizer', 'lens cap', 'camera strap', 'smartphone tripod', 'camera bag', 
            'camera cleaning kit', 'wireless earbuds', 'bluetooth headset', 'portable speaker', 'smart glasses', 'dash cam', 
            'baby monitor', 'fitness watch', 'sports watch', 'heart rate monitor', 'blood pressure monitor', 'body fat scale', 
            'smart scale', 'robot vacuum', 'smart coffee maker', 'smart plug', 'smart bulb', 'smart refrigerator', 'smart oven', 
            'smart microwave', 'smart washer', 'smart dryer', 'robot lawn mower', 'smart irrigation system', 'solar panel kit', 
            'solar charger', 'power inverter', 'solar generator', 'portable power station', 'usb solar charger', 'car charger', 
            'portable fridge', 'camping fridge', 'car battery jump starter', 'car tire inflator', 'roof rack', 'car bike rack', 
            'car seat cover', 'car floor mat', 'car dash cover', 'headrest mount', 'phone car mount', 'laptop car mount', 
            'action camera for car', 'gaming mouse pad', 'gaming monitor arm', 'mechanical switch keyboard', 'rgb keyboard', 
            'keyboard wrist rest', 'gaming mouse bungee', 'wireless gaming mouse', 'gaming headset stand', 'gaming headset with mic', 
            'wired gaming headset', 'wireless game controller', 'ergonomic gaming chair', 'gaming footrest', 'gaming mat', 
            'gaming glasses', 'anti-glare monitor', 'curved ultrawide monitor', '240hz monitor', '165hz monitor', 'gaming desk mat', 
            'gaming projector', 'home theater projector', 'portable projector', 'led projector', 'pico projector', 
            'short throw projector', 'long throw projector', 'projector screen', 'projector ceiling mount', 'wireless hdmi adapter', 
            'tv wall mount', 'soundproofing foam', 'acoustic panels', 'wireless surround sound', 'bluetooth soundbar', 
            'surround sound speakers', 'soundproof curtains', 'soundproof door seal', 'noise-cancelling headset', 'studio microphone', 
            'audio mixer', 'sound mixer', 'studio monitor', 'usb microphone', 'wireless microphone', 'podcast equipment', 
            'voice recording equipment', 'karaoke system', 'dj equipment', 'turntable', 'vinyl record player', 'vinyl records', 
            'record cleaner', 'record shelf', 'home audio system', 'hi-fi audio', 'amp', 'subwoofer', 'guitar amplifier', 
            'bluetooth amplifier', 'home automation hub', 'z-wave hub', 'zigbee hub', 'smart home security system', 
            'window security sensor', 'door security sensor', 'smart thermostat', 'smart garage door opener', 'smart blinds', 
            'smart shades', 'solar security camera', '4k security camera', '1080p security camera', 'outdoor security camera', 
            'indoor security camera', 'poe camera', 'wireless nvr', 'wireless security system', 'video doorbell', 
            'smart door lock', 'smart intercom', 'voice assistant', 'robot mop', 'smart coffee grinder', 'robot pool cleaner', 
            'smart water leak detector', 'smart water shutoff', 'solar floodlight', 'solar pathway light', 'home automation light', 
            'smart home hub', 'ethernet over power', 'powerline adapter', 'network extender', 'wireless mesh system', 
            'gaming router', 'smart switch', 'smart dimmer', 'smart outlet', 'usb wall charger', 'power strip', 'ups battery', 
            'laptop sleeve', 'usb charging station', 'usb extension cable', 'wireless charging stand', 'usb-c charging cable', 
            'usb-c to hdmi adapter', 'usb-c dock', 'usb to ethernet adapter', 'thunderbolt 3 dock', 'thunderbolt 4 dock', 
            'usb-c power delivery', 'laptop docking station', 'usb sound card', 'gaming sound card', 'hdmi capture card', 
            'wireless display adapter', 'laptop privacy screen', 'laptop screen protector', 'keyboard cover', 'laptop cleaning kit', 
            'privacy filter', 'ssd enclosure', 'hdd docking station', 'portable ssd', 'internal ssd', 'external ssd', 'm.2 ssd', 
            'sata ssd', 'nvme ssd', 'external hdd', 'desktop hdd', 'laptop hdd', 'usb external hdd', 'nas hdd', 'server hdd', 
            'backup ssd', 'gaming ssd', 'high-speed ssd', 'hdd to ssd upgrade kit', 'sata to usb adapter', 'nvme to usb adapter', 
            'hard drive duplicator', 'data recovery kit', 'hard drive enclosure', 'hard drive cooling fan', 'm.2 heatsink'
        ]


        # Create the tags if they don't already exist
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Tag '{tag_name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Tag '{tag_name}' already exists"))
