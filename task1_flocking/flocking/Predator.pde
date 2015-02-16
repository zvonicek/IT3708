
class Predator extends Boid {  
  Predator(float x, float y) {
     super(x,y);
     
     maxSpeed = 2.5;
     obstacleLookahead = 10;
  }
  
  PVector updateBoid(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    ArrayList<Boid> neighbors = findNeighbors(boids, 100.0);
    
    PVector coh = calculateCohesionForce(neighbors);
    PVector avoid = calculateAvoidanceForce(obstacles);   
    
    avoid.mult(avoidanceWeight); 
   
    PVector vel = new PVector(0,0);    
    vel.add(coh);
    vel.add(avoid);

    return vel;
  }   
  
  void setColors() {
    fill(204, 102, 0);
    stroke(204, 102, 0);  
  }
}
