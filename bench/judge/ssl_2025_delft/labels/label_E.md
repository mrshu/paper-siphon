Delft Mercurians Team Description Paper RoboCup 2025<|LOC_257|><|LOC_143|><|LOC_741|><|LOC_143|><|LOC_741|><|LOC_175|><|LOC_257|><|LOC_175|>
The Delft Mercurians  
Delft University of Technology  
Molengraaffsingel 29, 2629 JD Delft, Netherlands  
contact@delftmercurians.nl  
https://delftmercurians.nl/<|LOC_256|><|LOC_232|><|LOC_665|><|LOC_232|><|LOC_665|><|LOC_269|><|LOC_256|><|LOC_269|>
The Delft Mercurians  
Delft University of Technology  
Molengraaffsingel 29, 2629 JD Delft, Netherlands  
contact@delftmercurians.nl  
https://delftmercurians.nl/<|LOC_256|><|LOC_218|><|LOC_665|><|LOC_218|><|LOC_665|><|LOC_269|><|LOC_256|><|LOC_269|>
Abstract. This paper goes over the progress the Delft Mercurians team has made in the past year in terms of robot design and development, to compete in RoboCup Small Sized League division B. The paper presents the hardware, embedded electrical, and software aspects of the robot as well as the research done into smart strategy-making. The future plan for the team is also described.<|LOC_257|><|LOC_351|><|LOC_741|><|LOC_351|><|LOC_741|><|LOC_484|><|LOC_257|><|LOC_484|>
Abstract. This paper goes over the progress the Delft Mercurians team has made in the past year in terms of robot design and development, to compete in RoboCup Small Sized League division B. The paper presents the hardware, embedded electrical, and software aspects of the robot as well as the research done into smart strategy-making. The future plan for the team is also described.<|LOC_257|><|LOC_367|><|LOC_741|><|LOC_367|><|LOC_741|><|LOC_484|><|LOC_257|><|LOC_484|>
1 Introduction<|LOC_256|><|LOC_542|><|LOC_376|><|LOC_542|><|LOC_376|><|LOC_561|><|LOC_256|><|LOC_561|>
Delft Mercurians is a multidisciplinary RoboCup Small Size League team based in Delft, the Netherlands, which debuted in Robocup 2024 and now aims to participate in Robocup 2025 in division B of the Small Size League [1] [2]. The team was founded in September 2022 by members of the Robotics Students Association (RSA) and is made up of robotics enthusiasts and students of the Technical University of Delft. Currently, the team consists of thirty part time members divided into four departments: Hardware, Embestrical, Software and Magic. This paper will outline the integral components that each department has worked on, with an emphasis on describing their innovations.<|LOC_256|><|LOC_644|><|LOC_741|><|LOC_644|><|LOC_741|><|LOC_780|><|LOC_256|><|LOC_780|>
1 Embestrical is a concatenation of the words embedded and electrical. This term was adopted from the Project MARCH Dream Team based in Delft.  
2 The magic department focuses on applying machine-learning to perform smart and adaptive control.<|LOC_256|><|LOC_817|><|LOC_741|><|LOC_817|><|LOC_741|><|LOC_928|><|LOC_256|><|LOC_928|>

2 The Delft Mercurians<|LOC_212|><|LOC_115|><|LOC_418|><|LOC_115|><|LOC_418|><|LOC_128|><|LOC_212|><|LOC_128|>
2 Hardware<|LOC_212|><|LOC_146|><|LOC_347|><|LOC_146|><|LOC_347|><|LOC_161|><|LOC_212|><|LOC_161|>
2.1 Wheels<|LOC_212|><|LOC_191|><|LOC_320|><|LOC_191|><|LOC_320|><|LOC_204|><|LOC_212|><|LOC_204|>
The previous design of the wheels were found to be hard to maintain during the competition due to the difficulty with disassembling the wheel and replacing the sub-wheels.<|LOC_212|><|LOC_230|><|LOC_798|><|LOC_230|><|LOC_798|><|LOC_244|><|LOC_212|><|LOC_244|>
The old wheel design that is suitable for commercial locking assembly for a 4mm shaft would cost a minimum of 1500 euros. Thus, the wheel and sub-wheel attachment was redesigned as seen in Figure 1.<|LOC_212|><|LOC_296|><|LOC_798|><|LOC_296|><|LOC_798|><|LOC_310|><|LOC_212|><|LOC_310|>
The old wheel design that is suitable for commercial locking assembly for a 4mm shaft would cost a minimum of 15000 euros. Thus, the wheel and sub-wheel attachment was redesigned as seen in Figure 1.<|LOC_212|><|LOC_312|><|LOC_798|><|LOC_312|><|LOC_798|><|LOC_326|><|LOC_212|><|LOC_326|>
The old wheel design that is suitable for commercial locking assembly for a 4mm shaft would cost a minimum of 150000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

Delft Mercurians Team Description Paper RoboCup 2025 3<|LOC_348|><|LOC_114|><|LOC_788|><|LOC_114|><|LOC_788|><|LOC_129|><|LOC_348|><|LOC_129|>
(a) Locking Assembly nuts and bolts  
(b) Locking Assembly centerpiece  

Fig. 2: Locking Assembly  

The wheels were mounted to the robot to validate the mechanical boundaries as defined in the competition rules remain respected. They still need to be manufactured and tested, to see how well they drive.  

2.2 Chipper and Dribbler Assembly  

For this year's competition, a full redesign of the dribbler assembly was done, to both improve the overall dribbling capabilities and accommodate the addition of the chipper. The dribbler and chipper assembly can be seen in Figure 3a.  

This new design features a single connection point between the moving section of the dribbler assembly and the mounts on the base-plate. This design choice establishes a well-defined rotation point which allows the dribbler to rotate freely around that pivot point. This is visualized in Figure 3b.  

This design intentionally constrains the dribbler assembly to a single degree of freedom. This means any energy absorbed during impacts or while dribbling is effectively converted to motion around the pivot, and it was decided to make use of a spring to regular the motion and provide the stiffness in this degree of freedom. Said spring is a compliant 3D printed spring. This can be seen in Figure 4 where the deformed and undeformed shape of this spring is shown. This was inspired by the UBC Thunderbots 2023 design [3]. The implementation was significantly altered to create a more robust and less complex system.  

In the conventional approach, the process of getting to the perfect stiffness involves specifying and ordering custom-fabricated springs. This is a process that  

In the conventional approach, the process of getting to the perfect stiffness involves specifying and ordering custom-fabricated springs. This is a process that

4 The Delft Mercurians<|LOC_216|><|LOC_115|><|LOC_418|><|LOC_115|><|LOC_418|><|LOC_127|><|LOC_216|><|LOC_127|>
(a) An isometric view of the current dribbler (b) A side view of the current dribbler design<|LOC_225|><|LOC_338|><|LOC_761|><|LOC_338|><|LOC_761|><|LOC_349|><|LOC_225|><|LOC_349|>
design<|LOC_225|><|LOC_349|><|LOC_271|><|LOC_349|><|LOC_271|><|LOC_359|><|LOC_225|><|LOC_359|>
indicating the degree of freedom<|LOC_502|><|LOC_349|><|LOC_693|><|LOC_349|><|LOC_693|><|LOC_359|><|LOC_502|><|LOC_359|>
Fig. 3: February 2025 dribbler design<|LOC_378|><|LOC_372|><|LOC_625|><|LOC_372|><|LOC_625|><|LOC_385|><|LOC_378|><|LOC_385|>
(a) In tension<|LOC_318|><|LOC_572|><|LOC_400|><|LOC_572|><|LOC_400|><|LOC_583|><|LOC_318|><|LOC_583|>
(b) In compression<|LOC_585|><|LOC_572|><|LOC_697|><|LOC_572|><|LOC_697|><|LOC_583|><|LOC_585|><|LOC_583|>
Fig. 4: Compliant spring deflection example<|LOC_357|><|LOC_596|><|LOC_649|><|LOC_596|><|LOC_649|><|LOC_609|><|LOC_357|><|LOC_609|>
is both expensive and time-consuming in the case of almost all suppliers. This<|LOC_214|><|LOC_644|><|LOC_788|><|LOC_644|><|LOC_788|><|LOC_657|><|LOC_214|><|LOC_657|>
alone hinders rapid, affordable and feasible prototyping and iterative testing.<|LOC_214|><|LOC_659|><|LOC_788|><|LOC_659|><|LOC_788|><|LOC_672|><|LOC_214|><|LOC_672|>
In contrast by making use of the compliant 3D printed spring it is possible to<|LOC_214|><|LOC_674|><|LOC_788|><|LOC_674|><|LOC_788|><|LOC_688|><|LOC_214|><|LOC_688|>
obtain any desired stiffness in a short time.<|LOC_214|><|LOC_690|><|LOC_529|><|LOC_690|><|LOC_529|><|LOC_703|><|LOC_214|><|LOC_703|>
When a new stiffness is desired, the compliant/deformable spring parameters<|LOC_214|><|LOC_720|><|LOC_788|><|LOC_720|><|LOC_788|><|LOC_733|><|LOC_214|><|LOC_733|>
such as the length and width of the compliant/deformable parts of the spring<|LOC_214|><|LOC_735|><|LOC_788|><|LOC_735|><|LOC_788|><|LOC_748|><|LOC_214|><|LOC_748|>
along with its thickness are adjusted. This is then followed by a preliminary<|LOC_214|><|LOC_750|><|LOC_788|><|LOC_750|><|LOC_788|><|LOC_763|><|LOC_214|><|LOC_763|>
finite element analysis (FEM) to validate the design. Eventually, the design is<|LOC_214|><|LOC_765|><|LOC_788|><|LOC_765|><|LOC_788|><|LOC_778|><|LOC_214|><|LOC_778|>
printed which takes less than 10 minutes. This allows for rapid prototyping to<|LOC_214|><|LOC_780|><|LOC_788|><|LOC_780|><|LOC_788|><|LOC_794|><|LOC_214|><|LOC_794|>
find the best stiffness and additionally allows the team to customize the stiffness<|LOC_214|><|LOC_795|><|LOC_788|><|LOC_795|><|LOC_788|><|LOC_808|><|LOC_214|><|LOC_808|>
and rebound of the dribbler to different performance requirements in case of<|LOC_214|><|LOC_810|><|LOC_788|><|LOC_810|><|LOC_788|><|LOC_823|><|LOC_214|><|LOC_823|>
different settings. Additionally, the use of 3D printing allows a wide selection of<|LOC_214|><|LOC_826|><|LOC_788|><|LOC_826|><|LOC_788|><|LOC_839|><|LOC_214|><|LOC_839|>

Delft Mercurians Team Description Paper RoboCup 2025 5<|LOC_206|><|LOC_114|><|LOC_788|><|LOC_114|><|LOC_788|><|LOC_128|><|LOC_206|><|LOC_128|>
materials to further tune the springs rigidity and durability. One of the main<|LOC_206|><|LOC_146|><|LOC_788|><|LOC_146|><|LOC_788|><|LOC_160|><|LOC_206|><|LOC_160|>
contenders for alternate materials at the moment is TPU, as this is known for<|LOC_206|><|LOC_161|><|LOC_788|><|LOC_161|><|LOC_788|><|LOC_175|><|LOC_206|><|LOC_175|>
its elasticity. This new design is being manufactured and tested for competition<|LOC_206|><|LOC_176|><|LOC_788|><|LOC_176|><|LOC_788|><|LOC_191|><|LOC_206|><|LOC_191|>
viability.<|LOC_206|><|LOC_192|><|LOC_279|><|LOC_192|><|LOC_279|><|LOC_206|><|LOC_206|><|LOC_206|>
2.3 Polycarbonate Baseplate<|LOC_206|><|LOC_246|><|LOC_465|><|LOC_246|><|LOC_465|><|LOC_261|><|LOC_206|><|LOC_261|>
The baseplate used in the 2024 and 2025 robots is double layered and made<|LOC_206|><|LOC_284|><|LOC_788|><|LOC_284|><|LOC_788|><|LOC_299|><|LOC_206|><|LOC_299|>
of polycarbonate, a novelty within the competition. This choice was made to<|LOC_206|><|LOC_300|><|LOC_788|><|LOC_300|><|LOC_788|><|LOC_314|><|LOC_206|><|LOC_314|>
accommodate for the required gap in the baseplate to allow the DF45L024048<|LOC_206|><|LOC_315|><|LOC_788|><|LOC_315|><|LOC_788|><|LOC_329|><|LOC_206|><|LOC_329|>
motors to drive the wheels directly. The common solution of a single-layered<|LOC_206|><|LOC_330|><|LOC_788|><|LOC_330|><|LOC_788|><|LOC_344|><|LOC_206|><|LOC_344|>
metal baseplate could not be accommodated, due to the lack of CNC capabilities<|LOC_206|><|LOC_345|><|LOC_788|><|LOC_345|><|LOC_788|><|LOC_359|><|LOC_206|><|LOC_359|>
within the team. The double-layered baseplate, which can be found in figure 5,<|LOC_206|><|LOC_360|><|LOC_788|><|LOC_360|><|LOC_788|><|LOC_374|><|LOC_206|><|LOC_374|>
allowed us to laser cut both 2 mm thick layers separately, with the top layer<|LOC_206|><|LOC_375|><|LOC_788|><|LOC_375|><|LOC_788|><|LOC_390|><|LOC_206|><|LOC_390|>
having additional cuts for the motors, the batteries, the fan and the case, as can<|LOC_206|><|LOC_391|><|LOC_788|><|LOC_391|><|LOC_788|><|LOC_405|><|LOC_206|><|LOC_405|>
be seen in figure 5b.<|LOC_206|><|LOC_406|><|LOC_362|><|LOC_406|><|LOC_362|><|LOC_420|><|LOC_206|><|LOC_420|>
The original design used wood for the baseplate layers. However, the structural<|LOC_206|><|LOC_437|><|LOC_788|><|LOC_437|><|LOC_788|><|LOC_451|><|LOC_206|><|LOC_451|>
integrity and reliability was not sufficient. The most promising alternative found<|LOC_206|><|LOC_452|><|LOC_788|><|LOC_452|><|LOC_788|><|LOC_466|><|LOC_206|><|LOC_466|>
was polycarbonate, which held up extremely well during play tests and the 2024<|LOC_206|><|LOC_467|><|LOC_788|><|LOC_467|><|LOC_788|><|LOC_482|><|LOC_206|><|LOC_482|>
competition in Eindhoven.<|LOC_206|><|LOC_482|><|LOC_405|><|LOC_482|><|LOC_405|><|LOC_496|><|LOC_206|><|LOC_496|>
The 2 plates are held together by the screws on the bottom and the assemblies<|LOC_206|><|LOC_513|><|LOC_788|><|LOC_513|><|LOC_788|><|LOC_527|><|LOC_206|><|LOC_527|>
connected to the baseplate on the top, basically sandwiching the plates together.<|LOC_206|><|LOC_528|><|LOC_788|><|LOC_528|><|LOC_788|><|LOC_542|><|LOC_206|><|LOC_542|>
Thus, if the robot is not assembled, the plates are loose. This is beneficial, since<|LOC_206|><|LOC_543|><|LOC_788|><|LOC_543|><|LOC_788|><|LOC_557|><|LOC_206|><|LOC_557|>
the layers can be replaced separately in case of design updates, or damages. There<|LOC_206|><|LOC_558|><|LOC_788|><|LOC_558|><|LOC_788|><|LOC_572|><|LOC_206|><|LOC_572|>
has been nearly zero damage done on the baseplates during the competition, they<|LOC_206|><|LOC_573|><|LOC_788|><|LOC_573|><|LOC_788|><|LOC_588|><|LOC_206|><|LOC_588|>
held be exceptionally well and can be reused for this year's competition.<|LOC_206|><|LOC_588|><|LOC_736|><|LOC_588|><|LOC_736|><|LOC_602|><|LOC_206|><|LOC_602|>
The polycarbonate does have some downsides. Mainly, the density of the poly-<|LOC_206|><|LOC_619|><|LOC_788|><|LOC_619|><|LOC_788|><|LOC_633|><|LOC_206|><|LOC_633|>
carbonate used is \( 1.21 \, g/cm^3 \), which leads to the center of gravity of the robot.<|LOC_206|><|LOC_634|><|LOC_788|><|LOC_634|><|LOC_788|><|LOC_648|><|LOC_206|><|LOC_648|>
being higher compared to most teams that use a metal base plate. The goal is to<|LOC_206|><|LOC_649|><|LOC_788|><|LOC_649|><|LOC_788|><|LOC_663|><|LOC_206|><|LOC_663|>
to compensate for this through the use of the fan.<|LOC_206|><|LOC_664|><|LOC_576|><|LOC_664|><|LOC_576|><|LOC_678|><|LOC_206|><|LOC_678|>
3 Embedded & Electrical<|LOC_206|><|LOC_719|><|LOC_477|><|LOC_719|><|LOC_477|><|LOC_734|><|LOC_206|><|LOC_734|>
3.1 New motor drivers<|LOC_206|><|LOC_770|><|LOC_418|><|LOC_770|><|LOC_418|><|LOC_783|><|LOC_206|><|LOC_783|>
The team is still using the same B-G431B-ESC1 motor drivers as last year,<|LOC_206|><|LOC_809|><|LOC_788|><|LOC_809|><|LOC_788|><|LOC_823|><|LOC_206|><|LOC_823|>
however the carrier boards have been redesigned.<|LOC_206|><|LOC_824|><|LOC_574|><|LOC_824|><|LOC_574|><|LOC_838|><|LOC_206|><|LOC_838|>

6 The Delft Mercurians<|LOC_216|><|LOC_115|><|LOC_417|><|