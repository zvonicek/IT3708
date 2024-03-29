final float BOID_RADIUS = 2.5;
final float BOID_VICINITY = 45.0;

class Boid {  
  PVector position;
  PVector velocity;

  float maxSpeed = 2;
  float obstacleLookahead = 20.0;

  Boid(float x, float y) {
    position = new PVector(x, y);
    velocity = PVector.random2D();
  }

  void run(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    PVector vel = updateBoid(boids, obstacles);
    vel.normalize();
    velocity.add(vel);
    
    move();
    borders();
    render();
  }

  PVector updateBoid(ArrayList<Boid> boids, ArrayList<Obstacle> obstacles) {
    ArrayList<Boid> neighbors = findNeighbors(boids, BOID_VICINITY);
    ArrayList<Predator> closePredators = findClosePredators(boids);

    PVector sep = calculateSeparationForce(neighbors);
    PVector align = calculateAlignmentForce(neighbors);
    PVector coh = calculateCohesionForce(neighbors);
    PVector avoid = calculateAvoidanceForce(obstacles);
    PVector escape = calculateEscapeForce(closePredators);
    
    sep.mult(separationWeight);
    align.mult(alignmentWeight);
    coh.mult(cohesionWeight);
    avoid.mult(avoidanceWeight);         
    escape.mult(escapeWeight);
      
    PVector vel = new PVector(0,0);    
    vel.add(sep);
    vel.add(align);
    vel.add(coh);
    vel.add(avoid);
    vel.add(escape);    
    
    return vel;   
  } 

  // finds all neighbours closer than BOID_VICINITY
  ArrayList<Boid> findNeighbors(ArrayList<Boid> boids, float vicinity) {
    ArrayList<Boid> neighbors = new ArrayList<Boid>();
    for (Boid other : boids) {
      float d = PVector.dist(position, other.position);
      if ((d > 0) && (d < vicinity) && !(other instanceof Predator)) {     
        neighbors.add(other);
      }
    }

    return neighbors;
  }  

  ArrayList<Predator> findClosePredators(ArrayList<Boid> boids) {
    ArrayList<Predator> closePredators = new ArrayList<Predator>();
    for (Boid other : boids) {
      float d = PVector.dist(position, other.position);      
      if ((d > 0) && (d < BOID_VICINITY * 2) && (other instanceof Predator)) {
        closePredators.add((Predator)other);
      }
    }

    return closePredators;
  }

  PVector calculateSeparationForce(ArrayList<Boid> boids) {
    PVector sep = new PVector(0, 0);

    for (Boid other : boids) {
      PVector diff = PVector.sub(position, other.position);
      diff.normalize();
      diff.div(PVector.dist(position, other.position));
      sep.add(diff);
    }

    if (boids.size() > 0) {
      sep.normalize();     
    }

    return sep;
  }

  PVector calculateAlignmentForce(ArrayList<Boid> boids) {
    PVector align = new PVector(0, 0);
    for (Boid other : boids) {
      align.add(other.velocity);
    }

    if (boids.size() > 0) {
      align.normalize();
    }    

    return align;
  }

  PVector calculateCohesionForce(ArrayList<Boid> boids) {
    PVector coh = new PVector(0, 0);
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
    PVector ahead = PVector.add(position, PVector.mult(velocity, obstacleLookahead));    
    Obstacle closest = getClosestObstacle(ahead, obstacles);
    if (closest == null) {
      return new PVector(0, 0);
    }               

    PVector avoid = PVector.sub(ahead, closest.position);
    avoid.normalize();

    return avoid;
  }  

  Obstacle getClosestObstacle(PVector ahead, ArrayList<Obstacle> obstacles) {    
    Obstacle closest = null;
  
    for (Obstacle obstacle : obstacles) {
      float distance = obstacle.position.dist(ahead);
      if (circleLineIntersect(position.x, position.y, ahead.x, ahead.y, obstacle.position.x, obstacle.position.y, obstacle.radius) && 
         (closest == null || obstacle.position.dist(position) < closest.position.dist(position))) {
        closest = obstacle;
      }      
    }             

    return closest;
  }  

  PVector calculateEscapeForce(ArrayList<Predator> predators) {
    PVector esc = new PVector(0, 0);

    for (Predator predator : predators) {
      PVector diff = PVector.sub(position, predator.position);
      diff.normalize();
      esc.add(diff);
    }

    if (predators.size() > 0) {
      esc.normalize();      
    }    

    return esc;
  }

  void move() {   
    velocity.normalize();
    velocity.mult(maxSpeed);    
    position.add(velocity);
  }

  // GUI Rendering

  void borders() {
    if (position.x < -BOID_RADIUS) position.x = width+BOID_RADIUS;
    if (position.y < -BOID_RADIUS) position.y = height-70+BOID_RADIUS;
    if (position.x > width+BOID_RADIUS) position.x = -BOID_RADIUS;
    if (position.y > height-70+BOID_RADIUS) position.y = -BOID_RADIUS;
  }    

  void render() {
    float theta = velocity.heading() + radians(90);

    setColors();
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

  void setColors() {
    fill(200, 100);
    stroke(255);
  }

  String toString() {
    return "position: " + position + ", velocity: " + velocity;
  }  
}

