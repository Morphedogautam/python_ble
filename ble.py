import time
import asyncio
from bleak import BleakClient
import os

DISTANCE = 0.6  # Corrected variable name
last_state = None
last_time = None
address = "FF:91:E0:91:F7:BA"
os.system('bluetoothctl -- remove FF:91:E0:91:F7:BA')
async def run():
    global last_state, last_time  # Added global keyword
    async with BleakClient(address) as client:
        while True:
            data = await client.read_gatt_char("00001002-494c-4359-4320-5241454e494c")
            if data == b'\x01' and last_state == b'\x00':
                current_time = time.time()
                if last_time is not None:  # Check if last_time is initialized
                    time_delta = current_time - last_time
                    speed = (DISTANCE * 2) / time_delta
                    print(f"speed: {speed:.2f} m/s")
                last_time = current_time
            last_state = data

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
