//#include <FirebaseArduino.h>
//#include <ESP8266WiFi.h>
#include <SPI.h>
#include <MFRC522.h>

//#define FIREBASE_HOST "cashierless-store-fa6cc.firebaseio.com/"
//#define FIREBASE_AUTH "7Y93JPGHrKDeaSmubQvsCQ5pYgGvUM3cIxMdIm5g"
//#define WIFI_SSID "shooter"
//#define WIFI_PASSWORD "29121998"

#define SS_PIN 10  //D2(4)
#define RST_PIN 9 //D1(5)

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;

void setup() {
  Serial.begin(9600);       // Initiate a serial communication
  SPI.begin();              // Initiate  SPI bus
  mfrc522.PCD_Init();       // Initiate MFRC522

//  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
//  Serial.print("connecting");
//  while (WiFi.status() != WL_CONNECTED) {
//    Serial.print(".");
//    delay(500);
//  }
//  Serial.println();
//  Serial.print("Connected: ");
//  Serial.println(WiFi.localIP());
//  
//  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
//  Firebase.setString("Detected UID","xx xx xx xx");
//  Firebase.setBool("Verification",0);
//  Firebase.setString("User","None");
//  Firebase.setString("Email","abc@example.com");
//  Firebase.setString("Password","xxxxx");
  
}

void loop() {

  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  //Show UID on serial monitor
  Serial.println();
  Serial.print("UID tag: ");
  String content= "";
  byte letter;

  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], OCT);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], OCT));
  }
  
  content.toUpperCase();
  Serial.println();
//  Firebase.setString("Detected UID",content.substring(1));
  
  if (content.substring(1) == "301 275 277 54")
  {
    Serial.println("User 1");
    Serial.println("Kitkat added");
//    Firebase.setString("User","Kitkat");
//    Firebase.setBool("Verification",1);
//    Firebase.setString("price","60");
//    Firebase.setString("Quantity","2");
    delay(1000);
    Serial.println();
    statuss = 1;
  }

  else if (content.substring(1) == "015 223 170 303")
  {
    Serial.println("User 2");
    Serial.println("Dairy milk silk added");
//    Firebase.setString("User","Dairy milk silk");
//    Firebase.setBool("Verification",1);
//    Firebase.setString("price","100");
//    Firebase.setString("quantity","1");
    delay(1000);
    Serial.println();
    statuss = 1;
  }
  
  else  {
    Serial.println("Access Denied.");
//    Firebase.setString("User","Unverified User");
//    Firebase.setBool("Verification",0);
//    Firebase.setString("Email","--");
//    Firebase.setString("Password","--");
    delay(1000);
  }

//  if (Firebase.failed()) {
//    Serial.print("setting /number failed:");
//    Serial.println(Firebase.error());
//    return;
//  }
  
  delay(1000);
}
