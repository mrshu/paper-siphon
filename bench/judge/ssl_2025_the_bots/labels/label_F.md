2025 Team Description Paper: The Bots<|LOC_223|><|LOC_142|><|LOC_732|><|LOC_142|><|LOC_732|><|LOC_162|><|LOC_223|><|LOC_162|>
Mathew MacDougall, Henry Bryant, Akhil Veeraghanta, Vikram Bhat, Ashley Lee, and Steven Guido<|LOC_219|><|LOC_199|><|LOC_783|><|LOC_199|><|LOC_783|><|LOC_214|><|LOC_219|><|LOC_214|>
Lee, and Steven Guido<|LOC_418|><|LOC_216|><|LOC_586|><|LOC_216|><|LOC_586|><|LOC_229|><|LOC_418|><|LOC_229|>
thebots.robocup@gmail.com<|LOC_410|><|LOC_243|><|LOC_596|><|LOC_243|><|LOC_596|><|LOC_256|><|LOC_410|><|LOC_256|>
github.com/sfunderbots<|LOC_410|><|LOC_258|><|LOC_586|><|LOC_258|><|LOC_586|><|LOC_270|><|LOC_410|><|LOC_270|>
cad.onshape.com/documents/f50de4495ca6813b0d6d1926<|LOC_310|><|LOC_272|><|LOC_691|><|LOC_272|><|LOC_691|><|LOC_285|><|LOC_310|><|LOC_285|>
Abstract. This paper details the design and development of the systems of The Bots, a Small Size League team intending to compete in RoboCup 2025 in Salvador, Brazil. As well as improving the modular low-cost design from last year, we introduce safety features for our chicken board, and vision filter improvements.<|LOC_261|><|LOC_318|><|LOC_783|><|LOC_318|><|LOC_783|><|LOC_331|><|LOC_261|><|LOC_331|>
Keywords: RoboCup 2025 · Small Size League · Robotic Soccer · Ball Filter<|LOC_261|><|LOC_393|><|LOC_743|><|LOC_393|><|LOC_743|><|LOC_407|><|LOC_261|><|LOC_407|>
Fig. 1: CAD of Generation 2 Robot. Shell and faceplate are transparent for internal view.<|LOC_216|><|LOC_741|><|LOC_788|><|LOC_741|><|LOC_788|><|LOC_755|><|LOC_216|><|LOC_755|>

2 M. Macdougall, H. Bryant, A. Veeraghanta et al.

1 Introduction

The Bots is an interdisciplinary team composed of university graduates who were formerly part of the UBC Thunderbots Design Team, as well as having recruited graduates from other Universities in the USA. Established in 2022 after RoboCup in Bangkok, Thailand, the team is now pursuing its first competitive action (after withdrawing from the 2024 competition) within the Small Size League seeking qualification for RoboCup 2025. One of the barriers of entry into the league is the development cost. The Bots has come up with a cost-optimized design, describing multiple optimizations for the league. As our mechanical systems have generally stayed consistent with last year, this paper outlines The Bots' progress in developing the electrical and software systems of these robots to compete in RoboCup 2025.

The Bots is an interdisciplinary team composed of university graduates who were formerly part of the UBC Thunderbots Design Team, as well as having recruited graduates from other Universities in the USA. Established in 2022 after RoboCup in Bangkok, Thailand, the team is now pursuing its first competitive action (after withdrawing from the 2024 competition) within the Small Size League seeking qualification for RoboCup 2025. One of the barriers of entry into the league is the development cost. The Bots has come up with a cost-optimized design, describing multiple optimizations for the league. As our mechanical systems have generally stayed consistent with last year, this paper outlines The Bots' progress in developing the electrical and software systems of these robots to compete in RoboCup 2025.

2025 Team Description Paper: The Bots 3<|LOC_466|><|LOC_115|><|LOC_788|><|LOC_115|><|LOC_788|><|LOC_127|><|LOC_466|><|LOC_127|>
2 Electrical<|LOC_216|><|LOC_145|><|LOC_344|><|LOC_145|><|LOC_344|><|LOC_159|><|LOC_216|><|LOC_159|>
2.1 Electrical System Overview<|LOC_216|><|LOC_169|><|LOC_487|><|LOC_169|><|LOC_487|><|LOC_182|><|LOC_216|><|LOC_182|>
Since a large part of the electrical system was developed in the previous year, our<|LOC_216|><|LOC_186|><|LOC_788|><|LOC_186|><|LOC_788|><|LOC_199|><|LOC_216|><|LOC_199|>
main focus for this year has been the integration of the electrical and mechanical<|LOC_216|><|LOC_201|><|LOC_788|><|LOC_201|><|LOC_788|><|LOC_214|><|LOC_216|><|LOC_214|>
systems, on the robot itself rather than in design. All of our board projects[9],<|LOC_216|><|LOC_216|><|LOC_788|><|LOC_216|><|LOC_788|><|LOC_230|><|LOC_216|><|LOC_230|>
have been integrated into our working robots, with our 30 dollar motor drivers<|LOC_216|><|LOC_231|><|LOC_788|><|LOC_231|><|LOC_788|><|LOC_244|><|LOC_216|><|LOC_244|>
being the key integration to lower the cost of our robot, adhering to our $500<|LOC_216|><|LOC_246|><|LOC_788|><|LOC_246|><|LOC_788|><|LOC_259|><|LOC_216|><|LOC_259|>
budget per robot we set last year. Besides the integration, there have been some<|LOC_216|><|LOC_261|><|LOC_788|><|LOC_261|><|LOC_788|><|LOC_274|><|LOC_216|><|LOC_274|>
improvements and new additions to the design of our electrical stackup this year,<|LOC_216|><|LOC_276|><|LOC_788|><|LOC_276|><|LOC_788|><|LOC_289|><|LOC_216|><|LOC_289|>
including a simple breakbeam design using off-the-shelf components, and improv-<|LOC_216|><|LOC_291|><|LOC_788|><|LOC_291|><|LOC_788|><|LOC_304|><|LOC_216|><|LOC_304|>
ing the robustness for the chicker board. There are other minor improvements<|LOC_216|><|LOC_306|><|LOC_788|><|LOC_306|><|LOC_788|><|LOC_319|><|LOC_216|><|LOC_319|>
and validations, which will be covered in the following sections.<|LOC_216|><|LOC_321|><|LOC_672|><|LOC_321|><|LOC_672|><|LOC_334|><|LOC_216|><|LOC_334|>
2.2 Chicker Board<|LOC_216|><|LOC_347|><|LOC_382|><|LOC_347|><|LOC_382|><|LOC_360|><|LOC_216|><|LOC_360|>
While testing the chicker board V1.0 last year, we encountered voltage spikes,<|LOC_216|><|LOC_367|><|LOC_788|><|LOC_367|><|LOC_788|><|LOC_381|><|LOC_216|><|LOC_381|>
over-current issues, as well as flyback charging sensitivity. These issues and so-<|LOC_216|><|LOC_382|><|LOC_788|><|LOC_382|><|LOC_788|><|LOC_395|><|LOC_216|><|LOC_395|>
solutions will be discussed in the following sections.<|LOC_216|><|LOC_397|><|LOC_572|><|LOC_397|><|LOC_572|><|LOC_410|><|LOC_216|><|LOC_410|>
Power Input Protections<|LOC_216|><|LOC_420|><|LOC_422|><|LOC_420|><|LOC_422|><|LOC_433|><|LOC_216|><|LOC_433|>
During testing last year, we saw a 40V spike travel to the board from a faulty<|LOC_216|><|LOC_435|><|LOC_788|><|LOC_435|><|LOC_788|><|LOC_448|><|LOC_216|><|LOC_448|>
power supply, shown in figure 2.1. This would prove that the input to the chicker<|LOC_216|><|LOC_450|><|LOC_788|><|LOC_450|><|LOC_788|><|LOC_463|><|LOC_216|><|LOC_463|>
board is not protected from voltage spikes. Since the chicker board is designed<|LOC_216|><|LOC_464|><|LOC_788|><|LOC_464|><|LOC_788|><|LOC_478|><|LOC_216|><|LOC_478|>
to run hand-in-hand with the midplate we designed, this should not be an issue<|LOC_216|><|LOC_479|><|LOC_788|><|LOC_479|><|LOC_788|><|LOC_492|><|LOC_216|><|LOC_492|>
in realistic testing scenarios. However, this voltage spike could be mitigated by<|LOC_216|><|LOC_494|><|LOC_788|><|LOC_494|><|LOC_788|><|LOC_507|><|LOC_216|><|LOC_507|>
adding a TVS diode to clamp the voltage if we are testing without the midplate.<|LOC_216|><|LOC_509|><|LOC_788|><|LOC_509|><|LOC_788|><|LOC_522|><|LOC_216|><|LOC_522|>
Stop<|LOC_476|><|LOC_547|><|LOC_499|><|LOC_547|><|LOC_499|><|LOC_557|><|LOC_476|><|LOC_557|>
M Pos: 2.880s<|LOC_562|><|LOC_545|><|LOC_646|><|LOC_545|><|LOC_646|><|LOC_557|><|LOC_562|><|LOC_557|>
CH1 10.0V<|LOC_320|><|LOC_788|><|LOC_384|><|LOC_788|><|LOC_384|><|LOC_800|><|LOC_320|><|LOC_800|>
M 2.50s<|LOC_500|><|LOC_788|><|LOC_546|><|LOC_788|><|LOC_546|><|LOC_799|><|LOC_500|><|LOC_799|>
CH1 7<|LOC_636|><|LOC_788|><|LOC_678|><|LOC_788|><|LOC_678|><|LOC_800|><|LOC_636|><|LOC_800|>
25-Mar-24 18:06<|LOC_500|><|LOC_800|><|LOC_603|><|LOC_800|><|LOC_603|><|LOC_810|><|LOC_500|><|LOC_810|>
Fig. 2.1: Power Input Voltage Spike<|LOC_373|><|LOC_821|><|LOC_629|><|LOC_821|><|LOC_629|><|LOC_835|><|LOC_373|><|LOC_835|>

4 M. Macdougall, H. Bryant, A. Veeraghanta et al.
Since this issue (above) showed up when trying to recreate an issue where gate driver chip would burn up from seemingly no outside interaction. There are two possibilities: one is caused from charging while kicking and the flyback transient energy, and the other due to the faulty power supply. In the test, the battery was plugged in while the logic level circuits were already functioning which caused the gate driver chip to burn up.
While it is generally not a good idea to send a charge cycle at the same time as a kick, we think this is not the cause of the problem; however it is a possibility that the transient energy from simply charging the high voltage rail could disrupt the chip operation. When a charge cycle is started, there is a large transfer of transient energy that can impact the voltage of the battery (see figure 2.1 between the 3rd and 4th grid intersection) since it draws large amounts of current. Having a tuned RCD snubber could help dissipate the excess energy due to leakage inductance and other factors, but including a 12V DC/DC converter would also likely help (this was cut due to size constraints). This was solved through the power board firmware to never charge when kicking and vice versa, but will hopefully be solved in hardware in the future.
The other likely cause of this problem (and maybe the more likely cause) is that the faulty power supply used in the test above was the culprit for this issue, which could have caused a smaller overvoltage condition (one that was not noticed, just barely exceeding the chip's ratings[2] of 20V), which would have been caused the chip to burn.
Logic Protections
Likewise, the logic level signals to the RP2040 are not protected from voltage and current spikes. For example, in the event of a long or non-deterministic pulse width sent to the gate driver, the IGBT would break from drawing too much current sent through the solenoid. Due to this large draw of power, the gate driver can pull too much current from the microcontroller, and break the pins connected. To solve the logic signal pins getting damaged we added 3v3 Zener diodes [1] to protect the logic level circuits, including: KICK, CHIP, BKBM, 5V_LEVEL, BATT_LEVEL (and any other important feedback pins).
Flyback Circuit Protections
There has been a long time to fix this problem. There has been a long time to fix this problem. There has been a long time to fix this problem.
There has been a long time to fix this problem.
In the datasheet for the LT3751[4] they mentioned that the primary inductance and the output voltage are intricately linked (page 16), and if this relationship is not met, the system will cause the system to be�ed.

2025 Team Description Paper: The Bots 5<|LOC_0|><|LOC_0|><|LOC_999|><|LOC_0|><|LOC_999|><|LOC_999|><|LOC_0|><|LOC_999|>
is not met (or if the inductance changes significantly) it could cause a runaway condition and it would overcharge the output capacitor. This follows by saying that the flyback charging design relies on having a low leakage inductance path, but will still work in “adequate” conditions. With the increase in temperature, this may well cause an increase in leakage current and possibly change the leakage inductance of the board, which would cause either thermal or voltage runaway depending on what was the cause.<|LOC_0|><|LOC_0|><|LOC_999|><|LOC_0|><|LOC_999|><|LOC_999|><|LOC_0|><|LOC_999|>
As the caps on UBC Thunderbots Power board (and ours) are rated for 250V, the safety margin is only about 3% since their power board charges up to 240V. Ideally, the voltage rating margin should be at least 25% above the maximum voltage. In this light, we decided to use 200V as our maximum, which should easily be able to achieve the same outcome in kick speed. This will eventually be modelled in simulation to verify if we are to achieve this, but we should be able to do real world tests by changing a single resistor. Changing R-out to 40.4k will make sure the output voltage charges to only $\approx$ 200V (using the same equation as last year[9]).<|LOC_0|><|LOC_0|><|LOC_999|><|LOC_0|><|LOC_999|><|LOC_999|><|LOC_0|><|LOC_999|>

6 M. Macdougall, H. Bryant, A. Veeraghanta et al.
3 Software
3.1 Vision Filter Test Suite
Accurate vision filters are essential for accurately estimating the state of the ball and robots, which in turn leads to more consistent gameplay performance.
With sufficient field space and a camera setup, tests can be done manually.
While the results will be representative of reality, the downside is that doing these tests in-person is time-consuming and not always consistent. Furthermore, there is no ground-truth data to compare against so evaluating the results is empirical. On the other hand, synthetic test data can be generated by creating ground-truth data and applying noise similar to SSL Vision. This test data can be used to create unit tests for the vision filters that are fast and repeatable.
However, it is difficult to manually create test data that accurately captures the more complicated interactions between the ball and robots for more advanced test cases, resulting in gaps in test coverage. An example of a scenario that is difficult to model manually is how a high-speed ball bounces off a robot, or how the ball moves when being dribbled.
To address the shortcomings of these testing options, we have created a solution that combines the best of both. The fundamental idea is that we use a simulator to accurately model our testing scenarios, and use the simulator to output both ground-truth data and raw vision data. We log the data so it can be stored in our GitHub repo and loaded for each individual unit test. The raw data is fed into our filters, and the output is compared against the ground truth data to generate metrics on the filter error. Our tests assert the error values are below acceptable thresholds, and also generate plots showing the raw data, filtered data, and ground truth data. The assertions ensure that we do not accidentally regress the filters while developing or making changes, and the plots are indispensable for empirical validation and debugging. Examples of our error metrics are shown in figure 1, and example plots are shown in figure 3.1.
Technical Details We modified the Er-Force simulator to output the internal simulation state, which we use as ground-truth data, using the SSL Vision TrackerWrapperPacket. This effectively makes the simulator also act as a Tracker implementation, which is useful both for generating test data and running our AI with "perfect" vision information. When running simulation scenarios to generate the test data, running the AI with perfect tracked vision is important because it decouples the AI behavior from the performance of the vision filters.

Technical Details We modified the Er-Force simulator to output the internal simulation state, which we use as ground-truth data, using the SSL Vision TrackerWrapperPacket. This effectively makes the simulator also act as a Tracker implementation, which is useful both for generating test data and running our AI with "perfect" vision information. When running simulation scenarios to generate the test data, running the AI with perfect tracked vision is important because it decouples the AI behavior from the performance of the vision filters.

2025 Team Description Paper: The Bots 7  
The Raw Position (Orange) vs. Filtered Position (Blue) vs. True Position (Green)  
x-coordinate (m) | y-coordinate (m)  
1.0 | -0.0025
1.5 | 0.0030
2.0 | -0.0020
2.5 | 0.0025
3.0 | -0.0030
3.5 | 0.0020
4.0 | -0.0025
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.0020
1.5 | 0.0015
2.0 | 0.0025
2.5 | 0.0010
3.0 | 0.0020
3.5 | 0.0015
4.0 | 0.0020
x-coordinate (m) | y-coordinate (m)  
0.0 | 0.0005
0.5 | 0.0010
1.0 | 0.00