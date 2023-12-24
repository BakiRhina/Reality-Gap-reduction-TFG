import time
import serial
import struct

class States():
    def __init__(self):
        print("Initializing States module fiiisss")
        self.ser = None
        self.retry_delay = 4
        time.sleep(0.1)


    def read_sensor_data(self, port, number_motors=10, number_sensors=15):
        while True:
            try:
                self.ser = serial.Serial(port, baudrate=115200, timeout=1)
                return self._receive_sensor_data(self.ser, number_motors, number_sensors)
            
            #except serial.serialutil.SerialException as e: # --> linux
            except Exception as e: # --> Windows
                print(f"Error: {e}")
                print(f"Waiting for {self.retry_delay} seconds before retrying...")
                for second in range(self.retry_delay, 0, -1):
                    print(f"{second}...")
                    time.sleep(1)
                    if second == 1:
                        break
            finally:
                if self.ser is not None:
                    self.ser.close()
                    
    def _receive_sensor_data(self, ser, number_motors, number_sensors):
        format_string = f'!{number_motors}i {number_sensors}f'
        expected_size = struct.calcsize(format_string)
        count = 0
        print("Waiting for state data...")
        while ser.in_waiting < expected_size:
            print(f"{count}...")
            time.sleep(1)
            count += 1

        # Read the packed data from the serial port
        packed_data = ser.read(expected_size)

        # Unpack the received data
        unpacked_data = struct.unpack(format_string, packed_data)

        # Convert the tuple to a list and return
        return list(unpacked_data)
