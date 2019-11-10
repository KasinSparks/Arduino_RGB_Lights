#define REDPIN  3
#define GREENPIN 5
#define BLUEPIN 6

#define FADESPEED 5

#define COMMAND_BUFFER_LENGTH 16

enum Color{
  RED=0,
  GREEN,
  BLUE
};

struct lights{
  Color color;
  int value;
  int pinNum;
};

lights myLights[3];

void setup() {
  // Initilize values
  pinMode(REDPIN, OUTPUT);
  pinMode(GREENPIN, OUTPUT);
  pinMode(BLUEPIN, OUTPUT);

  myLights[0].color = Color::RED;
  myLights[0].value = 0;
  myLights[0].pinNum = REDPIN;

  myLights[1].color = Color::GREEN;
  myLights[1].value = 0;
  myLights[1].pinNum = GREENPIN;
  
  myLights[2].color = Color::BLUE;
  myLights[2].value = 0;
  myLights[2].pinNum = BLUEPIN;

  Serial.begin(9600);
}

// Will fade a light from current value to toVal at a rate defined by FADESPEED
void fadeColor(lights &l, const int &toVal){
  int delta = (l.value - toVal < 0 ? -1 : 1);

  while(l.value != toVal){
    l.value -= delta;
    analogWrite(l.pinNum, l.value);
    delay(FADESPEED);
  }
}

// Fades mulitple lights to idv. values at a rate defined by FADESPEED
void fadeColors(lights *l, const unsigned int &numOfLights, const int *toVals, const unsigned int fadeSpeed = FADESPEED){
  int deltas[numOfLights];

  // Calculate deltas
  for(int i = 0; i < numOfLights; ++i){
    deltas[i] = (l[i].value - toVals[i] < 0 ? 1 : -1);
  }

  // Defined as if all lights reached their target value
  bool isDone = false;

  // Fade the lights
  while(!isDone){
    // Check for doneness and adjust light values
    isDone = true;

    for(int i = 0; i < numOfLights; ++i){
      if(l[i].value != toVals[i]){
        // Change the light value by delta
        l[i].value += deltas[i];

        // Send the value to pins
        analogWrite(l[i].pinNum, l[i].value);

        // Set done flag to not done
        isDone = false;
      }
    }

    // Set the delay
    delay(fadeSpeed);
    ///Serial.println("FADING");
  }
}

// Checks to see if the command is vaild
bool checkCommand(const char *command, const unsigned int &COMMAND_LENGTH, int **values){
  if (COMMAND_LENGTH != COMMAND_BUFFER_LENGTH) {
    return false;
  }

  // Check for format of xxx,xxx,xxx,xxx;
  int counterA = 0;
  int counterB = 0;

  for (int i = 0; i < COMMAND_LENGTH; ++i){
    // Comma positions
    if(i == 3 || i == 7 || i == 11){
      // Comma was not found in position
      if(command[i] != ',') return false;

      counterA++;
      counterB = 0;
    } else if(i == COMMAND_BUFFER_LENGTH - 1){
      // Semicolon position
      if(command[i] != ';') return false;
    } else {
      // Check for vaild ascii char
      if(command[i] < '0' || command[i] > '9'){
        Serial.println("ERROR with command....");
        return false;
      } else {
        values[counterA][counterB] = command[i] - '0';
        counterB++;
      }
    }
  }

  return true;
}

// Will calculate the base raised to the expoent using integers
int customSlowIntPow(const int &base, const int &expoent){
  int val = 1;

  for(int i = 0; i < expoent; ++i){
    val *= base;
  }

  if(val < 0 || val > 255){
    // Out of range
    val = 0;
  }

  return val;
}

// Converts the given number of values to a base 10 number. Example {1,2,3} -> 123
int convertTobase10Int(const int *vals, const int &numOfDigits){
  int value = 0;

  for(int i = 0; i < numOfDigits; ++i){
    value += vals[i] * customSlowIntPow(10, numOfDigits - 1 - i);
  }

  return value;
}

// Processed the command to change the light values
void processCommand(char *commandBuffer){
  const unsigned int NUM_OF_BYTES = 4;
  int *values[NUM_OF_BYTES];

  for(int i = 0; i < NUM_OF_BYTES; ++i){
    values[i] = new int[3];
  }

  // Check for vaild command
  if(!checkCommand(commandBuffer, COMMAND_BUFFER_LENGTH, values)){
    // Not a vaild command
    // clean up and return
    for(int i = 0; i < NUM_OF_BYTES; ++i){
      delete values[i];
    }
    return;
  }

  // Command must of been vaild... process command

  // Convert from 4 digit array to base ten number
  int numVals[NUM_OF_BYTES];
  for(int i = 0; i < NUM_OF_BYTES; ++i){
    numVals[i] = convertTobase10Int(values[i], 3);
  }

  // Change the lights
  fadeColors(myLights, 3, numVals, numVals[NUM_OF_BYTES - 1]);

  // Clean up
  for(int i = 0; i < NUM_OF_BYTES; ++i){
    delete values[i];
  }
}


// Read in the command from Serial input
void readInCommand(){
  char charIn = '\0';
  char commandBuffer[COMMAND_BUFFER_LENGTH];
  int numIn = 0;


  while(charIn != '\n' && numIn < COMMAND_BUFFER_LENGTH){
    // See if there is data to be read
    int numOfBytesInSerial = Serial.available();

    if(numOfBytesInSerial > 0){
      ///Serial.println("READING..");
      // Read the number of bytes available
      for(int i = 0; i < numOfBytesInSerial; ++i){
        charIn = Serial.read();

        // Reset the buffer
        if(charIn == 'r'){
          Serial.flush();
          return;
        }
        
        commandBuffer[numIn++] = charIn;
        delay(10);
      }
    }

    delay(100);
  }

  processCommand(commandBuffer);

  // Tell the controller we are done with given command
  Serial.println("DONE");
}



// Main loop
void loop() {
  readInCommand();
  //delay(1000);
}
