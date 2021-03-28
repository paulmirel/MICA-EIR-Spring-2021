import processing.serial.*;

Serial connectUSBSerial(int baud) {
  // return a Serial object that we think is the usb-serial (arduino), or null
  String[] usbPorts = Serial.list();
  println(usbPorts);

  String arduinoPortName = null;
  for (int i = 0; i < usbPorts.length; i++) {
    if (
      // guess, based on historical names of ports
      // We are taking the first 1
      usbPorts[i].contains("ACM") // linux
      || usbPorts[i].contains("cu.usbmodem") // mac
      || usbPorts[i].contains("tty. usbmodem") // windows
      ) { 
      arduinoPortName = usbPorts[i];
    }
  }

  if (arduinoPortName != null) {
    print("Connected to ");
    println(arduinoPortName);
    return new Serial( this, arduinoPortName, baud);
  } else {
    println("Failed to find an usb serial");
    return null;
  }
}
