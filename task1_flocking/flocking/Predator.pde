
class Predator extends Boid {  
  Predator(float x, float y) {
     super(x,y);
     
     maxSpeed = 1.5;
  }
  
  void updateBoid(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    ArrayList<Boid> neighbors = findNeighbors(boids, 60.0);
    
    PVector coh = calculateCohesionForce(neighbors);
    PVector avoid = calculateAvoidanceForce(obstacles);   
    
    
    coh.mult(cohesionWeight);
    avoid.mult(avoidanceWeight); 
   
    velocity.add(coh);
    velocity.add(avoid);    
  }   
  
  void setColors() {
    fill(204, 102, 0);
    stroke(204, 102, 0);  
  }
}
