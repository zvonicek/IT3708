GSlider sepSl; 
GLabel LblPromptDur;

void drawGUI() {
  LblPromptDur = new GLabel(this, 10, height - 60, 110, 20);
  LblPromptDur.setText("Separation");
  LblPromptDur.setLocalColorScheme(4);
  
  sepSl = new GSlider(this, 10, height - 70, 200, 100, 15); 
  // Some of the following statements are not actually
  // required because they are setting the default value. 
  sepSl.setLocalColorScheme(4); 
  sepSl.setOpaque(false); 
  sepSl.setValue(0.91712713); 
  sepSl.setNbrTicks(2); 
  sepSl.setShowLimits(false); 
  sepSl.setShowValue(false); 
  sepSl.setShowTicks(true); 
  sepSl.setStickToTicks(false); 
  sepSl.setEasing(1.0); 
  sepSl.setLimits(0, 4);
  sepSl.setValue(1);
  sepSl.setRotation(0.0, GControlMode.CENTER); 
}

public void handleSliderEvents(GValueControl slider, GEvent event) {
  if (slider.equals(sepSl)) {
    separationWeight = slider.getValueF();
    println("a" + slider.getValueF()); 
  }
}
