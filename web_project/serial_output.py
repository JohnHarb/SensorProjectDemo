from serial import Serial

serial_port = 'COM3';
baud_rate = 9600;
write_to_file_path = "/Users/zastr/OneDrive/Desktop/output.txt";

output_file = open(write_to_file_path, "w+")
ser = Serial(serial_port, baud_rate)
while True:
    line = ser.readline();
    line = line.decode("utf-8")
    print(line);
    output_file.write(line);