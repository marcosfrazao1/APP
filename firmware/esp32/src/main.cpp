#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configure antes do uso em campo.
const char* WIFI_SSID = "SEU_WIFI";
const char* WIFI_PASSWORD = "SUA_SENHA";
const char* API_URL = "http://SEU_SERVIDOR:8000/api/v1/readings";
const char* DEVICE_ID = "ete-monitor-001";

// Pinos de exemplo. Os pinos finais dependem dos módulos adquiridos.
constexpr int PIN_TEMP = 4;
constexpr int PIN_TURBIDITY = 34;
constexpr int PIN_EC = 35;
constexpr int PIN_PH = 32;
constexpr int PIN_DO = 33;

constexpr unsigned long SAMPLE_INTERVAL_MS = 10000;
unsigned long lastSample = 0;

float readTemperatureC() {
  // TODO: implementar DS18B20 com biblioteca adequada.
  return NAN;
}

float readAnalogPlaceholder(int pin) {
  int raw = analogRead(pin);
  return static_cast<float>(raw);
}

bool postReading(float ph, float turbidity, float conductivity, float temperature, float dissolvedOxygen) {
  if (WiFi.status() != WL_CONNECTED) return false;

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");

  JsonDocument doc;
  doc["device_id"] = DEVICE_ID;
  doc["timestamp_ms"] = millis();
  doc["ph"] = ph;
  doc["turbidity_ntu"] = turbidity;
  doc["conductivity_us_cm"] = conductivity;
  doc["temperature_c"] = temperature;
  doc["dissolved_oxygen_mg_l"] = dissolvedOxygen;
  doc["quality"] = "raw";

  String payload;
  serializeJson(doc, payload);
  int code = http.POST(payload);
  http.end();
  return code >= 200 && code < 300;
}

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
    delay(250);
  }
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  connectWiFi();
}

void loop() {
  if (millis() - lastSample < SAMPLE_INTERVAL_MS) return;
  lastSample = millis();

  float temperature = readTemperatureC();
  float turbidityRaw = readAnalogPlaceholder(PIN_TURBIDITY);
  float conductivityRaw = readAnalogPlaceholder(PIN_EC);
  float phRaw = readAnalogPlaceholder(PIN_PH);
  float doRaw = readAnalogPlaceholder(PIN_DO);

  // TODO: substituir os valores brutos por conversões calibradas.
  bool sent = postReading(phRaw, turbidityRaw, conductivityRaw, temperature, doRaw);
  Serial.printf("Leitura enviada=%s\n", sent ? "sim" : "nao");
}
