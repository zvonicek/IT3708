class Obstacle {
  PVector position;  
  float radius = 20;
  
  Obstacle(PVector position) {
    this.position = position;
  }
  
  String toString() {
    return "position: " + position;
  }  
}
