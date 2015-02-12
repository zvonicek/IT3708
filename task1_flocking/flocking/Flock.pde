
class Flock {
  ArrayList<Boid> boids;
  ArrayList<Obstacle> obstacles;
    
  Flock() {
    boids = new ArrayList<Boid>();
    obstacles = new ArrayList<Obstacle>();
  }
  
  void run() {
    for (Boid b: boids) {
       b.run(boids, obstacles);
    } 
    
    for (Obstacle o: obstacles) {
       o.render();      
    }
  }
  
  void addBoid(Boid b) {
     boids.add(b); 
  }
  
  void addObstacle(int x, int y) {
    for (Obstacle o: obstacles) {
      if (inCircle(x, y, o.position.x, o.position.y, o.radius)) {
        obstacles.remove(o);
        return;
      }
    }
    
    obstacles.add(new Obstacle(new PVector(x,y)));    
  }
  
  void deletePredators() {
    ArrayList<Boid> boidsCopy = new ArrayList<Boid>(boids);
    
    for (Boid b: boidsCopy) {
      if (b instanceof Predator) {
        boids.remove(b);
      }
    }       
  }
  
  boolean inCircle( float mx, float my, float cx, float cy, float circleDia ) {
    float distance = dist(mx, my, cx, cy);
    if (distance > circleDia/2) {
      return false;
    } 
    else {
      return true;
    }
  }  
  
}
