int contador = 0;
String archivoCompartido = "contador.txt";
float r=0;

void setup() {
  size(400, 400);
}

void draw() {
  background(255);
  
  // Leer el valor del contador desde el archivo compartido
  String[] lines = loadStrings(archivoCompartido);
  if (lines.length > 0) {
    contador = int(lines[0]);
    println("Rostros de Python: " + contador);
  }
  
  // Dibujar el círculo con el valor actual del contador
  float circleSize = map(contador, 0, 100, 0, width);
  ellipse(width/2, height/2, circleSize, circleSize);
  r=contador;
  text("rostros: "+r,5,11);
  textSize(16);
  fill(0);


}
