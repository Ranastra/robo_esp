########### ADC Multiplexer (CD74HC4067S)############

S0 = 4
S1 = 5
S2 = 12
S3 = 14
ADC_MULTI = 39

ADC_PT_REF_L = 0  # silver
ADC_PT_L_1 = 1
ADC_PT_L_0 = 2
ADC_PT_M = 3
ADC_PT_R_0 = 4
ADC_PT_R_1 = 5
ADC_PT_REF_R = 6  # silver
ADC_PT_RGB = 7  # front sensor
ADC_PT_L_3 = 8
ADC_PT_L_2 = 9
ADC_PT_R_2 = 10
ADC_PT_R_3 = 11
ADC_T_M = 12
ADC_AE1 = 13  # External Analog Input
ADC_AE2 = 14  # External Analog Input
ADC_AE3 = 15  # External Analog Input


##################### Servos#########################

SERVO1 = 19
SERVO2 = 18
SERVO3 = 17
SERVO4 = 16
SERVO5 = 13

############# Motor Driver (TB6612FNG)###############

PWMA = 26
PWMB = 25

############ Shiftregister (74HC595PW)###############

SHCP = 27
STCP = 32
DS = 33

# Shiftregister IC10

SR_AIN1 = 0
SR_AIN2 = 1
SR_BIN1 = 2
SR_BIN2 = 3
SR_STBY = 4
SR_LED_L_RED = 5  # Light sensor bar white led ##HIGH - ON
SR_LED_L_GREEN = 6  # Light sensor bar red led
SR_LED_L_BLUE = 7  # Light sensor bar green led

# Shiftregister IC12

SR_LED_R_RED = 8  # Light sensor bar blue led
SR_LED_R_GREEN = 9  # LOW - ON
SR_LED_R_BLUE = 10  # status leds
SR_XSHT1 = 11
SR_XSHT2 = 12
SR_XSHT3 = 13
SR_XSHT4 = 14
SR_RGB_RED = 15  # TOF Select

# Shiftregister IC13

SR_RGB_GREEN = 16
SR_PT_WHITE = 17
SR_PT_RED = 18
SR_PT_GREEN = 19
SR_PT_BLUE = 20
SR_DE1 = 21  # External Digital Pins
SR_DE2 = 22  
SR_DE3 = 23 

################# Rotary Encoder#####################

ENC_A = 35
ENC_B = 34
ENC_SW = 15

################# extern Buttons#####################

T_L = 2  # Button left
T_R = 23  # Button right
# T_M = 12  # Button center

##################### Battery########################

VBAT = 36

###################### I2C###########################

SDA = 21
SCL = 22
MPU6050_ADRESS = 0x68  # 0x51 in c++
OLED_ADRESS = 0x3C
TOF_ADRESS = 0x29
