import java.lang.System; // for System.arraycopy

class ReadALine {
  // look for certain kinds of lines
  // e.g. "starts with ["

  // call .get_line() by serialEvent()
  // w/ bufferUntil('\r')
  // Get the next line with .get_line()

  Serial port;
  String line;
  String starts_with;

  ReadALine(Serial port, String starts_with ) {
    this.port = port;
    if ( port != null) {
      this.port.buffer(1024); // plenty of buffer space if loop is too slow
      this.port.bufferUntil( '\r' );
    }
    this.starts_with = starts_with;
  }

  boolean pred() {
    // return true if the line is the one we want
    String sofar = this.line.substring(0, this.starts_with.length() );
    /*
    print("? ");
     print( this.starts_with );
     print(" == ");
     print( this.line.substring(0, this.starts_with.length() ) );
     print(" ");
     println( sofar.equals( this.starts_with ));
     */
    return sofar.equals( this.starts_with );
  }

  String get_line() {
    // return the desired line or null
    
    if ( port == null) {
      return null;
    }

    if ( this.read_a_line() ) {

      if (this.pred()) {
        String x = this.line;
        //print("read ");
        //println(this.line);
        // safety: next time see nothing
        this.line = null;
        return x;
        
      } else {
        // throw away unwanted line
        this.line = null;
      }
    }
    
    return null;
  }

  boolean read_a_line() {
    // read into this.line, up to eol,
    // without blocking, because we were called by serialEvent w/bufferuntil
    // return true if we saw the upto marker

    this.line = port.readString();
    this.line = this.line.substring(1); // drop leading \r

    if ( this.line.length() <= 1 ) {
      // throw away blank or short lines
      this.line = null;
      return false;
    }

    return true; // didn't see it yet
  }
}
