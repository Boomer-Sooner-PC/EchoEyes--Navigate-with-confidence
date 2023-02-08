#include <Arduino.h>
#include <LD06.h>

LD06forArduino lidar;

#define TOLERANCE 2
#define POINTS 8
#define MIN 30
#define MAX 500

int points[POINTS][2];

int pins[] = {2, 15, 16, 17, 18, 19, 20, 21};

void setup() {

  for (int i = 0; i < 360; i += (int)(360 / POINTS)) {
    points[i / (int)(360 / POINTS)][0] = i - TOLERANCE;
    points[i / (int)(360 / POINTS)][1] = i + TOLERANCE;
  }

  Serial.begin(115200);
  lidar.Init(17);

  Serial.println("setup done");
}

void loop() {
  lidar.read_lidar_data();

  for (int i = 0; i < lidar.angles.size(); i++) {
    int angle = lidar.angles[i];
    int distance = lidar.distances[i];
    int confidence = lidar.confidences[i];

    if (confidence < 10) {
      continue;
    }

    for (int j = 0; j < POINTS; j++)  {
      int point[] = { points[j][0], points[j][1] };
      if (point[0] <= angle && angle <= point[1]) {
        Serial.printf("point: %d, angle: %d, distance: %d, confidence: %d\n", j, angle, distance, confidence);
        int strength = map(distance, MIN, MAX, 80, 255);
        analogWrite(pins[j], strength);
      }
    }
  }
}

