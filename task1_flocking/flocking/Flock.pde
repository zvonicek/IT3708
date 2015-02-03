
class Flock {
  ArrayList<Boid> boids;
  ArrayList<PVector> obstacles;
  
  float obstacleRadius = 30;
  
  Flock() {
    boids = new ArrayList<Boid>();
    obstacles = new ArrayList<PVector>();
  }
  
  void run() {
    for (Boid b: boids) {
       b.run(boids);
    } 
    
    for (PVector o: obstacles) {
       ellipse(o.x, o.y, obstacleRadius, obstacleRadius);      
    }
  }
  
  void addBoid(Boid b) {
     boids.add(b); 
  }
  
  void addObstacle(int x, int y) {
    for (PVector o: obstacles) {
      if (inCircle(x, y, o.x, o.y, obstacleRadius)) {
        obstacles.remove(o);
        return;
      }
    }
    
    obstacles.add(new PVector(x,y));    
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
