import logging
import asyncio
import time
from govee_local_api import GoveeController, GoveeDevice
from .db_functions import connect, get_count_data

from .config import LightsConfig

logger = logging.getLogger(__name__)

def update_device_callback(device: GoveeDevice) -> None:
    # print(f"Goveee device update callback: {device}")
    pass

def discovered_callback(device: GoveeDevice, is_new: bool) -> bool:
    if is_new:
        # print(f"Discovered: {device}. New: {is_new}")
        device.set_update_callback(update_device_callback)
    return True

async def create_controller(discovery_enabled: bool) -> GoveeController:
    controller = GoveeController(
        loop=asyncio.get_event_loop(),
        listening_address="0.0.0.0",
        discovery_enabled=discovery_enabled,
        discovered_callback=discovered_callback,
        evicted_callback=lambda device: print(f"Evicted {device}"),
    )

    await controller.start()

    if discovery_enabled:
        while not controller.devices:
            print("Waiting for devices... ")
            await asyncio.sleep(1)
    else: 
        logger.info(f"Discovery not enabled. Adding {CONFIG.lamp.hostname} to discovery.")
        controller.add_device_to_discovery_queue(CONFIG.lamp.hostname)
        while not controller.devices:
            logger.info(f"Waiting for device {CONFIG.lamp.hostname} to be discovered...")
            await asyncio.sleep(1)        
    return controller

async def turn_on(device: GoveeDevice) -> None:
    await device.turn_on()
    await set_color(device, 255, 255, 255)


async def set_color(device: GoveeDevice, r: int, g: int, b: int) -> None:
    await device.set_rgb_color(r, g, b)
    
async def setup_device():
    controller: GoveeController = await create_controller(False)
    global device
    device = controller.devices[0]
    print(device)
    await turn_on(device)
    return device
    
async def main():
    connect(CONFIG)
    device = await setup_device()
    time.sleep(1) 
    while True:
        count = get_count_data(CONFIG.lamp.observation_id)
        logger.info(f"Current object count {count}")
        if count > 0 and count < CONFIG.lamp.threshold_yellow:
            await set_color(device, 0, 255, 0)
        if count > CONFIG.lamp.threshold_yellow:
            await set_color(device, 255, 220, 0)
        if count > CONFIG.lamp.threshold_red:
            await set_color(device, 255, 0, 0)
        time.sleep(1)

def run_app():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    global CONFIG
    CONFIG = LightsConfig()
    logger.debug(f'Starting light commander. Config: {CONFIG.model_dump_json(indent=2)}')
    try:
        asyncio.run(main())
    except (EOFError, KeyboardInterrupt):
        logger.info("Shutting down")
        asyncio.run(device.turn_off())
 
if __name__ == "__main__":
    run_app()
        