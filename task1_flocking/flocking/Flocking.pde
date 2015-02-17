import g4p_controls.*;

Flock flock;

float separationWeight = 1.0;
float alignmentWeight = 1.0;
float cohesionWeight = 1.0;
float avoidanceWeight = 1000.0;
float escapeWeight = 10.0;

int selectedDropItem = 1;

void setup() {
  size(1000, 600);
  flock = new Flock();
  
  for (int i = 0; i < 350; i++) {
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
    if (selectedDropItem == 1) {
      flock.addObstacle(mouseX, mouseY);
    } else if (selectedDropItem == 2) {
      flock.addBoid(new Predator(mouseX, mouseY));
    }  
  } 
}

void clearButtonPressed() {
  if (selectedDropItem == 1) {
    flock.obstacles.clear();
  } else if (selectedDropItem == 2) {
    flock.deletePredators();
  }
}
