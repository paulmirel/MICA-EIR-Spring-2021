float increment = 0.01; // larger equals finer grain 
// The noise function's 3rd argument, a global variable that increments once per cycle
float zoff = 0.0;  
// We will increment zoff differently than xoff and yoff
float zincrement = 0.2; // larger equals "faster" change

NoiseScape drawer;
float f_rate = 30;

void setup() {

  size(1280, 720);
  frameRate(f_rate);

  DataSource data_source = new SerialDataSourceStella();
  drawer = new AlanNoiseScape(data_source);
}

void draw() {

  // Optional: adjust noise detail here
  // noiseDetail(8,0.65f);

  loadPixels();
  drawer.one_frame();
  updatePixels();
  
  drawer.datasource.update();
  
  // every second:
  // if ( frameCount % f_rate == 0 ) {


}
