final float BOID_RADIUS = 2.0;
final float VICINITY = 20.0;

class Boid {  
  PVector position;
  PVector velocity;
  
  float maxSpeed = 1;
  
  Boid(float x, float y) {
     position = new PVector(x, y);
     velocity = PVector.random2D();     
  }
  
  void run(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    updateBoid(boids, obstacles);
    move();
    borders();
    render();    
  }
  
  void updateBoid(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    ArrayList<Boid> neighbors = findNeighbors(boids);
    
    PVector sep = calculateSeparationForce(neighbors);
    PVector align = calculateAlignmentForce(neighbors);
    PVector coh = calculateCohesionForce(neighbors);
    PVector avoid = calculateAvoidanceForce(obstacles);
    
    sep.mult(separationWeight);
    align.mult(alignmentWeight);
    coh.mult(cohesionWeight);
    avoid.mult(avoidanceWeight);
    
    velocity.add(sep);
    velocity.add(align);
    velocity.add(coh);
    velocity.add(avoid);
  } 
  
  // finds all neighbours closer than VICINITY
  ArrayList<Boid> findNeighbors(ArrayList<Boid> boids) {
    ArrayList<Boid> neighbors = new ArrayList<Boid>();
    for (Boid other : boids) {
      float d = PVector.dist(position, other.position);
      if ((d > 0) && (d < VICINITY)) {     
        neighbors.add(other);  
      }  
    }
    
    return neighbors;
  }  
  
  PVector calculateSeparationForce(ArrayList<Boid> boids) {
    PVector sep = new PVector(0,0);

    for (Boid other : boids) {
      PVector distance = PVector.sub(other.position, position);
      distance.normalize();
      sep.add(distance);
    }
            
    sep.mult(-1);          
        
    if (boids.size() > 0) {
       sep.div(boids.size());
    }     
   
    sep.normalize(); 
            
    return sep;
  }
  
  PVector calculateAlignmentForce(ArrayList<Boid> boids) {
    PVector align = new PVector(0,0);
    for (Boid other : boids) {
      align.add(other.velocity);      
    }
    
    if (boids.size() > 0) {
       align.div(boids.size());
       align.normalize();
    }    
    
    return align;
  }
  
  PVector calculateCohesionForce(ArrayList<Boid> boids) {
    PVector coh = new PVector(0,0);
    for (Boid other : boids) {
      coh.add(other.position);
    }
    
    if (boids.size() > 0) {
       coh.div(boids.size());
       coh = PVector.sub(coh, position);
       coh.normalize();
    }        
        
    return coh;
  }  
  
  PVector calculateAvoidanceForce(ArrayList<Obstacle> obstacles) {
    PVector ahead = PVector.add(position, PVector.mult(velocity, VICINITY));
    Obstacle closest = getClosestObstacle(ahead, obstacles);
    
    if (closest == null) {
      return new PVector(0,0);
    }    
        
    PVector avoid = PVector.sub(ahead, closest.position);
    avoid.normalize();
    avoid.mult(0.9);
        
    return avoid;    
  }  
  
  Obstacle getClosestObstacle(PVector ahead, ArrayList<Obstacle> obstacles) {    
    Obstacle closest = null;
        
    for (Obstacle obstacle : obstacles) {
      float distance = obstacle.position.dist(ahead);
      if (distance <= obstacle.radius && 
         (closest == null || obstacle.position.dist(position) < closest.position.dist(position))) {
          closest = obstacle;
      }           
    }      
    
    return closest;
  }
  
  // Wraparound
  void borders() {
    if (position.x < -BOID_RADIUS) position.x = width+BOID_RADIUS;
    if (position.y < -BOID_RADIUS) position.y = height-70+BOID_RADIUS;
    if (position.x > width+BOID_RADIUS) position.x = -BOID_RADIUS;
    if (position.y > height-70+BOID_RADIUS) position.y = -BOID_RADIUS;
  }  
    
  void move() {    
    velocity.limit(maxSpeed);    
    position.add(velocity);
  }
 
  void render() {
    // Draw a triangle rotated in the direction of velocity
    float theta = velocity.heading2D() + radians(90);
    // heading2D() above is now heading() but leaving old syntax until Processing.js catches up
    
    fill(200, 100);
    stroke(255);
    pushMatrix();
    translate(position.x, position.y);
    rotate(theta);
    beginShape(TRIANGLES);
    vertex(0, -BOID_RADIUS*2);
    vertex(-BOID_RADIUS, BOID_RADIUS*2);
    vertex(BOID_RADIUS, BOID_RADIUS*2);
    endShape();
    popMatrix();   
  }
  
  String toString() {
    return "position: " + position + ", velocity: " + velocity;
  }
}
