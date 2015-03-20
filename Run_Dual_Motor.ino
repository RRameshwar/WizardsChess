// Initializing pins
const int pwr1_a = 3;
const int pwr1_b = 9;
const int dir1_a = 2;
const int dir1_b = 8;
const int pwr2_a = 5;
const int pwr2_b = 10;
const int dir2_a = 4;
const int dir2_b = 12;
const int MAGNET = 7;
const int STEPS = 2*200;      //total count of halfsteps per full rotation (*2 for half steps!)
// e.g. 1.8deg stepper => 200 steps => 400 halfsteps
int currStep = 0;             //current step, corresponds to angular position,  limits: 0...STEPS
int sub = 0;                  //current halfstep within repeating sequence (8 halfsteps), limits: 0...7
int stepdelay = 7000;    //Wait time between steps (microseconds) - slow drive

int mag = 0;
int xDir = 0;
int xDist = 0;
int yDir = 0;
int yDist = 0;
long int val = 0;


void setup()
{
  // Initialize the pins, in the correct type of mode.
  Serial.begin(9600);
  pinMode(pwr1_a,OUTPUT);
  pinMode(pwr1_b,OUTPUT);
  pinMode(dir1_a,OUTPUT);
  pinMode(dir1_b,OUTPUT);
  pinMode(pwr2_a,OUTPUT);
  pinMode(pwr2_b,OUTPUT);
  pinMode(dir2_a,OUTPUT);
  pinMode(dir2_b,OUTPUT);
  pinMode(MAGNET,OUTPUT);
  digitalWrite(MAGNET,LOW);
  
}


void loop()
{
  if (Serial.available()){
    
  //Get command from python
  val = Serial.parseInt();

  //Unpack command
  mag = (val/100000000);
  xDir = (val/10000000)%10;
  xDist = ((val/10000)%1000)*2;
  yDir = (val/1000)%10;
  yDist = (val%1000)*2;
  
  //Interpret directions
  if (xDir == 2){ xDir = -1; }
  else { xDir = 1; }
  if (yDir == 2){ yDir = -1; }
  else { yDir = 1; }
 
  //Control the magnet
  if (mag == 1) { digitalWrite(MAGNET, HIGH); }
  else { digitalWrite(MAGNET, LOW); }
  
  //Control the motors
  if (xDist == yDist && xDist != 0) {    
     if (xDir == yDir){
        for (int i=0;i<xDist/2;i++){
          subStep1(xDir, stepdelay); //X Motor (small axis)
          subStep2(yDir, stepdelay); //Y Motor (large axis)
        }
     }
     else {
       for (int i=0;i<xDist/8;i++){
          subStep1(xDir*10, stepdelay); //X Motor (small axis)
          subStep2(yDir*10, stepdelay); //Y Motor (large axis)
        }
     }
  }
  
  else {
    //Non-diagonal
    subStep1(xDir*xDist, stepdelay); //X Motor (small axis)
    subStep2(yDir*yDist, stepdelay); //Y Motor (large axis)
  }
  
  TurnOffMotors();
  
  //Tell python you're done
  Serial.print("Done\n");
  
  }
}


// This method simply just turns off the motors, called when ever we don't need the motors anymore.
// In this way, we won't fray the circuit or coils.
// Note 1: Motor has no torque anymore
// Note 2: If current position is between full steps, motor will move for a half step!
void TurnOffMotors(){
  digitalWrite(pwr1_a,LOW);
  digitalWrite(pwr1_b,LOW);
  digitalWrite(dir1_a,LOW);
  digitalWrite(dir1_b,LOW);
  digitalWrite(pwr2_a,LOW);
  digitalWrite(pwr2_b,LOW);
  digitalWrite(dir2_a,LOW);
  digitalWrite(dir2_b,LOW);
}

