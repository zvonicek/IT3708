import g4p_controls.*;

Flock flock;

float separationWeight = 1.01;
float alignmentWeight = 1;
float cohesionWeight = 1;
float avoidanceWeight = 1.1;

void setup() {
  size(1000, 600);
  flock = new Flock();
  
  for (int i = 0; i < 300; i++) {
    flock.addBoid(new Boid(random(width),random(height)));
  }  
  
  drawGUI();
}

void draw() {
  background(50);
  flock.run();
}

void mousePressed() {
  if (mouseY < height - 70) {
    flock.addObstacle(mouseX, mouseY);
  } 
}
