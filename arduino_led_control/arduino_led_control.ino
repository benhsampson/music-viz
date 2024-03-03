
// receiving LED commands every 33 milliseconds (192 bytes)

// import necessary libraries
#include <FastLED.h>
 
// setup constants
#define LED_PIN     13
#define NUM_LEDS    64
#define BRIGHTNESS  170
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
#define ARR_SIZE 192
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100
 
CRGBPalette16 currentPalette;
TBlendType    currentBlending;

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

// LED buffer to command 64 leds using RGB values
char inputBuffer[192];

// setup
void setup() {

    delay( 3000 ); // power-up safety delay

    // open serial port (baudrate 9600 bits/second)
    Serial.begin(9600);

    // FastLED setup
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness( BRIGHTNESS );
}

// loop
void loop() { 
    while(!Serial.available());
    // check if data in serial buffer ()

    // store received data in array
    Serial.readBytesUntil('\r', inputBuffer, ARR_SIZE);
    
    // set LED colors
    for (byte i = 0; i < 192; i = i + 3) {
        byte R = inputBuffer[i];
        byte G = inputBuffer[i+1];
        byte B = inputBuffer[i+2];

        leds[i/3] = CRGB(R,G,B);
        FastLED.show();
    }

    // empty array after use
    memset(inputBuffer, 0, sizeof(inputBuffer));

}