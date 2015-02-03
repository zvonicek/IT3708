GSlider sepSl; 
GSlider alignSl;
GSlider cohSl;
GLabel sepLab;
GLabel alignLab;
GLabel cohLab;

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
  sepSl.setLimits(0, 2);
  sepSl.setValue(1); 
  
  alignLab = new GLabel(this, 230, height - 60, 110, 20);
  alignLab.setText("Alignment");
  alignLab.setLocalColorScheme(4);  
  alignSl = new GSlider(this, 230, height - 70, 200, 100, 15); 
  alignSl.setLocalColorScheme(4);  
  alignSl.setNbrTicks(3);  
  alignSl.setShowValue(true); 
  alignSl.setShowTicks(true); 
  alignSl.setEasing(1.0); 
  alignSl.setLimits(0, 2);
  alignSl.setValue(1);   
  
  cohLab = new GLabel(this, 440, height - 60, 110, 20);
  cohLab.setText("Cohesion");
  cohLab.setLocalColorScheme(4);  
  cohSl = new GSlider(this, 440, height - 70, 200, 100, 15); 
  cohSl.setLocalColorScheme(4);  
  cohSl.setNbrTicks(3);  
  cohSl.setShowValue(true); 
  cohSl.setShowTicks(true); 
  cohSl.setEasing(1.0); 
  cohSl.setLimits(0, 2);
  cohSl.setValue(1);     
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
