final float BOID_RADIUS = 2.0;
final float BOID_VICINITY = 25.0;
final float OBSTACLE_LOOKAHEAD = 20.0;

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

    velocity.add(sep);
    velocity.add(align);
    velocity.add(coh);
    velocity.add(avoid);
    velocity.add(escape);
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
      if ((d > 0) && (d < BOID_VICINITY) && (other instanceof Predator)) {
        closePredators.add((Predator)other);
      }
    }

    return closePredators;
  }

  PVector calculateSeparationForce(ArrayList<Boid> boids) {
    PVector sep = new PVector(0, 0);

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
    PVector align = new PVector(0, 0);
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
    PVector ahead = PVector.add(position, PVector.mult(velocity, OBSTACLE_LOOKAHEAD));
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
      if (distance <= obstacle.radius &&
        (closest == null || obstacle.position.dist(position) < closest.position.dist(position))) {
        closest = obstacle;
      }
    }      

    return closest;
  }  

  PVector calculateEscapeForce(ArrayList<Predator> predators) {
    //PVector escape = new PVector(0,0);   
    if (predators.size() == 0) {
     return new PVector(0,0); 
    }
      
    
    float angle = PVector.angleBetween(predators.get(0).velocity, velocity);
    
    //println ("pr: " + predators.get(0).velocity + " bo: " + velocity + " : " + degrees(angle) );

    PVector escape = PVector.sub(predators.get(0).position, position);
    escape.normalize();
    escape.mult(-1);
    //escape.rotate(radians(random(-45, 45)));

    return escape;
  }

  void move() {    
    velocity.limit(maxSpeed);    
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
    // Draw a triangle rotated in the direction of velocity
    float theta = velocity.heading2D() + radians(90);
    // heading2D() above is now heading() but leaving old syntax until Processing.js catches up

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

