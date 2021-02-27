import java.lang.Math;

class AlanNoiseScape extends NoiseScape {

  // a few choices for dynamic behavior

  AlanNoiseScape(DataSource data_source) { 
    super(data_source);
  }

  float graininess() { 
    // we want about .05 to about 0.001
    // for temperature room -> body

    // hmm, want to do something like: temp->to->graininess
    //  and temp knows its range, and graininess knows its range

    // high temp is finer grained
    return map( datasource.temperature(), 15.0, 50.0, 0.001, 0.05);
  }

  float speed() {
    // i.e. step size in the z noise dimension
    // high temp is slower
    return map( datasource.temperature(), 15.0, 40.0, 0.1, 0.03);
  }

  color rgb(float brightness) {
    // convert each pixel to rgb

    float colors[] = datasource.vis_color();

    // get the average of the power
    float total = 0;
    for (float p : colors ) {
      total += p;
    }
    float avg = total / colors.length;

    // group into rgb
    float red = (colors[5] + colors[4]) / 2.0;
    float green = (colors[3] + colors[2]) / 2.0;
    float blue = (colors[1] + colors[0]) / 2.0;

    // re-map to full scale
    float min = Math.min( red, Math.min( green, blue ));
    float max = Math.max( red, Math.max( green, blue ));
    max += 0.001;

    red = map( red, min, max, 0.0, 1.0 );
    green = map( green, min, max, 0.0, 1.0 );
    blue = map( blue, min, max, 0.0, 1.0 );

    return color( red*brightness*255, green*brightness*255, blue*brightness*255 );
  }
}
