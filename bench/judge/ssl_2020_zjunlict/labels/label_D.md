ZJUNlict Extended Team Description Paper for Robocup 2020<|LOC_208|><|LOC_144|><|LOC_788|><|LOC_144|><|LOC_788|><|LOC_169|><|LOC_208|><|LOC_169|>
Zheyuan Huang\(^{1}\), Haodong Zhang\(^{1}\), Dashun Guo\(^{1}\), Shenhan Jia\(^{1}\), Xianze Fang\(^{1}\), Zexi Chen\(^{1}\), Yunkai Wang\(^{1}\), Peng Hu\(^{1}\), Licheng Wen\(^{1}\), Lingyun Chen\(^{1}\), Zhengxi Li\(^{1}\), and Rong Xiong\(^{1}\)<|LOC_236|><|LOC_210|><|LOC_788|><|LOC_210|><|LOC_788|><|LOC_229|><|LOC_236|><|LOC_229|>
Zhejiang University, Zheda Road No.38, Hangzhou, Zhejiang Province, P.R.China

rxiong@zju.edu.cn

http://zjunlict.cn<|LOC_208|><|LOC_266|><|LOC_788|><|LOC_266|><|LOC_788|><|LOC_287|><|LOC_208|><|LOC_287|>
Abstract. ZJUNlict has won the champion of the Small Size League of RoboCup 2019 because of the great effort made in hardware and software. In this paper, we detailedly describe the major improvements that have contributed to our success. In hardware, we optimize our robots' mechanical structure and electronic board for better stability and stronger ball control ability. Also, we increase our robots' control frequency to achieve more accurate and stable control. In software, we develop a dynamic passing strategy and an off-the-ball running module which helps us gain a high possession rate and offensive threat in the game.<|LOC_236|><|LOC_388|><|LOC_788|><|LOC_388|><|LOC_788|><|LOC_410|><|LOC_236|><|LOC_410|>
ZJUNlict has been participating in the Small Size League of RoboCup since 2004. We seek innovation and progress in software and hardware every year, which improves our competitiveness in the game and also brings us the champion of the Small Size League of RoboCup 2019[1]. Our teammates come from different majors and have done excellent work in the software and hardware groups. This paper presents our work and is organized as follows: In Sects.2 and 3, we introduce our main optimization on hardware, including mechanical structure and electronic board. In Sects.4, we described how we increase the robot control frequency to achieve better motion control. In Sects.5 and 6, we discuss the dynamic passing strategy and the off-the-ball running module respectively which helped us gain a ball possession rate\(^{1}\) of 68.8% during 7 matches in RoboCup 2019. In Sect.7, we analyze the performance of our algorithms at RoboCup 2019 with the log files recorded during the matches.<|LOC_208|><|LOC_301|><|LOC_788|><|LOC_301|><|LOC_788|><|LOC_321|><|LOC_208|><|LOC_321|>
Abstract. ZJUNlict has won the champion of the Small Size League of RoboCup 2019 because of the great effort made in hardware and software. In this paper, we detailedly describe the major improvements that have contributed to our success. In hardware, we optimize our robots' mechanical structure and electronic board for better stability and stronger ball control ability. Also, we increase our robots' control frequency to achieve more accurate and stable control. In software, we develop a dynamic passing strategy and an off-the-ball running module which helps us gain a high possession rate and offensive threat in the game.

1 Introduction<|LOC_208|><|LOC_536|><|LOC_376|><|LOC_536|><|LOC_376|><|LOC_554|><|LOC_208|><|LOC_554|>
ZJUNlict has been participating in the Small Size League of RoboCup since 2004. We seek innovation and progress in software and hardware every year, which improves our competitiveness in the game and also brings us the champion of the Small Size League of RoboCup 2019[1]. Our teammates come from different majors and have done excellent work in the software and hardware groups. This paper presents our work and is organized as follows: In Sects.2 and 3, we introduce our main optimization on hardware, including mechanical structure and electronic board. In Sects.4, we described how we increase the robot control frequency to achieve better motion control. In Sects.5 and 6, we discuss the dynamic passing strategy and the off-the-ball running module respectively which helped us gain a ball possession rate\(^{1}\) of 68.8% during 7 matches in RoboCup 2019. In Sect.7, we analyze the performance of our algorithms at RoboCup 2019 with the log files recorded during the matches.<|LOC_208|><|LOC_322|><|LOC_788|><|LOC_322|><|LOC_788|><|LOC_340|><|LOC_208|><|LOC_340|>
The possession rate is calculated by comparing the interception time of both sides. If the interception time of one team is shorter, the ball is considered to be possessed by this team.<|LOC_208|><|LOC_761|><|LOC_788|><|LOC_761|><|LOC_788|><|LOC_777|><|LOC_208|><|LOC_777|>

2 Z. Huang et al.<|LOC_211|><|LOC_115|><|LOC_374|><|LOC_115|><|LOC_374|><|LOC_128|><|LOC_211|><|LOC_128|>
2 Modification of Mechanical Structure of ZJUNlict<|LOC_211|><|LOC_146|><|LOC_736|><|LOC_146|><|LOC_736|><|LOC_161|><|LOC_211|><|LOC_161|>
2.1 The position of two capacitors<|LOC_211|><|LOC_175|><|LOC_511|><|LOC_175|><|LOC_511|><|LOC_189|><|LOC_211|><|LOC_189|>
During a match of the Small Size League, robots could move as fast as \( 3.25 \, m/s \).<|LOC_211|><|LOC_197|><|LOC_788|><|LOC_197|><|LOC_788|><|LOC_211|><|LOC_211|><|LOC_211|>
In this case, the stability of the robot became very important, and this year,<|LOC_211|><|LOC_212|><|LOC_788|><|LOC_212|><|LOC_788|><|LOC_226|><|LOC_211|><|LOC_226|>
we focused on the center of the gravity with a goal of lower it. In fact, there<|LOC_211|><|LOC_227|><|LOC_788|><|LOC_227|><|LOC_788|><|LOC_241|><|LOC_211|><|LOC_241|>
are already many teams got there hands busy with lowering the center of the<|LOC_211|><|LOC_242|><|LOC_788|><|LOC_242|><|LOC_788|><|LOC_256|><|LOC_211|><|LOC_256|>
gravity, eg, team KIKS and team RoboDragons have their robot compacted<|LOC_211|><|LOC_257|><|LOC_788|><|LOC_257|><|LOC_788|><|LOC_271|><|LOC_211|><|LOC_271|>
to \( 135 \, mm \), and team TIGERs have their capacitor moved sideways instead of<|LOC_211|><|LOC_272|><|LOC_789|><|LOC_272|><|LOC_789|><|LOC_286|><|LOC_211|><|LOC_286|>
regularly laying upon the solenoid [2].<|LOC_211|><|LOC_287|><|LOC_489|><|LOC_287|><|LOC_489|><|LOC_302|><|LOC_211|><|LOC_302|>
Thanks to the open source of team TIGERs [2], in this year's mechanical<|LOC_230|><|LOC_303|><|LOC_788|><|LOC_303|><|LOC_788|><|LOC_317|><|LOC_230|><|LOC_317|>
structure design, we moved the capacitor from the circuit board to the chassis.<|LOC_211|><|LOC_318|><|LOC_787|><|LOC_318|><|LOC_787|><|LOC_332|><|LOC_211|><|LOC_332|>
On the one hand, this lowers the center of gravity of the robot and makes the<|LOC_211|><|LOC_333|><|LOC_788|><|LOC_333|><|LOC_788|><|LOC_347|><|LOC_211|><|LOC_347|>
mechanical structure of the robot more compact. On the other hand, to give the<|LOC_211|><|LOC_348|><|LOC_788|><|LOC_348|><|LOC_788|><|LOC_362|><|LOC_211|><|LOC_362|>
upper board a larger space for future upgrades. The capacitor is fixed on the<|LOC_211|><|LOC_363|><|LOC_788|><|LOC_363|><|LOC_788|><|LOC_377|><|LOC_211|><|LOC_377|>
chassis via the 3D printed capacitor holder as shown in Figure 1, and in order to<|LOC_211|><|LOC_378|><|LOC_788|><|LOC_378|><|LOC_788|><|LOC_392|><|LOC_211|><|LOC_392|>
protect the capacitor from the impact that may be suffered on the field, we have<|LOC_211|><|LOC_393|><|LOC_788|><|LOC_393|><|LOC_788|><|LOC_407|><|LOC_211|><|LOC_407|>
added a metal protection board on the outside of the capacitor which made of<|LOC_211|><|LOC_408|><|LOC_789|><|LOC_408|><|LOC_789|><|LOC_422|><|LOC_211|><|LOC_422|>
40Cr alloy steel with high strength.<|LOC_211|><|LOC_423|><|LOC_471|><|LOC_423|><|LOC_471|><|LOC_437|><|LOC_211|><|LOC_437|>
Fig. 1: The new design of the capacitors<|LOC_358|><|LOC_597|><|LOC_647|><|LOC_597|><|LOC_647|><|LOC_611|><|LOC_358|><|LOC_611|>
2.2 The structure of the dribbling system<|LOC_211|><|LOC_667|><|LOC_570|><|LOC_667|><|LOC_570|><|LOC_681|><|LOC_211|><|LOC_681|>
The handling of the dribbling part has always been a part we are proud of, and<|LOC_211|><|LOC_687|><|LOC_788|><|LOC_687|><|LOC_788|><|LOC_701|><|LOC_211|><|LOC_701|>
it is also the key to our strong ball control ability. In last year's champion paper,<|LOC_211|><|LOC_702|><|LOC_788|><|LOC_702|><|LOC_788|><|LOC_716|><|LOC_211|><|LOC_716|>
we have completely described our design concept, that is, using a one-degree-of-<|LOC_211|><|LOC_717|><|LOC_788|><|LOC_717|><|LOC_788|><|LOC_731|><|LOC_211|><|LOC_731|>
freedom mouth structure, placing appropriate sponge pads on the rear and the<|LOC_211|><|LOC_732|><|LOC_788|><|LOC_732|><|LOC_788|><|LOC_746|><|LOC_211|><|LOC_746|>
lower part to form a nonlinear spring damping system. When a ball with certain<|LOC_211|><|LOC_747|><|LOC_788|><|LOC_747|><|LOC_788|><|LOC_761|><|LOC_211|><|LOC_761|>
speed hits the dribbler, the spring damping system can absorb the rebound force<|LOC_211|><|LOC_762|><|LOC_788|><|LOC_762|><|LOC_788|><|LOC_776|><|LOC_211|><|LOC_776|>
of the ball, and the dribbler uses a silica gel with a large friction force so that<|LOC_211|><|LOC_777|><|LOC_788|><|LOC_777|><|LOC_788|><|LOC_791|><|LOC_211|><|LOC_791|>
the ball can not be easily detached from the mouth.<|LOC_211|><|LOC_792|><|LOC_592|><|LOC_792|><|LOC_592|><|LOC_806|><|LOC_211|><|LOC_806|>
The state of the sponge behind the mouth is critical to the performance of the<|LOC_230|><|LOC_808|><|LOC_788|><|LOC_808|><|LOC_788|><|LOC_822|><|LOC_230|><|LOC_822|>
dribbling system. In RoboCup 2018, there was a situation in which the sponge<|LOC_211|><|LOC_823|><|LOC_788|><|LOC_823|><|LOC_788|><|LOC_837|><|LOC_211|><|LOC_837|>

ZJUNlict Extended Team Description Paper for Robocup 2020 3<|LOC_0|><|LOC_110|><|LOC_791|><|LOC_110|><|LOC_791|><|LOC_127|><|LOC_0|><|LOC_127|>
fell off, which had a great impact on the play of our game. In last year's design,<|LOC_0|><|LOC_142|><|LOC_790|><|LOC_142|><|LOC_790|><|LOC_160|><|LOC_0|><|LOC_160|>
as shown in Figure 2, we directly insert a sponge between the carbon plate at<|LOC_0|><|LOC_158|><|LOC_790|><|LOC_158|><|LOC_790|><|LOC_175|><|LOC_0|><|LOC_175|>
the mouth and the rear carbon plate. Under frequent and severe vibration, the<|LOC_0|><|LOC_173|><|LOC_790|><|LOC_173|><|LOC_790|><|LOC_191|><|LOC_0|><|LOC_191|>
sponge could easily be filled off[3]. In this case, we made some changes, a baffle is<|LOC_0|><|LOC_189|><|LOC_790|><|LOC_189|><|LOC_790|><|LOC_207|><|LOC_0|><|LOC_207|>
added between the dibbler and the rear carbon fiberboard, as shown in figure 3,<|LOC_0|><|LOC_204|><|LOC_790|><|LOC_204|><|LOC_790|><|LOC_222|><|LOC_0|><|LOC_222|>
and the sponge is glued to the baffle plate, which made it hard for the sponge<|LOC_0|><|LOC_220|><|LOC_790|><|LOC_220|><|LOC_790|><|LOC_238|><|LOC_0|><|LOC_238|>
to fall off, therefore greatly reduce the vibration.<|LOC_0|><|LOC_236|><|LOC_570|><|LOC_236|><|LOC_570|><|LOC_253|><|LOC_0|><|LOC_253|>
Fig. 2: ZJUNlict 2018 mouth design Fig. 3: ZJUNlict 2019 mouth design<|LOC_232|><|LOC_421|><|LOC_770|><|LOC_421|><|LOC_770|><|LOC_438|><|LOC_232|><|LOC_438|>
3 Modification of Electronic Board<|LOC_212|><|LOC_492|><|LOC_571|><|LOC_492|><|LOC_571|><|LOC_509|><|LOC_212|><|LOC_509|>
In the past circuit design, we always thought that the board should be designed<|LOC_0|><|LOC_522|><|LOC_790|><|LOC_522|><|LOC_790|><|LOC_540|><|LOC_0|><|LOC_540|>
into multiple independent boards according to the function module so that if<|LOC_0|><|LOC_538|><|LOC_790|><|LOC_538|><|LOC_790|><|LOC_555|><|LOC_0|><|LOC_555|>
there is a problem, the whole board can be replaced. But then we gradually<|LOC_0|><|LOC_553|><|LOC_790|><|LOC_553|><|LOC_790|><|LOC_570|><|LOC_0|><|LOC_570|>
realized that instead of giving us convenience, it is unexpectedly complicated,<|LOC_0|><|LOC_568|><|LOC_790|><|LOC_568|><|LOC_790|><|LOC_586|><|LOC_0|><|LOC_586|>
on the one hand, we had to carry more spare boards, and on the other hand, it<|LOC_0|><|LOC_583|><|LOC_790|><|LOC_583|><|LOC_790|><|LOC_601|><|LOC_0|><|LOC_601|>
was not conducive to our maintenance.<|LOC_0|><|LOC_599|><|LOC_499|><|LOC_599|><|LOC_499|><|LOC_617|><|LOC_0|><|LOC_617|>
3.1 The new motherboard design<|LOC_212|><|LOC_637|><|LOC_504|><|LOC_637|><|LOC_504|><|LOC_653|><|LOC_212|><|LOC_653|>
For the new design, we only kept one motherboard and one booster board, which<|LOC_0|><|LOC_661|><|LOC_790|><|LOC_661|><|LOC_790|><|LOC_679|><|LOC_0|><|LOC_679|>
reduced the number of boards, making the circuit structure more compact and<|LOC_0|><|LOC_677|><|LOC_790|><|LOC_677|><|LOC_790|><|LOC_694|><|LOC_0|><|LOC_694|>
more convenient for maintenance. We also fully adopted ST's STM32H743ZI<|LOC_0|><|LOC_692|><|LOC_790|><|LOC_692|><|LOC_790|><|LOC_709|><|LOC_0|><|LOC_709|>
master chip, which has a clock speed of up to 480MHz and has a wealth of<|LOC_0|><|LOC_707|><|LOC_790|><|LOC_707|><|LOC_790|><|LOC_725|><|LOC_0|><|LOC_725|>
peripherals. The chip is responsible for signal processing, packet unpacking and<|LOC_0|><|LOC_723|><|LOC_790|><|LOC_723|><|LOC_790|><|LOC_741|><|LOC_0|><|LOC_741|>
packaging, and motor control.<|LOC_0|><|LOC_739|><|LOC_434|><|LOC_739|><|LOC_434|><|LOC_756|><|LOC_0|><|LOC_756|>
Thanks to the open source of TIGERs again, we use Allergo's A3930 three-<|LOC_232|><|LOC_755|><|LOC_790|><|LOC_755|><|LOC_790|><|LOC_772|><|LOC_232|><|LOC_772|>
phase brushless motor control chip, simplifying the circuit design of the motor<|LOC_0|><|LOC_771|><|LOC_790|><|LOC_771|><|LOC_790|><|LOC_788|><|LOC_0|><|LOC_788|>
drive module on the motherboard. The biggest advancement in electronic this<|LOC_0|><|LOC_786|><|LOC_790|><|LOC_786|><|LOC_790|><|LOC_803|><|LOC_0|><|LOC_803|>
year was the completion of the stability test of the H743 version of the robot.<|LOC_0|><|LOC_801|><|LOC_790|><|LOC_801|><|LOC_790|><|LOC_819|><|LOC_0|><|LOC_819|>
In the case of all robots using the H743 chip, there was no robot failure caused<|LOC_0|><|LOC_817|><|LOC_790|><|LOC_817|><|LOC_790|><|LOC_835|><|LOC_0|><|LOC_835|>
by board damage during the game. In addition, we replaced the motor encoder<|LOC_0|><|LOC_833|><|LOC_790|><|LOC_833|><|LOC_790|><|LOC_851|><|LOC_0|><|LOC_851|>

4 Z. Huang et al.<|LOC_211|><|LOC_115|><|LOC_374|><|LOC_115|><|LOC_374|><|LOC_128|><|LOC_211|><|LOC_128|>
from the original 360 lines to the current 1000 lines. The reading mode has been<|LOC_211|><|LOC_147|><|LOC_793|><|LOC_147|><|LOC_793|><|LOC_161|><|LOC_211|><|LOC_161|>
changed from the original direct reading to the current differential mode reading.<|LOC_211|><|LOC_162|><|LOC_792|><|LOC_162|><|LOC_792|><|LOC_177|><|LOC_211|><|LOC_177|>
3.2 The new attitude transducer: IMU<|LOC_211|><|LOC_197|><|LOC_549|><|LOC_197|><|LOC_549|><|LOC_211|><|LOC_211|><|LOC_211|>
To increase the motion performance of our robot, we add an IMU on our mother-<|LOC_211|><|LOC_219|><|LOC_793|><|LOC_219|><|LOC_793|><|LOC_233|><|LOC_211|><|LOC_233|>
board. The IMU can measure the acceleration in three directions and the angular<|LOC_211|><|LOC_233|><|LOC_793|><|LOC_233|><|LOC_793|><|LOC_248|><|LOC_211|><|LOC_248|>
velocity of the robot. Then it calculates the angular velocity integral and gets<|LOC_211|><|LOC_248|><|LOC_793|><|LOC_248|><|LOC_793|><|LOC_263|><|LOC_211|><|LOC_263|>
the real time heading angel. It is a MEMS device and can be put on the PCB.<|LOC_211|><|LOC_263|><|LOC_792|><|LOC_263|><|LOC_792|><|LOC_278|><|LOC_211|><|LOC_278|>
To ensure the stability of the measurements of the angular velocity we tested the<|LOC_211|><|LOC_278|><|LOC_793|><|LOC_278|><|LOC_793|><|LOC_293|><|LOC_211|><|LOC_293|>
IMU and got a satisfying result. The temperature drift and the time drift are<|LOC_211|><|LOC_293|><|LOC_793|><|LOC_293|><|LOC_793|><|LOC_308|><|LOC_211|><|LOC_308|>
low. We put the robot on the level ground and let it stay static. The deviation<|LOC_211|><|LOC_308|><|LOC_793|><|LOC_308|><|LOC_793|><|LOC_323|><|LOC_211|><|LOC_323|>
of the heading angel in 5 minutes is less than 0.5 degree.<|LOC_211|><|LOC_323|><|LOC_626|><|LOC_323|><|LOC_626|><|LOC_338|><|LOC_211|><|LOC_338|>
With the real time heading angel data got, we can control the heading angel.<|LOC_242|><|LOC_338|><|LOC_793|><|LOC_338|><|LOC_793|><|LOC_353|><|LOC_242|><|LOC_353|>
in the lower computer and increase both the control frequency and the accuracy.<|LOC_211|><|LOC_353|><|LOC_793|><|LOC_353|><|LOC_793|><|LOC_368|><|LOC_211|><|LOC_368|>
This will be further discussed in Sects.4.<|LOC_211|><|LOC_368|><|LOC_506|><|LOC_368|><|LOC_506|><|LOC_383|><|LOC_211|><|LOC_383|>
4 Increase the Control Frequency<|LOC_211|><|LOC_404|><|LOC_556|><|LOC_404|><|LOC_556|><|LOC_422|><|LOC_211|><|LOC_422|>
On our research platform, ZJUNlict small size soccer team, the frequency of the<|LOC_211|><|LOC_432|><|LOC_793|><|LOC_432|><|LOC_793|><|LOC_446|><|LOC_211|><|LOC_446|>
global vision system is 75 Hz, which determines the frequency of coordination<|LOC_211|><|LOC_446|><|LOC_793|><|LOC_446|><|LOC_793|><|LOC_461|><|LOC_211|><|LOC_461|>
decision, motion planning and other control instructions.<|LOC_211|><|LOC_461|><|LOC_626|><|LOC_461|><|LOC_626|><|LOC_476|><|LOC_211|><|LOC_476|>
As Figure 4 shows, after obtaining the target position and target orientation.<|LOC_242|><|LOC_476|><|LOC_793|><|LOC_476|><|LOC_793|><|LOC_491|><|LOC_242|><|LOC_491|>
from the strategy layer (only the target orientation is concerned here), the motion<|LOC_211|><|LOC_491|><|LOC_793|><|LOC_491|><|LOC_793|><|LOC_506|><|LOC_211|><|LOC_506|>
planner plans next step according to the current orientation and speed obtained<|LOC_211|><|LOC_506|><|LOC_793|><|LOC_506|><|LOC_793|><|LOC_521|><|LOC_211|><|LOC_521|>
from the global visual system, and then sends the next speed instructions to the<|LOC_211|><|LOC_521|><|LOC_793|><|LOC_521|><|LOC_793|><|LOC_536|><|LOC_211|><|LOC_536|>
robot.<|LOC_211|><|LOC_536|><|LOC_261|><|LOC_536|><|LOC_261|><|LOC_549|><|LOC_211|><|LOC_549|>
Decision layer + Motion planner + Communication protocol + Robots + Global vision system + Network system + Data system + Communication protocol + Robots + Local vision system + Motion plan + Global vision system + Network system + Data system + Control system + Global vision system + Control system + Network system + Control system + Control system + Co