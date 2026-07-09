First Order Robotics Team Description Paper Small Size League of RoboCup 2025
Martin Liang, Joel Ng, Fred Huang, Louis Yong, Pi Rong Koh, Hamish Starling, and Luke Moran
Imperial College London, Exhibition Rd, South Kensington, London, UK firstorderrobotics@gmail.com
Abstract. This paper describes the efforts and improvements made by the First Order Robotics Team to compete in the 2025 RoboCup Small Size League Division B. It describes the major hardware improvements from the previous year's design, along with a newly developed codebase for the control and coordination of the robots.
1 Introduction
The First Order Robotics Team is a newly formed student-run group from Imperial College London under the umbrella of the Imperial College Robotics Society (ICRS). Initially formed under ICRS FC in 2023, the team was unsuccessful in qualifying, as it struggled with lacklustre student engagement, along with a plethora of mechanical, hardware and software roadblocks. This year, the team has seen a significant reconsolidation of its members' effort to design a credible hardware system and codebase by studying ETDPs and TDPs from successful teams, and learning from the team's past mistakes in 2024. This year, the team has also enjoyed a revitalized software development team that has made substantial progress in the robotic control and coordination algorithm design, as detailed in Section 5. This paper is divided into four major categories: mechanical systems, hardware, embedded systems and software.
2 Mechanical Systems
2.1 Objectives
Last year was our first attempt at designing and building robots that fit the RoboCup SSL competition criteria. The previous generation used a three-wheel omnidirectional layout with a simple fixed-frame dribbler design. The kicker employed a spring-loaded mechanism.
Looking back, many of these design decisions were not ideal. For example, the threewheel layout significantly restricted the dribbler module's open-for-catch size when receiving the ball. Another issue was that the chosen motor had a relatively long body extending toward the wheelbase center, severely limiting the available space for the solenoid, restricting shooting performance, and leaving no room for future upgrades. Only two units were produced last year. The design from last year can be seen in Figure 1 (1) and (2).
This year, our goal is to redesign from first principles, correct past mistakes, make well-informed engineering decisions for mass production, and ensure expandability for future iterations in the coming years. As a new team, we aim to achieve top-tier mechanical performance in Division B and ultimately reach a level where we are competitive with Division A teams.
The final design of the robot for SSL this year is shown in figure 1 (3)-(6), with details discussed below.

2023-4 SSL Robot Design
2024-5 SSL Robot Design
(3)Dimetric View
(4)Front View
(5)Side View
(6)Top View
Fig. 1. Robot design comparison between SSL 24 to 25

First Order Robotics Team Description Paper
2.2 Wheelbase
The wheelbase defines the overall framework of the mechatronic system, and the design  of  each  wheel  actuator  unit  directly  determines  the  available  design  space  for other modules. Therefore, it is made as compact as possible while ensuring sufficient clearance for the dribbler and kicker at the front and middle, respectively.
In our final design, each wheel actuator unit comprises a motor secured to a carbon fibre  base  using  a  CNC-machined  aluminium  alloy  block,  with  a  3D-printed  plastic spacer in between for reinforcement. This structure ensures rigidity and prevents yielding or bending. The CNC block is an off-the-shelf standard component with prethreaded mounting points, offering ease of assembly and cost efficiency. The assembled design is shown in figure 2.
Fig. 2. Exploded view of the wheel actuator assembly
We used the DM3519, a brushless motor with built-in precision FOC control and CAN communication. It delivers high power output, is compact, and remains cost-effective at just £40 per motor. This outperforms other motors in the same price range. The specifications of this motor is listed in Table 1.
Table 1. DM3519 Motor Specifications
DM3519 Motor Parameters
Rated Voltage
24V (Drive supports 15-52V supply)
Rated Phase Current (Power Supply Current)
9.2A (8.6A)
Peak Phase Current (Bus Current)
20.5A (16.1A)
Rated Torque
3.5Nm
Peak Torque
7.8Nm
Rated Speed
395rpm
No-load Maximum Speed
435rpm
With this crucial component finalized, the design space for other modules was established. The whole robot assembly breakdown is shown in Figure 3, with important specifications listed in Table 2.

M. Liang et al.
Fig. 3. Explode view of the wheel actuator assembly
Table 2. Essential Physical Specifications
2.3 Dribbler System
The dribbler is the most complex mechanical unit in an SSL robot. Based on insights from previous TDPs of other teams, a well-designed dribbler should have the following key features.
- High RPM: Ensures the ball remains in contact with the rod both at rest and during motion.
- Shock Absorption: Effectively dampens impact when the ball enters the dribbler at high speed.
- Self-Centering Capability: Improves precision shooting and enables the robot to execute sharper turns with higher angular velocity.
Due to budget limitations, we were unable to source for a dribbler motor with similar specifications (>35W, 20K+ RPM) as described in other papers   [11]. To minimize design limitations, we selected a 12W BLDC motor with a built-in Hall sensor and a speed of over 12K RPM, originally designed for surgical applications (e.g., plaster removal). The actual performance of this motor is still under evaluation, but based on initial observations, it performs satisfactorily.
Recognizing that the motor speed of the dribbler is crucial for ball control, we designed a ball feed-in status feedback mechanism to enable closed-loop control.

First Order Robotics Team Description Paper
2.3.1 Design Considerations & Mechanisms We studied the dribbler designs of teams such as ZJUNLICT [3] and TIGER [4], implementing a single DoF rotational mechanism for our dribbler. Additionally, a spring-damper system, commonly used in RC car models for shock absorption, was installed between the dribbler rotor frame and the wheelbase. The spring constantly pushes the dribbler rod forward, and when the ball enters, the compression of the spring and damping oil counteract the shock impact. Both the spring and damping oil are replaceable, allowing us to test different damping levels and spring constants.
A  parallelogram  linkage  is  constructed  within  the  dribbler,  with  one  side  fixed  to a  stationary  screw  and  the  other  attached  to  an  incremental  rotary  encoder.  This synchronizes  rotary  motion  and  provides  angle  feedback.  The  system  informs  the robot of the ball's behaviour - whether it is feeding in, leaving the rod, or bouncing against it. This feedback can dynamically adjust the dribbler speed, ensuring precise control. A visual illustration is shown in Figure 4.
(1)ball leaving
(2)Steady state
(3)ball crash-in
Fig. 4. Visual illustration of the dynamic interaction between ball and spring damper
Furthermore, the robot's forward/backward speed and angular velocity can be used as  feed-forward  inputs  in  the  control  loop.  This  helps  regulate  the  dribbler  speed, maintaining an upright ball position with three stable contact points - the carpet, chip shovel, and rod - for stable ball control.
Lastly, for self-centring, we are using a lathed aluminium rod as the core, with siliconemolled outer features. This allows for quick iterations and geometry testing. Several design iterations have been implemented, proving that a variable pitch spiral design is  effective.  In  some  cases,  the  ball  oscillates  back  and  forth  on  the  rod,  which  we suspect is due to improper damping and spring tuning. Further refinements will be made to optimize stability.
2.4  Kicker Actuation
The  kicker  of  the  robot,  although  designed  and  manufactured,  has  not  been  thoroughly tested due to the unfinished control board. The primary goal is to maximize the kicking speed.
From a research paper from Eastern Washington University  [14], we know that the force generated by a solenoid is proportional to certain key parameters, as shown in the equation below. A simple conclusion can be drawn: winding factor and internal resistance are crucial in solenoid coil design. A solenoid with thin wire and a high turn count is less desirable than one with thicker wire and fewer turns if the resistance is too high.
F = 8π ( ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂ ∂

6 M. Liang et al.
Where ρ is the resistivity of the material, is the cross-sectional area of the wire, is the coil length,  0 and  r are permittivity, V is the applied voltage, N is the number of windings, r 0 is the internal radius of the coil.
Additionally, the plunger material must have high magnetic permeability and high saturation flux density to ensure optimal performance. According to previous studies, 1020 steel is a suitable material for this application. However, after further research, we found that DT4 is also a viable alternative. DT4 is also readily available, easy to manufacture, and cost-effective. A comparison between DT4 and 1020 steel is provided in Table 3.
Property
1020 Steel
DT4 (Soft Magnetic Alloy)
Composition
Low-carbon steel (0.18-0.23% C)
High-purity iron
Magnetic Permeability
Moderate
High
Saturation Flux Density
≈ 2.1 T
≈ 2.0 T
Coercivity
Higher
Lower
Electrical Resistivity
10 -7    m
Slightly higher than 1020 steel
Machinability
Good
Moderate
Corrosion Resistance
Low
Low
Cost
Lower
Higher
Table 3. Comparison of 1020 Steel and DT4 Material for Solenoid Plungers
In order to produce the coil with good winding factor in-house, a winding machine was made to facilitate this process, as shown in Figure 5. Additionally, for simpler routing & assembly, the solenoid coil ends are connected to an XT30 ports installed on a PCB. The full model of the kicker is shown in Figure 6, with the upper coil for parallel kicking and lower one for chip kicking. The chip kicking uses a percussion mechanism described in a ZJUNLICT TDP [5]. A preliminary test was done using a boost converter that charges a capacitor array to 90V. This was discharged immediately through a mechanical switch. From the accompanying video submission, the ball can be seen to eject at roughly 3m/s. Please note that in our qualification video, the high-power kicker board responsible for controlling the charging and discharging of the kicking actuation is still under development. As a result, we have used the robot to collide with the ball and push it toward the goal instead. The video of the capacitor array discharge is attached at the end, which should perform effectively the same for our final version [12]. More supplementary media materials will be posted in the future under the same channel.
Fig. 5. Coil winding Machine in use

First Order Robotics Team Description Paper
Fig. 6. Kicker system assembly
3 Hardware
The robot's operation is managed by three primary boards: the main control board, the  kicker  board,  and  a  Raspberry  Pi.  The  main  control  board  communicates  with the  central  computer  via  the  onboard  NRF24  module,  controls  five  BLDC  motors (four for movement and one for dribbling), and processes inputs from various sensors, including infrared sensors, encoders, and a compass. The kicker board is responsible for distributing power across the robot's voltage rails (24V, 5V, and 3.3V) and supplying power to the two kicking solenoids. Finally, the Raspberry Pi is dedicated to handling the camera, which provides additional data to enhance the robot's decision-making capabilities.
3.1 Main Control Board
In  this  year's  iteration,  a  robotics  specific  STM32H723VGT6  development  board  is used for the following reasons:
-The  DM-MC02  -  STM32H723VGT6  development  board  can  be  procured  at  a decent price with very compact physical dimensions.
-The board comes with most of the peripherals needed, such as USART, SPI, CAN ports, saving manpower and costs related to prototyping.
However, a key limitation of this approach is the insufficient number of GPIO pins to meet the robot's requirements. To address this constraint, an additional extension board was designed and stacked above the main board, utilizing the extension BTB port for expanded functionality. Future development will focus on developing a new hardware unit with same MCU that server as a role of a master transmitter, which communicates  between  the  main  decision-making  PC  and  all  6  robots  in  the  field. This board will have features such as a screen and buttons for debugging and status input, and multiple NRF24 and antennas installed.
3.2 Kicker Board
In  the  previous  year,  challenges  arose  in  the  design  of  the  robot's  kicker  due  to  the use of relays for discharging the capacitor bank. Over  time,  the  relay  contacts  experienced wear and tear, leading to reliability issues. In the current iteration, power MOSFETs have been implemented as a more reliable alternative, ensuring faster and more consistent discharge performance.
3.2.1 Capacitor Array The kicker is powered by a capacitor bank consisting of 12 265uF 330V electrolytic capacitors connected in parallel. This configuration provides a theoretical maximum energy of 173J. However, the capacitors are only charged up to 120V, as this voltage is sufficient to propel the ball at the speed limit of 6.5m/s.
3.2.2 Charging Architecture The capacitor bank is charged using the LT3751 high voltage capacitor charger. This chip enables rapid charging, allowing the capacitor  bank  to  fully  charge  in  under  2  seconds,  ensuring  minimal  downtime  between kicks. This is a huge improvement from last year's charging time, allowing for higher frequency of passes and an improved strategy.

M. Liang et al.
Fig. 7. Kicker 2025 Version
Fig. 8. Capacitor Board
3.2.3 Safety and Isolation Given the high voltages involved, the kicker board is designed with safety in mind to protect the user:
-Galvanic Isolation: The board is divided into low and high-voltage sections, which are galvanically isolated to protect the MCUs. Transformers handle power delivery, while optocouplers transmit digital signals. This isolation has proven effective in safeguarding the low power control system, especially during high-power testing.
-Automatic Discharge: To prevent accidental shocks, the capacitor bank automatically discharges through a power resistor when the battery is disconnected.
One limitation of the current design is that the kicker's strength cannot be easily adjusted due to galvanic isolation. Future iterations will incorporate a variable voltage charging mechanism, allowing for adjustable kick strength and greater strategic flexibility in gameplay.
3.3 Wireless Communication
Last year, we selected the NRF24L01 as the RF solution for communication between the controller PC and each bot. A PCB was designed with this chip and its peripherals, with signals output through an on-board PCB antenna. This setup has proven effective, and we continue to use this model this year. Two improvements have been proposed.
-To enhance transmission stability and ensure a secure connection, each NRF24 module is now decoupled from the main control PCB and installed in a dedicated area, making it easier to replace if damaged. Additionally, each module is equipped with a power amplifier, low-noise amplifier, and an SMA antenna connected via an IPEX coaxial cable.
-Each robot is now equipped with two NRF24 modules, with one dedicated solely to receiving (Rx) and the other to transmitting (Tx). This allows for greater communication bandwidth. Although considerable redundancy is reserved for current software development, this setup ensures sufficient data transfer bandwidth in the future.

First Order Robotics Team Description Paper
3.4 Raspberry Pi
Each bot is equipped with a Raspberry Pi 4 that serves as a reserve on-board computing  platform  with  wireless  connectivity.  While  software  development  is  still  in progress, it will eventually suppor