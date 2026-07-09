# ZJUNlict Extended Team Description Paper for Robocup 2020

Zheyuan Huang<sup>1</sup> , Haodong Zhang<sup>1</sup> , Dashun Guo<sup>1</sup> , Shenhan Jia<sup>1</sup> , Xianze Fang<sup>1</sup> , Zexi Chen<sup>1</sup> , Yunkai Wang<sup>1</sup> , Peng Hu<sup>1</sup> , Licheng Wen<sup>1</sup> , Lingyun Chen<sup>1</sup> , Zhengxi Li<sup>1</sup> , and Rong Xiong<sup>1</sup>

Zhejiang University, Zheda Road No.38, Hangzhou, Zhejiang Province, P.R.China rxiong@zju.edu.cn http://zjunlict.cn

Abstract. ZJUNlict has won the champion of the Small Size League of RoboCup 2019 because of the great effort made in hardware and software. In this paper, we detailedly describe the major improvements that have contributed to our success. In hardware, we optimize our robots' mechanical structure and electronic board for better stability and stronger ball control ability. Also, we increase our robots' control frequency to achieve more accurate and stable control. In software, we develop a dynamic passing strategy and an off-the-ball running module which help us gain a high possession rate and offensive threat in the game.

### 1 Introduction

ZJUNlict has been participating in the Small Size League of RoboCup since 2004. We seek innovation and progress in software and hardware every year, which improves our competitiveness in the game and also brings us the champion of the Small Size League of Robocup 2019[1]. Our teammates come from different majors and have done excellent work in the software and hardware groups. This paper presents our work and is organized as follows: In Sects.2 and 3, we introduce our main optimization on hardware, including mechanical structure and electronic board. In Sects.4, we described how we increase the robot control frequency to achieve better motion control. In Sects.5 and 6, we discuss the dynamic passing strategy and the off-the-ball running module respectively which helped us gain a ball possession rate<sup>1</sup> of 68.8% during 7 matches in RoboCup 2019. In Sect.7, we analyze the performance of our algorithms at RoboCup 2019 with the log files recorded during the matches.

<sup>1</sup> The possession rate is calculated by comparing the interception time of both sides. If the interception time of one team is shorter, the ball is considered to be possessed by this team.

### 2 Modification of Mechanical Structure of ZJUNlict

#### 2.1 The position of two capacitors

During a match of the Small Size League, robots could move as fast as 3.25 m/s. In this case, the stability of the robot became very important, and this year, we focused on the center of the gravity with a goal of lower it. In fact, there are already many teams got there hands busy with lowering the center of the gravity, eg, team KIKS and team RoboDragons have their robot compacted to 135 mm, and team TIGERs have their capacitor moved sideways instead of regularly laying upon the solenoid [2].

Thanks to the open source of team TIGERs [2], in this year's mechanical structure design, we moved the capacitor from the circuit board to the chassis. On the one hand, this lowers the center of gravity of the robot and makes the mechanical structure of the robot more compact, On the other hand, to give the upper board a larger space for future upgrades. The capacitor is fixed on the chassis via the 3D printed capacitor holder as shown in Figure 1, and in order to protect the capacitor from the impact that may be suffered on the field, we have added a metal protection board on the outside of the capacitor which made of 40Cr alloy steel with high strength.

Fig. 1: The new design of the capacitors

#### 2.2 The structure of the dribbling system

The handling of the dribbling part has always been a part we are proud of, and it is also the key to our strong ball control ability. In last year's champion paper, we have completely described our design concept, that is, using a one-degree-offreedom mouth structure, placing appropriate sponge pads on the rear and the lower part to form a nonlinear spring damping system. When a ball with certain speed hits the dribbler, the spring damping system can absorb the rebound force of the ball, and the dribbler uses a silica gel with a large friction force so that the ball can not be easily detached from the mouth.

The state of the sponge behind the mouth is critical to the performance of the dribbling system. In RoboCup 2018, there was a situation in which the sponge fell off, which had a great impact on the play of our game. In last year's design, as shown in Figure 2, we directly insert a sponge between the carbon plate at the mouth and the rear carbon plate. Under frequent and severe vibration, the sponge could easily to fall off[3]. In this case, we made some changes, a baffle is added between the dibbler and the rear carbon fiberboard, as shown in figure 3, and the sponge is glued to the baffle plate, which made it hard for the sponge to fall off, therefore greatly reduce the vibration.

Fig. 2: ZJUNlict 2018 mouth design Fig. 3: ZJUNlict 2019 mouth design

### 3 Modification of Electronic Board

In the past circuit design, we always thought that the board should be designed into multiple independent boards according to the function module so that if there is a problem, the whole board can be replaced. But then we gradually realized that instead of giving us convenience, it is unexpectedly complicated, on the one hand, we had to carry more spare boards, and on the other hand, it was not conducive to our maintenance.

#### 3.1 The new motherboard design

For the new design, we only kept one motherboard and one booster board, which reduced the number of boards, making the circuit structure more compact and more convenient for maintenance. We also fully adopted ST's STM32H743ZI master chip, which has a clock speed of up to 480MHz and has a wealth of peripherals. The chip is responsible for signal processing, packet unpacking and packaging, and motor control.

Thanks to the open source of TIGERs again, we use Allergo's A3930 threephase brushless motor control chip, simplifying the circuit design of the motor drive module on the motherboard. The biggest advancement in electronic this year was the completion of the stability test of the H743 version of the robot. In the case of all robots using the H743 chip, there was no robot failure caused by board damage during the game.In addition, we replaced the motor encoder

#### 4 Z. Huang et al.

from the original 360 lines to the current 1000 lines. The reading mode has been changed from the original direct reading to the current differential mode reading.

#### 3.2 The new attitude transducer: IMU

To increase the motion performance of our robot, we add an IMU on our motherboard. The IMU can measure the acceleration in three directions and the angular velocity of the robot. Then it calculates the angular velocity integral and gets the real time heading angel. It is a MEMS device and can be put on the PCB. To ensure the stability of the measurements of the angular velocity we tested the IMU and got a satisfying result. The temperature drift and the time drift are low. We put the robot on the level ground and let it stay static. The deviation of the heading angel in 5 minutes is less than 0.5 degree.

With the real time heading angel data got, we can control the heading angel in the lower computer and increase both the control frequency and the accuracy. This will be further discussed in Sects.4.

### 4 Increase the Control Frequency

On our research platform, ZJUNlict small size soccer team, the frequency of the global vision system is 75 Hz, which determines the frequency of coordination decision, motion planning and other control instructions.

As Figure 4 shows, after obtaining the target position and target orientation from the strategy layer (only the target orientation is concerned here), the motion planner plans next step according to the current orientation and speed obtained from the global visual system, and then sends the next speed instructions to the robot.

Fig. 4: Control scheme based on global vision system feedback frequency

There are four major problems with the current vision feedback system. Firstly, the frequency of the global vision system, 75Hz, is far enough for decision and planning, but it can not meet the requirements of fast and accurate motion control. Secondly, the global vision system information feedback has much noise. According to the experimental measurement, the amplitude of the vision information noise is up to 1 degree and the error of the feedback information seriously affects the precision of orientation control. Thirdly, the vision information we obtained has been processed by vision module. It takes about 3- 4 frames (40-60ms) from collecting the original vision information to obtaining the vision information. The feedback delay which makes the control precision significantly reduced (at present, it is solved by filtering, prediction and other methods) is not negligible. Fourthly, the frame rate of vision system is very unstable. When the communication is disturbed or the real-time vision processing cannot be fully guaranteed, the frame will be lost, which makes the control frequency unstable.

In order to solve these problems, the robot steering control is transferred to the slave computer, and the feedback information can be directly obtained from sensors such as gyroscope and coding plate. This improvement has achieved good results.

Fig. 5: Orientation control based on sensor feedback

The improved control scheme is shown in Figure 5. The host computer obtains the vision information at the frequency of 75Hz, and the robot will also upload the sensor information to the upper computer's motion planning layer by polling the packet (there are 11 robots in the field, and the communication protocol limits only four robots at a time). The host computer decides to send information of global vision or gyroscope to the slave computer according to the feedback and the instruction is target orientation, current orientation (for sensor calibration) or rotation speed ω (Sensor is broken).

The framework shown in the Figure 5 is divided into three cases: in the first case, the host computer planning layer determines that the sensor works normally and transmits the target orientation to the robot through wireless communication; when the robot gets the target orientation, it will calculate the rotation speed to be executed according to the current orientation and speed feedback by the gyroscope, and the control frequency of this process can reach to 500Hz. In the second case, when there is big difference between the global vision and the feedback information of the gyroscope, the motion planning layer thinks that it is necessary to calibrate the sensor, that is to say, "tell" the robot its current direction, then the host computer will send the filtered angle to the robot. In the third case, when there is no gyroscope information returning or the angle of gyroscope returning is obviously wrong, the planning layer adopts the original control scheme: according to the image feedback, the rotation speed is planned and issued, and the robot steering control automatically adjusts back to 75Hz.

The new scheme greatly improves the control frequency of steering. As shown in Figure 6, the effect of steering control is significantly improved. Figure 6 is the comparison of the effect before and after the scheme improvement, and the orientation step test of 0.5rad is carried out for the robot respectively. Figure (a) is the low-frequency steering response curve based on the global vision. We can easily find that the robot is unstable to the point, and there is a steady-state error of about 0.03rad. Due to the low control frequency, the angle change curve of the robot has "sawtooth"; on the other hand, the angle of the image will also shake slightly when the robot reaches the target point. Figure (b) shows the high frequency response curve based on the sensor. It can be shown from the figure that although there is a little overshoot (the attenuation ratio is still in the acceptable range of 4:1 to 10:1), there is no steady-state error, and the response is rapid and stable.

Fig. 6: Step response of robot orientation control before (a) and after (b) (horizontal axis unit: frame; vertical axis unit: rad)

As shown in the experiment data in Figure 7, the feedback angle of the sensor is very stable. Since the maximum communication accuracy of the small football robot platform is about 0.087◦ (12 bit signed number), the feedback angle of the gyroscope obtained at this time is stable, so it can be determined that the maximum amplitude value of the angle noise of the gyroscope is strictly less than 0.17◦ (the accuracy given in the parameter table is 0.01◦ ), and the maximum image noise is The value is about 1.2 ◦ .

Fig. 7: Sensor and gyroscope angle feedback information

The difficulty of omni-directional wheeled robot motion control lies in the nonlinearity of dynamic model (there is coupling between robot translation and rotation). Intuitively, the rotation control and translation control of the robot are mutually disturbed. It is impossible to solve the nonlinear coupling problem by simply increasing the rotation control frequency. However, when the translation control frequency is kept unchanged and the update frequency of the rotation speed is increased to 500Hz, it can be seen that the path tracking effect of the robot is significantly improved.

In Figure 8, (a) is the track tracking effect at 75Hz control frequency and (b) is the path tracking effect at 500Hz. The reference path is three meters long and one meter wide. Both of them are the data collected by the robot running 4-5 laps in the real field. It is interesting that when the frequency is controlled at 500Hz, the trajectory of the robot in several laps almost coincides. The possible explanation is that the rotation speed of the four driving motors (four wheels) of the robot is obtained by kinematic decomposition of the motion instructions, so the frequency of updating the rotation speed is increased, which means that the frequency of updating the rotation speed of the driving motor is increased, and the uncertainty of the robot motion is also decreased accordingly.

Fig. 8: Comparison of robot track tracking effect

### 5 Dynamic Passing Strategy

#### 5.1 Real-time Passing Power Calculation

Passing power plays a key role in the passing process. For example, robot A wants to pass the ball to robot B. If the passing power is too small, the opponent will have plenty of time to intercept the ball. If the passing power is too large, robot B may fail to receive the ball in limited time. Therefore, it's significant to calculate appropriate passing power.

Suppose we know the location of robot A that holds the ball, its passing target point, and the position and speed information of robot B that is ready to receive the ball. We can accurately calculate the appropriate passing power based on the ball model shown in Figure 9. In the ideal ball model, after the ball is kicked out at a certain speed, the ball will first decelerate to 5/7 of the initial speed with a large sliding acceleration, and then decelerate to 0 with a small rolling acceleration.

Fig. 9: Ideal ball model

Let µ, g, m, r, M, β, v0, v1, t be the friction coefficient of the field, the gravity coefficient, the mass of the ball, the radius of the ball, the resultant moment of the ball, the angular acceleration of the ball, the initial speed of the ball, the speed at which the ball starts to roll, and the total time the ball slides respectively. Then the speed at which the ball changes from sliding to rolling can be calculated by the following equations.

During the slide,

$$M = \mu mgr = \frac{2}{5}mr^2\beta \tag{1}$$

$$\beta = \frac{5\mu g}{2r} \tag{2}$$

When the ball changes from sliding to rolling,

$$v_0 - \mu gt = \frac{5\mu g}{2r}rt\tag{3}$$

$$\mu gt = \frac{2}{7}v_0 \tag{4}$$

$$v_1 = v_0 - \mu gt = \frac{5}{7}v_0 \tag{5}$$

Based on this, we can use the passing time and the passing distance to calculate the passing power. Obviously, the passing distance is the distance between robot A and its passing target point. It's very easy to calculate the Euclidean distance between these two points. Passing time consists of two parts: robot B's arrival time and buffer time for adjustment after arrival. We calculate robot B's arrival time using last year's robot arrival time prediction algorithm. The buffer time is usually a constant (such as 0.3 second). Since the acceleration in the first deceleration process is very large and the deceleration time is very short, we ignore the moving distance of the first deceleration process and simplify the calculation. Let d, t and a be the passing distance, time and rolling acceleration. Then, the velocity of the ball after the first deceleration and the passing power are given by the following:

$$v_1 = (d + \frac{1}{2}at^2)/t \tag{6}$$

$$v_0 = v_1 / \frac{5}{7} \tag{7}$$

According to the capabilities of the robots, we can limit the threshold of passing power and apply it to the calculated result.

### 5.2 SBIP-Based Dynamic Passing Points Searching (DPPS) Algorithm

Passing is an important skill both offensively and defensively and the basic requirement for a successful passing process is that the ball can't be intercepted by opponents. Theoretically, we can get all feasible passing points based on the SBIP (Search-Based Interception Prediction) [3][4]. Assuming that one of our robots would pass the ball to another robot, it needs to ensure that the ball can't be intercepted by opposite robots, so we need the SBIP algorithm to calculate interception time of all robots on the field and return only the feasible passing points.

In order to improve the execution efficiency of the passing robot, we apply the searching process from t