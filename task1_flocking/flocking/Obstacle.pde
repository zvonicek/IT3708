class Obstacle {
  PVector position;  
  float radius = 20;
  
  Obstacle(PVector position) {
    this.position = position;
  }
  
  String toString() {
    return "position: " + position;
  }  
  
  void render() {
    fill(200, 100);
    stroke(255);      
    ellipse(o.position.x, o.position.y, o.radius, o.radius);    
  }
}
