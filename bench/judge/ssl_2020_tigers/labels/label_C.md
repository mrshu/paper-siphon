TIGERs Mannheim
(Team Interacting and Game Evolving Robots)
Extended Team Description for RoboCup 2020

Andre Ryll, Sabolc Jut
Department of Information Technology
Baden-Württemberg Cooperative State University,
Coblitzallee 1-9, 68163 Mannheim, Germany
management@tigers-mannheim.de
https://tigers-mannheim.de

Abstract. This paper presents details of the hardware systems of TIGERs Mannheim, a Small Size League (SSL) team intending to participate in RoboCup 2020 in Bordeaux, France. This year, the ETDP will focus on hardware design for SSL-compatible robots. Weaknesses of previous generations are outlined and changes to mitigate them are discussed in detail. Furthermore, our software implementation of the on-board camera system, used to win the technical challenge 2019, is outlined.

1 Introducing Robot Generation v2020

Fig. 1: CAD rendering of v2020 robot. Cover is shown transparently for a better view on the internals.

The v2020 generation presents our fifth iteration of robots for the RoboCup Small Size League. A CAD rendering of v2020 is shown in figure 1. With 10 years of experience in designing such robots many mistakes were made and many lessons learned. In this paper, we focus on the previous generation (v2019), its strength and weaknesses, and how they are mitigated. The outcome of all fixes is a major overhaul of the powertrain, the dribbler, and kicker. Most of the work went into the powertrain to ensure robust and smooth operation in a competitive environment. More details on the powertrain can be found in section 2.1. The specifications for v2019 and v2020 can be found in table 1. The most prominent change can be seen on the wheel size and powertrain. A comparison of the older v2016 generation with v2019 exists in our previous year TDP [1].

While mechanics have experienced a large update, electronics remain mostly unchanged from v2019 to v2020. They have proven to work well and reliably. The details of the different boards, their purpose, and interconnections are outlined in section 3.

### Table 1: Robot Specifications

| Robot version | v2019 | v2020 |
| :--- | :--- | :--- |
| Dimension | Ø178 x 146mm | Ø178 x 148mm |
| Total weight | 2.5kg | 2.62kg |
| Max. ball coverage | 19.3% | 19.8% |
| Driving motors | Nanotec DF45L024048-A2, 65W¹ | |
| Gear | 30 : 50 | none |
| Gear type | External Spur | Direct Drive |
| Wheel diameter | 33mm | 62mm |
| Encoder | RLS RLC2HD, 36864ppr [2] | iC-PX2604, 23040ppr [3] |
| Dribbling motor | Maxon EXC Speed 13L HP | Moons ECU22048H18, 55W |
| Dribbling gear | 12 : 32 + 14 : 18 | 1 : 1 : 1 |
| ØDribbling bar | 12mm | 11.5mm |
| Kicker charge | 4400µF @ 230V (116.38J) | 3600µF @ 240V (103.68J) |
| Chip kick distance | approx. 3m | approx. 3.6m |
| Straight kick speed | max. 8.5m/s | max. 8.5m/s |
| Microcontroller | STM32H743 [4] | |
| Sensors | Encoders, Gyroscope, Accelerometer, Compass, Camera | |
| Communication link | Semtech SX1280 + FEM @1.3MBit/s, 2.300 - 2.555GHz [5,6] | |
| Compute module | Raspberry Pi 3 with forward oriented camera | |
| Power Supply | Li-Po Battery, 22.2V nominal (6S1P), 1300mAh | |

¹ Alternative option: Maxon EC-45 flat 70W

Fig. 2: Exploded view of major robot modules. Each interchangeable individually. 1) Base plate. 2) Powertrain. 3) Dribbler. 4) Kicking device. 5) Electronics stack. 6) Cover.

2 Mechanical Design

Open-Source TIGERs Mannheim v2020 robot design will be made available as open-source design after the RoboCup World Championship 2020. Sections below omit detailed dimensions for most parts. Please refer to open-source material for all exact dimensions.

Modularity Concept Since v2016 our robots are very modular. This concept has been proven to be very benificial for development and during assembly as well as repair. Each robot has six major modules which can be replaced as a whole. Figure 2 shows an exploded view of these components.

Module #1 is the base plate. Most of the modules (except for the cover) are mounted directly on the base plate and fixed by screws at the bottom. An important detail here is to use screws with countersunk heads. They allow for an alignment of parts on the base plate. Moreover, they ensure that the bottom surface of the robot is as flat as possible, minimizing friction effects. Module #2 is a powertrain with wheel. In the current configuration four wheels are used with a front angle between the robot’s X axis (parallel to the front) and wheel shaft of 31° and a rear angle of 45°.

Module #3 is a dribbler module. It includes the dribbling motor, the dribbling bar, a gear connection between them and electronics for the front break beam to detect the ball. Furthermore, it includes a shovel to translate a linear kick impulse to a rotational impulse for chip kicks. Module #4 is a kicker module. It consists of two rectangular plungers, one for flat kicks and one for chip kicks, two coils, and a capacitor charge PCB with two capacitors.

Module #5 contains the primary electronics stack. That includes a battery, a power board for motor drivers, a mainboard for control, a Raspberry Pi for computer vision algorithms, and a set of auxiliary boards. This module makes extensive use of standard distance bolts to stack the different layers. No custom parts are used here, thus reducing overall cost. Module #6 is a 3D printed cover with standard SSL Vision pattern.

The modules listed above are usually replaced as a whole during a competition to keep time for repairs as low as possible. This allows the team to repair robots not only after a game but already during a game. Experienced team members can replace a dribbler or powertrain unit in less than two minutes. This design allowed us to mostly have the maximum permitted number of robots on the field and have them fully functional.

Manufacturing Methods Some SSL robots have evolved to a highly-intergrated and compact platform for a special purpose. This is only possible with custom parts and their optimization. Commercial Off-The-Shelf (COTS) components usually do not fullfil the strict size requirements of the SSL.

Most components in our robots are manufactured by milling 7075 high-strength aluminum. It offers a low weight and high stiffness at a reasonable price. Some parts without pockets are manufactured via laser cutting. An alternative to laser cutting is using a waterjet, as it is done by other teams [7,8]. Two

parts of our robots are produced by turning, which is the core of the dribbling bar and the subwheel bodies. The previous robot versions v2011, v2013, and v2016 contained custom parts only made by milling and turning.

With v2019 we introduced 3D printing and molding. 3D printing is a common and cheap manufacturing method nowadays. It is well suited for components which would otherwise be difficult to machine (e.g. small dimensions, complex structure, large volumes). However, 3D printed parts are not suited for components experiencing high stress (e.g. impacts). In the v2020 robot design only a few connecting elements and the cover are 3D printed. In contrast to that, other teams have already built most of their robot parts via 3D printing only [9].

Molding was used in the v2019 design for the first time in our robots. It was used to manufacture the dribbling bar with its helix shape. The v2020 design added some molded dampers for the dribbler.

2.1 Powertrain and Wheels

v2019 - 3D Printed Wheels The v2019 wheels were mostly 3D printed with standard PLA material and had a diameter of 33mm. 3D printing is cheap and the small wheels allowed them to be arranged in even 90° spacing between all wheels. This is the optimal configuration for an omni-directional robot as most of the non-linear friction effects linearize themselves.

Although the wheels worked on our test field they suffered heavy damage on the RoboCup 2019 field in Sydney. The result of this can be seen in figure 3. Due to a deep carpet and solidly painted field lines covers of the wheels broke regularly and subwheels were dropped.

![Fig. 3: v2019 robot wheels after RoboCup 2019 in Sydney. Most wheel covers are broken and could not retain their subwheels.](image)

The top cover was fixed to the wheel base by three screws which directly went into holes in the PLA, without an extra thread. Due to constant repairs these holes were overused and no longer able to retain the cover. Occasionally, the cover was then lost and all subwheels were dropped at once. Furthermore, the white silicon O-rings were regularly broken and had to be replaced. As soon as a wheel started to degrade this was a self-amplifying process. A lost subwheel or

O-ring led to direct contact of PLA to the carpet. Heat generated from friction led to melting PLA (PLA gets soft around 60°C) and rendered the wheel non-repairable.

v2020 - Solid Aluminum Wheels
To obtain a more robust solution the 3D printed wheels are replaced by aluminum ones. However, milling wheels with the dimensions of the v2019 wheels is extremely difficult and expensive. Hence, the wheel size was increased. This implies that the ideal 90° spacing cannot be retained. Overall, wheel size was almost doubled compared to v2019 to a total diameter of 62mm.

The optimal wheel size for a SSL robot is always a compromise between multiple factors. Some key factors are: robot top speed, gear ratio, energy consumption, and available space. Most of the time a SSL robot is accelerating, it almost never moves with constant velocity. Hence, it makes sense to optimize the motor operating point for acceleration. This can best be achieved with a reduction gear. It decreases speed, but increases torque at the same energy consumption. This is done in the v2019 powertrain. This robot version can run for approximately two full games with one battery. For the exact endurance of v2020 robots no data is available yet.

To reduce the overall powertrain complexity v2020 robots now use a direct drive, i.e. no gears at all. The wheel is directly attached to the motor shaft. Main drawback of this change is the increased energy consumption. Given the v2019 endurance, this is an acceptable minus. Benefits are a more precise control as there is no backlash due to gears. Furthermore, it theoretically allows higher top speeds.

![Fig. 4: v2020 powertrain. 1) Motor. 2) Shaft adapter. 3) Encoder PCB. 4) Mounting block. 5) Optical encoder disk. 6) Wheel base. 7) Subwheels. 8) Wheel cover. 9) Spring washer. 10) Hex nut.](image)

Figure 4 shows an exploded view of a complete v2020 powertrain. The shaft adapter (item #2) is glued to the motor (item #1) shaft with Loctite 648. It is very important not to machine the motor shaft. Steel dust or chips are attracted by the motor magnets. If they enter the motor its lifetime is significantly reduced.

A small PCB for an optical encoder IC (item #3) is inserted into the mounting block (item #4) which connects to the base plate. On the counterside, a reflective optical encoder disk (item #5) is inserted into the back of the wheel base (item #6).

The integration of the optical encoder directly into the mounting block and wheel make this solution very compact compared to older versions. v2019 robots had magnetic encoders above the wheels, v2016 had optical encoders behind the motors. Both solutions took significantly more space.

**Subwheel Design** Inserted into the wheel base are 20 subwheels (item #7). A wheel cover (item #8) secured with four screws tightens it to the wheel base. Items #5 to #8 form a wheel. The wheel can be removed from the shaft adapter by removing a hex nut (item #10), allowing for fast wheel changes. To ensure the hex nut does not loosen itself from vibrations a spring washer is inserted (item #9).

![Fig. 5: Exploded view of v2020 subwheel. 1) X-Ring. 2) Roller body. 3) Friction bearings. 4) Dowel pin.](image)

The v2020 subwheels are optimized based on experience with previous generations and publications of other teams [10]. Figure 5 shows an exploded view of the subwheels, they consist of four different parts. Item #2 is the subwheel body. Inserted into the body are two friction bearings (item #3) and a dowel pin (item #4) as shaft. Friction bearings are available off-the-shelf from igus$^2$. The bearings are pressed into the body and offer a bearing with very low clearance. The bearing material is shock absorbing and has excellent dry-run capabilities.

An X-Ring is put on the roller body as a connecting element to the carpet to increase friction. X-Rings are superior to O-Rings when it comes to traction, but they have a slightly higher wear. As X-Rings offer two contact points to ground instead of just one like an O-Ring the circular wheel is approximated by 40 contact points, which results in a smooth movement (low vibration, low noise).

These subwheels are similar to v2016 design. However, v2016 did not use a friction bearing, which resulted in higher vibrations and also more wear around the axis. Hence, the center hole was becoming bigger over time, increasing clearance and leading to imprecise control.

$^2$ www.igus.de, type number MSM-0205-02

2.2 Kicker

The kicker module integrates two coils, two plungers, and a capacitor charge PCB. An overview is shown in figure 6. Item #1 is the capacitor charge PCB. One capacitor is hidden for a better view. Details on the charge circuit can be found in section 3.2.

Item #2 is the rear damper of the dribbling device. It has to absorb the impact energy of received balls. It is made of a polyurethane rubber with a shore hardness of 30A$^3$, manufactured using a 3D printed mold. Item #3 indicates location for a pull spring. The spring itself is not shown in the image. The spring is required to pull back the plunger after a kick.

![Fig. 6: v2020 kicker module. 1) Charging PCB with capacitors. 2) Damper for dribbling device. 3) Mount points for pull-back springs. 4) Printed plunger dampers. 5) Ferromagnetic plunger part.](image)

Item #4 is a damper for the plunger. It is 3D printed and made of TPU98. Despite being a relatively hard rubber, it is still flexible enough and robust. Cutouts in the shape allow the dampers to be compressed upon impact on the rear mounting block. A method of damping the plungers is strictly required. Usually, the kick impulse is transferred to the ball and little energy remains to be absorbed. Nevertheless, if the ball is not present during a kick, the complete energy needs to be absorbed by the structure itself. Without a damper the energy would be transferred during a short time frame, resulting in a severe impact. By using a damper, the energy is transferred over a longer time frame. This mitigates structural damage to the rest of the robot.

Item #5 shows the rear part of a plunger, made of ferromagnetic steel$^4$. The steel alloy must be ferromagnetic. This part of the plunger is attracted by a coil made of enameled copper wire with a diameter of 0.63mm. Approximately

$^3$ Smooth-On VytaFlex 30.
$^4$ Usually St37 or C45 low carbon steel

380-450 turns are used on 6-7 layers. A high-voltage, high-current pulse through the coil generates a magnetic field which attracts the plunger. The current flow direction does not matter, the plunger is attracted in all cases.

Half of the plunger is made of steel. The other half is made of aluminum which is not ferromagnetic. The steel part of the plunger is accelerated until it is centered in the coil. After it passes this point, the magnetic field will decelerate it. Hence, a plunger made of steel only would not work. Finding the optimal composition of coil parameters and plunger size as well as position is very difficult and either requires complex simulations or empirical data.

The v2020 kicker design uses a rectangular shaped plunger. It has only one degree of freedom left (moving forward and backward). v2019 used a round bar as plunger. It had one additional (undesired) degree of freedom since it could additionally rotate in place. To prevent this guiding blocks are usually required, which increases mechanical complexity. No deviation in kick strength was noticeable when the shape is changed while the coil cross-section area and number of turns is kept equal.

### 2.3 Dribbler

The dribbler module interacts with the ball and has infrared sensors to detect its presence and position. Figure 7 shows the main components of the dribbler. v2020 uses three gears (item #1) to transfer motor speed to the dribbling bar. All gears are of the same size. Hence, motor speed equals dribbling bar speed. The gear on the motor shaft and on the dribbling bar are made of brass and glued onto the respective components. The middle gear is made of polyketone and is just pushed on two small ball bearings. It is very important to have different materials on mating gears to reduce wear as one part can always yield in such combinations.

The dribbling bar is mounted into a ball bearing on each side. The helix shaped roller (item #6) is molded from polyurethane rubber with a hardness of shore 60A$^5$.

The dribbling motor in v2020 is a brushless motor with 55W and a rated speed of 17000rpm. The dribbling motor is used in short-term overload mode. That implies it is off most of the time but when it is used the rated power is exceeded, leading to heat build up. The winding temperature must not exceed 155$^\circ$C, otherwise the motor is permanently damaged. To monitor heat of the motor a temperature sensor (item #2) has been added to the IR controller PCB (item #4).

Apart from dribbling, the module also has sensing capabilities consisting of infrared diodes (receivers) and emitters. On the sides of the dribbler an emitter and receiver are paired to form a break beam. This is mandatory for a precise kick mechanism. Relying on vision data for this purpose is not precise enough due to the visions capture and transfer delay. The components of the break beam are protected by 3D printed PLA covers (item #5) to prevent damage in

$^5$ Smooth-On VytaFlex 60.

Fig. 7: 