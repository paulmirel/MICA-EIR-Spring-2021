float increment = 0.01; // larger equals finer grain 
// The noise function's 3rd argument, a global variable that increments once per cycle
float zoff = 0.0;  
// We will increment zoff differently than xoff and yoff
float zincrement = 0.2; // larger equals "faster" change

NoiseScape drawer;
float f_rate = 30;


void setup() {

  size(1280, 720);
  //size(640, 480);
  //frameRate(f_rate);

  // Non-interactive
  //drawer = new NoiseScape( new DataSource() );

  // mouse:
  //drawer = new AlanNoiseScape( new DataSource() );

  // stella
  drawer = new AlanNoiseScape( new SerialDataSourceStella() );
}

void draw() {

  loadPixels();
  drawer.one_frame();
  updatePixels();

  
  //print(frameCount); print(" "); println(frameRate);
  
  // every second:
  // if ( frameCount % f_rate == 0 ) {
}

void serialEvent(Serial x) {
  drawer.datasource.update();
}
