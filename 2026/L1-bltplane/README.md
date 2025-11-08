# 11/8/25

Launched a bltplane holding 1 sensor mod and 1 radio mod on an L1 kit

## Setup
- Launched on Poisson Dart, a slightly modified version of Poison Dart by Donovan Barros.
- On attempt 1, RSO said your fin fillets have cracks, your motor retainer is wack, go home (or fix it and come back)
- We borrowed JBQuick from some canadians and sealed up the motor retainer and went over the cracks in the fillets
- On attempt 2, RSO said ok, have fun guys
- GPS wasn't working but we setup 4 guys to watch it and it was in view the whole time
- Forgot to tell someone to video it though
- All modules at [this](https://github.com/RIT-Launch-Initiative/FSW/commit/0700af97dc681b3515d198d7582d855ec7e1b56f) FSW commit
## Summary
- 
- Flash storage on sensor mod chilling
	- Dean protection bytes all good and functional
	- Boot counting working during evil power tests (not in flight, just sitting on table)
- Flash storage on other mods as well
	- couldnt access radio mod headers :( (we gotta get telnet into these guys)
- GPS continued to not work
	- despite working the previous night (albeit with different lora transmission context)
	- Louis has theories that are testable
- Radio worked but was a real nailbiter bc of some questionable packet format decision (yap w/ richie)
- Boost detect worked wonderfully
	- Seeing the future so save the past (start of boost) is a premium feature reserved for payloads so it was not implemented
- Apogee detect got silly
	- Apogee lockout worked great
	- Immediately after Apogee lockout went out, apogee was detected bc Barometer 1 was acting all funny
	- This happened bc Barometer 1 was showing big stairsteps (looks like we were only reading the MSB or something like that
		- Wasnt undersampled bc the time was varying quickly (look at edges of stairs where it flickers back and forth real quick)
	- Bc the output looked so constant, it looked to the apogee detector like it was at apogee (vertical velocity < 10 ft/s for 250ms)
	- There were 2 barometers wired together as an OR so as soon as the first went, the rocket assumed it happened
- Ground detect disabled bc literally just use a timer lol.
