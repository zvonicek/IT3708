GSlider sepSl, alignSl, cohSl;
GLabel sepLab, alignLab, cohLab;
GToggleGroup dropGroup;
GOption dropObstacle, dropPredator;
GButton clearButton;

void drawGUI() {
  sepLab = new GLabel(this, 10, height - 60, 110, 20);
  sepLab.setText("Separation");
  sepLab.setLocalColorScheme(4);  
  sepSl = new GSlider(this, 10, height - 70, 200, 100, 15); 
  sepSl.setLocalColorScheme(4);  
  sepSl.setNbrTicks(3);  
  sepSl.setShowValue(true); 
  sepSl.setShowTicks(true); 
  sepSl.setEasing(1.0); 
  sepSl.setLimits(0.7, 1.3);
  sepSl.setValue(separationWeight); 
  
  alignLab = new GLabel(this, 230, height - 60, 110, 20);
  alignLab.setText("Alignment");
  alignLab.setLocalColorScheme(4);  
  alignSl = new GSlider(this, 230, height - 70, 200, 100, 15); 
  alignSl.setLocalColorScheme(4);  
  alignSl.setNbrTicks(3);  
  alignSl.setShowValue(true); 
  alignSl.setShowTicks(true); 
  alignSl.setEasing(1.0); 
  alignSl.setLimits(0.0, 2.0);
  alignSl.setValue(alignmentWeight);   
  
  cohLab = new GLabel(this, 440, height - 60, 110, 20);
  cohLab.setText("Cohesion");
  cohLab.setLocalColorScheme(4);  
  cohSl = new GSlider(this, 440, height - 70, 200, 100, 15); 
  cohSl.setLocalColorScheme(4);  
  cohSl.setNbrTicks(3);  
  cohSl.setShowValue(true); 
  cohSl.setShowTicks(true); 
  cohSl.setEasing(1.0); 
  cohSl.setLimits(0.7, 1.3);
  cohSl.setValue(cohesionWeight);   

  dropGroup = new GToggleGroup();
  
  dropObstacle = new GOption(this, 650, height-40, 70, 20);
  dropObstacle.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);
  dropObstacle.setText("Obstacle");  
  dropObstacle.setLocalColorScheme(4);
  dropObstacle.tag = "obstacle";
  dropObstacle.tagNo = 1;
  dropGroup.addControl(dropObstacle);
  
  dropPredator = new GOption(this, 650, height-20, 70, 20);
  dropPredator.setTextAlign(GAlign.LEFT, GAlign.MIDDLE);
  dropPredator.setText("Predator");  
  dropPredator.setLocalColorScheme(4);
  dropPredator.tag = "predator";
  dropPredator.tagNo = 2;  
  dropGroup.addControl(dropPredator);
  
  dropObstacle.setSelected(true);
  
  clearButton = new GButton(this, 740, height-30, 50, 20);
  clearButton.setLocalColorScheme(4);
  clearButton.setText("Clear");
}

public void handleSliderEvents(GValueControl slider, GEvent event) {
  if (slider.equals(sepSl)) {
    separationWeight = slider.getValueF();
  } else if (slider.equals(alignSl)) {
    alignmentWeight = slider.getValueF();    
  } else if (slider.equals(cohSl)) {
    cohesionWeight = slider.getValueF();    
  }
}

public void handleToggleControlEvents(GToggleControl option, GEvent event) {
 selectedDropItem = option.tagNo; 
}

public void handleButtonEvents(GButton button, GEvent event) {
  clearButtonPressed();
}

