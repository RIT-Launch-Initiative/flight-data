# URRG Launch on 3/28/26

Test flight of 3 L1s with a controls_module+babyplane combination for airbrakes sensor data, kalman filter tuning, and gyroscope orientation verification/

The same physical devices were used for all three flights.

# File Formats

## Engine File

`AeroTech_HP-H195NT.eng` is the thrust curve file from [ThrustCurve.com](https://www.thrustcurve.org/motors/AeroTech/HP-H195NT/)

## Openrocket

`rocket.ork` is the openrocket file for this flight. Accuracy is up for debate as real masses were not measured day of.


## Featherweight

CSV of data downloaded after the flight NOT the packets received by the ground station

## Controls Module

Data format from SRAD software. It was downloaded from the flight computer over serial and parsed using the `parse_capture.py` script in this directory.

### Controller Configuration
controller_configuration.json provides a description to the firmware for how it should run. This includes
- Kalman Filter matrices
- IMU orientation quaternions
- Atmosphere model

### params.csv

singly stored data points that describe the environment of the flight: Which controller_description was used, what was the gyro bias at time of launch, what timestamp was boost detected at etc.

| Param | Units | Meaning |
| -- | -- | -- |
| `magic` |  | Exists to check validity of data in flash memory, can be ignored for analysis |
| `timestamp_of_boost_detect_ms` | ms | uptime of the flight computer in milliseconds when boost was detected |
| `pre_boost_pressure` | kPa | The pressure we felt on the rail before the motor was lit |
| `bias_x_dps` | °/s | The bias we found in the gyroscope x axis for 2 seconds before the motor was lit |
| `bias_y_dps` |°/s |The bias we found in the gyroscope y axis for 2 seconds before the motor was lit |
| `bias_z_dps` |°/s| The bias we found in the gyroscope x axis for 2 seconds before the motor was lit |
| `bootcount` | | Number of times this flight computer booted since it first began counting | 
| `lockout_ms` | ms | Amount of after motor ignition that we will not command the servo. NOTE: this is not reflected in the effort parameter in the saved data but it is honored when the servo is to be set in flight. |
| `num_flight_packets` |  | Number of discrete packets of data we store (at 100hz)
| `num_preboost_packets` | | Number of discrete packets we store ahead of boost detect to be written after such that we don't miss the first couple moments of flight |
| `num_gyro_bias_packets` | | Number of packets that go into developing the average bias values |
| `md5` |  | md5 sum of the controller_configuration.json file used to build the program for this flight |
| `up_axis_q1` | | Scalar component of quaternion describing the transformation from IMU space to rocket space |
| `up_axis_q2` | | `i` component of above quaternion |
| `up_axis_q3` | | `j` component of above quaternion |
| `up_axis_q4` | | `k` component of above quaternion |
| `atmo0` | meters | constant component of polynomial atmosphere model |
| `atmo1` | meters/pascal | 1st order component of polynomial atmosphere model | 
| `atmo2` | meters/pascal^2 | 2nd order component of polynomial atmosphere model | 
| `atmo3` | meters/pascal^3 | 3rd order component of polynomial atmosphere model | 
| `atmo4` | meters/pascal^4 | 4th order component of polynomial atmosphere model | 
| `atmo5` | meters/pascal^5 | 5th order component of polynomial atmosphere model | 


### data.csv

| Data Value | Unit | Meaning |
| -- | -- | -- |
| `timestamp_ms` | ms | Time since boot at the time this sample was taken. Consult params.csv for the time that boost was detected |
| `temp_c` | °C | Temperature of the AV bay from the barometer (MS5611) | 
| `pressure_kpa` | kPa | Measured barometric pressure in the AV bay (MS5611) | 
| `accel_x_m_s2` | m/s^2 | Measured x-axis acceleration. x-axis in IMU space (LSM6DSV) |
| `accel_y_m_s2` | m/s^2 | Y component of above |
| `accel_z_m_s2` | m/s^2 | Z component of above |
| `gyro_x_dps` | °/s | Measured x-axis angular velocity. x-axis in IMU space (LSM6DSV) |
| `gyro_y_dps` | °/s | Y component of above |
| `gyro_z_dps` | °/s | Z component of above |
| `e_alt_m` | meters | AGL Altitude estimate from kalman filter |
| `e_vel_m_s` | meters/s | Velocity estimate from kalman filter |
| `e_acc_m_s2` | m/s^2 | Acceleration estimate from kalman filter |
| `e_bias` |  | Bias estimate from kalman filter. See Tech report or Airbrake Control Report |
| innovation0 | | Innovation of the kalman filter corresponding to AGL altitude |
| innovation1 | | Innovation of the kalman filter corresponding to measured vertical acceleration |
| rAcB | | Row `A` and column `B` of rotation matrix describing the onboard integrated gyroscope |
| effort | | Commanded effort for the airbrakes. Purely fictional for the L1s as they had no physical airbrakes |



This data was not completely filled for John's rocket due to The Incident. This is explained further in `Johns/README.md`

