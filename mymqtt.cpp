#include <user_config.h>
#include <SmingCore/SmingCore.h>
#include <Libraries/Adafruit_SSD1306/Adafruit_SSD1306.h>
#include <Libraries/DHT/DHT.h>

Adafruit_SSD1306 display(4);
DHT dht(14);

void startMqttClient();
void onMessageReceived(String topic, String message);
void displayTemp(String s_temp);
void displayText(String s_msg);



Timer procTimer;

MqttClient mqtt("your_mqtt_server.com", 1883, onMessageReceived);


void publishMessage()
{
	if (mqtt.getConnectionState() != eTCS_Connected) {
		startMqttClient(); // Auto reconnect
		return;
	}

	TempAndHumidity th;
	if(!dht.readTempAndHumidity(th)) {
		return;
	}

	String message = "T=";
	message += th.temp;
	message += ", H=";
	message += th.humid;

	Serial.println("Let's publish message now!");

	mqtt.publish("your_topic", message);

	displayTemp(message);
}

void onMessageReceived(String topic, String message)
{
	Serial.print(topic);
	Serial.print(":\r\n\t"); 
	Serial.println(message);

	if(message.indexOf("T=") != 0)
		displayText(message);
}

void startMqttClient()
{
	if(!mqtt.setWill("last/will","The connection from this device is lost:(", 1, true)) {
		debugf("Unable to set the last will and testament. Most probably there is not enough memory on the device.");
	}
	mqtt.connect("ESP8266");
	mqtt.subscribe("your_topic");
	displayText("Start MQTT client...");
}


void connectFail()
{
	Serial.println("I'm NOT CONNECTED. Need help :(");
	displayText("I'm NOT CONNECTED. Need help !!");

}

void init()
{
	Serial.begin(SERIAL_BAUD_RATE);
	Serial.systemDebugOutput(true);

	display.begin(SSD1306_SWITCHCAPVCC);
	display.clearDisplay();

	dht.begin();
}


void displayTemp(String s_temp) {
	display.fillRect(0, 0, 128, 32, BLACK);
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(5,10);
	display.println(s_temp);
	display.display();
}

void displayText(String s_msg) {
	display.fillRect(0, 32, 128, 32, BLACK);
	display.setTextSize(1);
	display.setTextColor(WHITE);
	display.setCursor(5,40);
	display.println(s_msg);
	display.display();
}
