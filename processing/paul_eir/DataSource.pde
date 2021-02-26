class RangedValue {
  // packages up a value with the range you want to use
  // for map() like behavior
  // basically curried, but you could do a non-linear mapping

  float v, min, max;

  RangedValue(float v, float from_min, float from_max) {
    this.v = v;
    this.min = min;
    this.max = max;
  }

  float to_range(float to_min, float to_max) {
    // map it to that range
    return map(v, min, max, to_min, to_max);
  }
}

class DataSource {
  // can read some sensor data from somewhere
  // and provide it as specific method names
  // Subclass for various "somewheres" (serial port, mqtt)

  // This base class uses the mouse to set the vis_color & temp
  float temperature() {
    // normalize? to a room temperature things, body =~ 37, room = 20
    return map(mouseX, 0, width, 15, 50); // a bit cold for room temp
  }

  public float[] vis_color() {
    // 6 bands, presumably going to be grouped to r,g,b
    // order is: vibgyor
    // stella gives numbers like 0..35
    // but this needs to map that to 0 .. 1.0
    float center = map(mouseY, 0, height, 0.0, 5.0);
    float power[] = new float[6];
    for (int i = 0; i < power.length; i++) {
      float delta = center - i;

      if ( delta < -2 || delta > 2 ) {
        power[i] = 0;
      } else if ( delta <= 0 ) {
        power[i] = map(delta, -2.0, 0.0, 0.0, 1.0 );
      } else if ( delta > 0 ) {
        power[i] = map(delta, 2.0, 0.0, 0.0, 1.0 );
      }
    }
    return power;
  }

  void update() {
    // if you need to calculate/read/etc
    // do it here, called every loop of draw()
  }
}

class NoiseScape {
  public
    // Draws noise frames
    // This base-class has fixed values
    // Subclass for data-driven

    // This base class has constant values, so is a bit boring
    
    float noise_z = 0.0;
  DataSource datasource;

  NoiseScape() {
    // shouldn't use this, but let's you subclass easier
    this.datasource  = new DataSource();
  }

  NoiseScape(DataSource d) { 
    this.datasource  = d;
  }

  float graininess() { 
    // i.e. step size in x,y in the noise dimensio
    return 0.002;
  }

  float speed() {
    // i.e. step size in the z noise dimension
    return 0.01;
  }

  color rgb(float brightness) {
    // convert each pixel to rgb

    return color( brightness*255, brightness*255, brightness*255 );
  }

  void one_frame() {
    float noise_x = 0.0; // Start noise_x at 0
    float frame_graniness = this.graininess(); // same for entire frame, faster

    //if ( frameCount % f_rate == 0 ) {
    //  println(datasource.vis_color());
    //}

    // For every x,y coordinate in a 2D space, calculate a noise value and produce a brightness value
    for (int x = 0; x < width; x++) {
      noise_x += frame_graniness;   // Increment noise_x * maybe temp is graininess

      float noise_y = 0.0;   // For every noise_x, start noise_y at 0

      for (int y = 0; y < height; y++) {
        noise_y += frame_graniness;
        ; // Increment noise_y

        // Calculate noise and scale by 255
        // possible group the color for xyz here
        float bright = noise(noise_x, noise_y, this.noise_z);

        // Try using this line instead
        //float bright = random(0,255);

        color rgb = this.rgb(bright);


        // Set each pixel onscreen to a grayscale value
        // * use temp*bright, color data
        pixels[x+y*width] = rgb;
      }
    }

    // * use remote-temp 0.002 is pretty slow and smooth, .1 pretty fast
    this.noise_z += this.speed(); // Increment zoff
  }
}
