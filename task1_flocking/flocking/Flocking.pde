import g4p_controls.*;

Flock flock;

float separationWeight = 1;
float alignmentWeight = 1;
float cohesionWeight = 1;

void setup() {
  size(640, 480);
  flock = new Flock();
  
  for (int i = 0; i < 150; i++) {
    flock.addBoid(new Boid(random(width),random(height)));
  }  
  
  drawGUI();
}

void draw() {
  background(50);
  flock.run();
}
