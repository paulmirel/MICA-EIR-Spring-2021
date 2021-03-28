class SerialDataSourceStella  extends DataSource {
  // The stella is printing a python list structure,like:
  // ['0.1', 'Friday,20210226T191124Z,hh.hhhh,19.19', 'surface_temperature,C,23.3,1.0', 'air_temperature,C,22.4,0.3', 'relative_humidity,%,30,3', 'air_pressure,hPa,1030,1', 'altitude_uncalibrated,m,-135.6,100', 'visible_spectrum,nm,uW/cm^2,12/100', 450, 41.3, 500, 46.8, 550, 54.8, 570, 50.0, 600, 50.0, 650, 38.5, 'near_infrared_spectrum,nm,uW/cm^2,12/100', 610, 10.5, 680, 10.3, 730, 9.1, 760, 9.6, 810, 11.2, 860, 11.0]
  // We look for that and try to decode the right columns

  Serial port; // usb serial port to arduino/etc
  int buffer_next = 0; // where we are in the buffer
  byte[] buffer = new byte[11 * 1024]; // lots of room
  ReadALine dline;
  float _temp = 0.0;
  float _vis[] = new float[6];

  SerialDataSourceStella() {
    // on a crash, the port may not be released. restart processing then.
    // will be null if we can't find anything
    dline = new ReadALine(connectUSBSerial(115200), "[");
  }

  float temperature() {
    return this._temp;
  }

  float[] vis_color() {
    return this._vis;
  }
  
  void update() {
    String data_line = dline.get_line(); // only relevant lines

    if (data_line == null) return;

    print(data_line.length());
    print("> ");
    println(data_line);
    //print("  ");
    //println( data_line.getBytes() );


    if (! extract_temperature(data_line) ) {
      print("Failed to extract temperature");
    }
    
    if (! extract_vis(data_line) ) {
      print("Failed to extract vis");
    }
  }

  boolean extract_temperature(String data_line) {

    Float t = extract_float(data_line, "surface_temperature,C," );
    if (t == null) return false;

    this._temp = t.floatValue();
    print("temp ");
    println(this._temp);

    return true;
  }

  boolean extract_vis(String data_line) {
    String prefix = "'visible_spectrum,nm,uW/cm^2,12/100', ";
    int start = data_line.indexOf( prefix );
    if (start < 0) return false;
    
    //print("prefix ");println(data_line.substring(start));
        
    start += prefix.length();
    //print("data ");print( data_line.length());print(" ");println(data_line.substring(start));

    // vis data looks like:
    // 450, 0.0, 500, 0.0, 550, 0.0, 570, 0.0, 600, 0.0, 650, 0.0,
    // which is wavelength, value, value, precision...
    
    for(int i=0; i < this._vis.length * 2; i += 1) {
      // so, length pairs of data...
      
      int end = data_line.indexOf( ",", start);
      //print("  next ");print(i);print(" ");print(end);print(" ");
      //println( data_line.substring(start, end) );
      
      if ( i % 2 == 1 ) {
        // but only take every other one
        this._vis[i/2] = Float.parseFloat( data_line.substring(start, end) );
      }
      start = end + 1; // past ','
      //print(" past ");println( data_line.substring(start, start+6) );
      if ( data_line.substring(start,start+1).equals(" ") ) start += 1; // past ", "
    }
    print("vis ");
    for (float f : this._vis) print(f);
    println();
    return true;
  }

  Float extract_float(String data_line, String prefix ) {
    // extract the float following the prefix
    // or null

    int start = data_line.indexOf( prefix );
    if (start < 0) return null;

    start += prefix.length();
    /*
    print("found at ");
     print( start );
     print( " " );
     println( data_line.substring(start) );
     */

    int end = data_line.indexOf( ",", start );
    if (end < 0) end = data_line.length();

    return Float.parseFloat( data_line.substring(start, end) );
  }
}
