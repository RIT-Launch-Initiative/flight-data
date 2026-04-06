# Motown

L1 Rocket

Equipped with a controls_module+babyplane for airbrakes sensor, kalman filter, and gyro integration testing and a featherweight for "ground truth" measurements. 

# Measurements

| Section                   | Mass [g] |
| ------------------------- | -------- |
| Whole (w/ burnt motor)    | 721      |
| Whole (w/o burnt motor)   | 637      |
| Nosecone                  | 87       |
| Payload Bay               | 164      |
| Booster (w/ burnt motor)  | 459      |
| Booster (w/o burnt motor) | 375      |
| Motor Retainer            | 12       |


# The Incident

## The beginning
1. Get rocket RSOed and integrate payload. Takes a bit of force to twist it to screw holes on this L1 
2. Set rocket up on the pad. 
3. See it launch last in the salvo
4. Goes quite high and looks to float far away but it wasn't so bad

## The Rumblings of Trouble

5. The buzzer beep that tries to get the attention of the RECO team and announce that boost was detected and the flight is over does not sound
6. Instructions given to maintain power and bring it back for diagnosis

## The Initial Diagnosis
Imagine a shorted battery in a car. And then stop imagining because we didn't realize it at the time. 

7. UART to USB converter connected but gives no signs of life
8. JLink with `--no-reset` attempts to connect but times out with suggestion "Please check power connection and settings"
9. Settings confirmed before, reseat SWD cable but still fails with same error
10. Measure voltage across VBAT to GND on Babyplane: 7.98 V
11. Measure 3.3V rail out of connector on controls_module: ~0.01 V
12. Observe the physical structure
    - note: Bent pin (VBAT towards GND) on 30 pin connector of baby plane
![Bent VBAT pin on bottom of Baby Plane 1st](images/bent_vbat_pin.jpg)
![Bent VBAT pin on bottom of Baby Plane 2nd](images/bent_vbat_pin2.jpg)

    - note: cracked support columns on left and right of board ![Cracked 3d print on right side of board](images/cracked_right_post.jpg) ![Cracked 3d print on the left side of the board](images/cracked_left_post.jpg)
13. Ponder
    - VBAT pin could not be touching GND for very long or we would have a much bigger problem on our hands in the mad battery department. Initial assumption of them shorting and doing something bad discarded because it would take an insane amount of force to bend a pin that much. Still possibility that they were prebent at some point and briefly touched. 
    - Did have to apply a bit of force to the mount when going in. As of photos after Emma's flight but before Zoey's flight, mount is totally intact. Amount of force was not smashing but a firm twist to align screws
14. Unplug battery until later autopsy

## The Autopsy
15. Eat food so we have our wits about us
16. Bend babyplane VBAT pin away from ground
17. Attach 8V from power supply to VBAT on babyplane screw connector 
18. Enable power supply and controls_module+babyplane stack immedietly appear to be overcurrenting. Further tests show it consuming 0.54 A. Power supply was set for 8.00 V but shows 8.14 V
19. Remove flight controls_module from flight babyplane
20. Enable power to only babyplane and verify 3.3V regulator, 5V regulator, and VBAT are as expected with no module on
21. Attach known good controls_module to flight babyplane and verify normal behavior and current draw (0.041 A)
22. Attach known good babyplane to flight controls_module and verify large current draw
23. Switch back to testing flight controls_module on flight babyplane  
24. Enable power supply, measure VBAT to GND on screw connector at 5.7V, 3.3V rail on controls_module still at basically zero
25. 3.3V regulator on babyplane heats up PCB around it when running 
26. Only things on VBAT rail on controls_module are pyro channels and ematch. 
27. Remove 0 ohm resistor to pyro power to separate concerns. Nothing changes
28. Touch chips on the board and realize wiznet is hot. Subsequent touches show its only vaguely warm not hot.
29. With no way to turn on the board, no other ideas and a big red flag, we decide to remove the w5500 from the board.
30. DRD goes to town and removes chip, legs, and solder. Verified under microscope that probably no pads are touching
31. Reconnect flight babyplane and flight controls module to power supply
32. Shows <0.041 A current draw and exactly 8 V
33. Plug in USB to UART converter and board working as expected
34. Successfully dump data from serial. Verify parameters, preboost data, some flight data followed by large amount of erase value (0xff)
35. Plot data that is available. Signs point to event at snatch. By construction, after boost all data writing is done in a single loop so between the last value written and disaster is no more than 10ms
![Graph showing normal flight before ending abruptly at around the time of snatch](images/TheIncidentInFlight.png)

36. Check all the sensors still work


<img width="307" height="355" alt="image" src="https://github.com/user-attachments/assets/961660d6-ab0a-401a-bacf-2cfa6fd3a0ba" />


## Theories

### Theory 1: Capacitor free-wheeling
Assumption: Pin was prebent and snatch force caused them to short for a little bit. 
When the battery/ground shorted, the potential across the capacitor became a negative voltage, that was then shunted through the steering/ESD diodes inside of the chips.
Consensus; while this is possible, the actual amount of power dissipated would be quite low. In addition, the W5500 actually seems to be the chip most likely to take the negative-going voltage, it is permitted to -0.5v compared to the -0.3 to 0.0 of most others.

### Theory 2: Transformer short
The transformers are heavy and full of wires, a shock impact could have shorted those, and taken out the W5500's media interface in the process.
Consensus; unclear what a short between ethernet would do, probably not much since that's basically what a transformer is anyway. Cannot explain the entire 3.3v rail going down.

### Theory 3: Generic FOD
Impossible to prove, potentially a short between 2 non-ideal spots resulted in damage to the IC. 
Consensus; one of the best theories due to the variability and unpredictability of when/how/if this'd happen, when stacked against the precedence of W5500 flights with no issues. Also lots of evidence of contamination on the boards.

### Theory 4: MTBF Luck of the Draw
This is just a chance encounter of the W5500 dying at a random unknown time like any other component of any other system. While it is rare and unlikely to happen on the average, we are subjecting the parts to extreme conditions and use them very commonly. So we are eventually likely to see a component failure. WizNET is also a relatively unknown/small company compared to a powerhouse like TI.
Consensus; again impossible to prove, but very unlikely due to the number of W5500s that are operating for longer times around the world. 

### Theory 5: Physical Impact Damage
Damage to surrounding av bay may point to a mechanical impact with the W5500 directly or the area around it, leading to a failure. 
Consensus: Unlikely, impossible to prove without IC dissection. Overmolded design of the IC makes this unlikely.

### Theory 6: ESD strike
While the W5500 is protected, it is still a likely candidate for ESD (both from the header and from direct handling).
Consensus; Possible, due to ESD protection only existing on off-board connectors. Any contact with the board itself may have caused issues that manifested in flight.

> My money is on a mix of 6/4/3, potentially with them causing each other (FOD led to increased chance of ESD, which pushed the chip towards the edge of a mean failure for instance). Overall consensus is this is an unlikely event that could potentially be mitigated in the future with safer handling, protective enclosures, and more robust ESD-safe designs.
> - J.H.

# Data Products

## Control Module Flight

Stored under `flight/controls_module`. See `AirbrakeL1Tests/README.md` for information about the file formats.

## Featherweight

The saved data was downloaded from the featherweight and saved under `flight/featherweight`
