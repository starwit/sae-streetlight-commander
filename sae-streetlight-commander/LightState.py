import asyncio
import time
from govee_local_api import GoveeController, GoveeDevice, GoveeLightFeatures

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
    return controller

async def turn_on(device: GoveeDevice) -> None:
    await device.turn_on()

async def set_color(device: GoveeDevice, r: int, g: int, b: int) -> None:
    await device.set_rgb_color(r, g, b)

async def main():
    controller: GoveeController = await create_controller(True)
    print(controller.devices[0])
    device = controller.devices[0]
    await turn_on(device)
    time.sleep(1)    
    intervall = 3
    for i in range(10):
        await set_color(device, 255, 0, 0)
        time.sleep(intervall)
        await set_color(device, 255, 255, 0)
        time.sleep(intervall)
        await set_color(device, 0, 255, 0)
        time.sleep(intervall)
        

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (EOFError, KeyboardInterrupt):
        print("REPL exited.")