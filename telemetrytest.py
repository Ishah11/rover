import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def read_serial_packet():
    # Read until '<' is found

 
    if ser.in_waiting >= 0:
        while True:
         
            if ser.read(1) == b'<':
                break
        
        # Read the packet until '*' is found
        packet = []
        packet.append(b'')
        packet.append(b'')
        packet.append(b'')
        packet.append(b'')
        while True:
        
            byte = ser.read(1)
            
            if byte == b',':
                break
            packet[0] += byte

        while True:
        
            byte = ser.read(1)
           
            if byte == b',':
                break
            packet[1] += byte

        while True:
        
            byte = ser.read(1)
            
            if byte == b',':
                break
            packet[2] += byte
        
        while True:

            byte = ser.read(1)
        
            if byte == b'>':
                break
            packet[3] += byte
            
      
        return packet





# Main loop to read packets
if __name__ == "__main__":
    #ser.reset_input_buffer()
    print("Serial OK")
    try:
        while True:
            packet = read_serial_packet()
            sensor_id = int.from_bytes(packet[0], byteorder='little') 
            packet_length = int.from_bytes(packet[1], byteorder='little')
            sensor_value_bytes = int.from_bytes(packet[2], byteorder='little')
            checksum = int.from_bytes(packet[3], byteorder='little')
            calculated_checksum = (sensor_id + packet_length + sensor_value_bytes) #checksum function that verifies the value of the byte as well as the packet length
            #print(f"Received packet - ID: {sensor_id}, Length: {packet_length}, Value1: {sensor_value_bytes}, Checksum: {checksum}")
            #print(f"Calculated checksum: {calculated_checksum}")
            if calculated_checksum == checksum: #checks the calcualted checksum value and validates it
                print(f"Received packet - ID: {sensor_id}, Length: {packet_length}, Value1: {sensor_value_bytes}, Checksum: {checksum}")
            else:
                print(f"Checksum error for Sensor ID: {sensor_id}")

    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        ser.close()  # Close the serial port
