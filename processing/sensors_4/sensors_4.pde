/*
Assumes the device is printing left/right/up/down data like:
 [100,5,200,99]
 (range 0..255)
 Which test-codes/sense-4-sensors/code.py does 
 by reading the "gesture" sensor apds9660.
 Nb.: We rely on there being no spaces in that data string.
 
 Visualize the data:
 * as blocks in the cooresponding locations, 
 with brightness: black=0,white=255
 * as a horizontal line in each corresponding block, 
 bottom=0, top=255
 * as a dot showing the difference: 
 center means equal values. i.e. position.
 * as an ellipse trying to show proportional location
 */

Serial usb;

// precalculated box stuff
int box_width;
int box_height;

// The origin point of our 4 boxes, so we can iterate
PVector[] box_points;

void setup() {
  size(1280, 720);

  usb = connectUSBSerial(115200);
  // force circuitpython to reload
  usb.write(char(3));
  usb.write(char(3));
  usb.write(char(4));
  print("Started\n");

  // precalculate where the boxes are
  
  box_width = width / 3;
  box_height = height / 3;

  // The origin point of our 4 boxes, so we can iterate
  box_points = new PVector[] {
    new PVector(0, box_height), // middle-left, aka left  
    new PVector(2 * box_width, box_height), // middle-right, aka right  
    new PVector(box_width, 0), // middle-top aka up
    new PVector(box_width, 2 * box_height), // middle-bottom aka down
  };
}

void draw() {

  // Does not read the EOL,
  // SO, that EOL would appear at the beginning of the next line
  // (but we .clear() below, and so never see it)
  String line = usb.readStringUntil( 13 );
  usb.readBytes(1); // consume that pesky eol

  if (line != null) {

    // we only care about lines starting with [
    if (line.length() > 1 && line.charAt(0) == '[') { 
      if (usb.available() > 0) {
        // this clears any built-up data
        // because processing can't keep up
        // which means we do miss some data
        // but, we can't keep up anyway
        // and it doesn't make a big difference
        usb.clear();
      }

      // looks like [224,156,189,166] for 0..254
      // for left/right/up/down
      // get rid of leading [  & trailing ]
      // and split into the values
      String[] pieces = line.substring(1, line.length() - 2).split(",");

      print("DATA " );
      int number_of_values = 4;
      int[] values = new int[number_of_values];

      for (int i=0; i < number_of_values; i += 1) {
        values[i] = Integer.parseInt(pieces[i]);
        print(values[i], " ");
      }
      print("\n");

      update_boxes( values );
    } else {
      if (line.length() > 1) {
        // we echo all other lines,
        // so you can see what is going on with the device
        print(line, "\n");
      }
    }
  }
}

void update_boxes( int[] values ) {
  // (and other visualization elements)
  // do a tic-tac-toe arrangement basically
  //   1 | 2 | 3
  //   4 | 5 | 6
  //   7 | 8 | 9
  // and we only use 2,4,6,8 for left/right/up/down

  for (int i=0; i<4; i += 1) {
    // box
    fill(values[i]);
    stroke(values[i]);
    rect( box_points[i].x, box_points[i].y, box_width, box_height );

    // a horizontal line that is the more direct value
    stroke(255 - values[i]); // contrast
    // line is always horizontal, so x..right-x
    //  the y position changes w/value
    float y = box_points[i].y + box_height // from bottom of box
      - (values[i]/255.0 * box_height) ; // up to the proportionate value
    line( 
      box_points[i].x, int(y), 
      box_points[i].x + box_width, int(y) 
      );
  }
  // brainless "erase" of previous circle
  stroke(128);
  fill(128);
  rect( box_width, box_height, box_width, box_height);

  // an ellipse that is more proportional
  // (use the height so "balanced" == circle)
    stroke(0);
  fill(0);
  float left_x = (box_height - values[0]/255.0 * box_height)/2; // leftmost=0
  float right_x = (box_height + values[1]/255.0 * box_height)/2; // rightmost=boxwidth
  float up_y = (box_height - values[2]/255.0 * box_height)/2; // upmost=0
  float down_y = (box_height + values[3]/255.0 * box_height)/2; // downmost=boxheight
  ellipse(
   // centered in center box    
    box_width + (box_width - box_height)/2 + (left_x + right_x)/2, 
    box_height  + (up_y + down_y)/2,
    right_x-left_x,down_y-up_y
    );

  // cross hair in center
  stroke(180);
  line( 
    box_width * 1.1, box_height * 1.5, 
    box_width * 1.9, box_height * 1.5
    );
  line( 
    box_width * 1.5, box_height * 1.1, 
    box_width * 1.5, box_height * 1.9
    );

  // a "center" dot for "location"
  // which is kind-of relative
  float diff_x = ( values[1] - values[0] )/2;
  int center_x = int( box_width * 1.5 + (diff_x/255 * box_width) );
  float diff_y = ( values[3] - values[2] )/2;
  int center_y = int( box_height * 1.5 + (diff_y/255 * box_height) );

  stroke(255);
  fill(255);
  ellipse(center_x, center_y, 10, 10);
}
