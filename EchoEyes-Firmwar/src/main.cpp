#include <Arduino.h>
#include <LD06.h>

LD06forArduino lidar;

void setup() {
  Serial.begin(9600);
  lidar.Init(16);
}

void loop() {
  lidar.read_lidar_data();
  for (int i = 0; i < lidar.distances.size(); i++) {
    Serial.printf("%d %d,", (int)lidar.angles[i], (int)lidar.distances[i]);
  }
  Serial.println();
}