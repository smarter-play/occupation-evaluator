
# Sample data generation

The sample-data generation is the process of generating fake, but as much as realistic as possible, measurements associated to the mock Basket.

The "mock Basket" is a special Basket used for tests that is characterized by the ID `0x23232323` in hex, or `589505315` in decimal.

The problem consist in generating three type of measurements:
- **Accelerometer data**: an acceleration of the Basket board above a certain threshold.
- **People detection data**: the detection of people standing in front of the basket.
- **Basket data**: anything that occluded the IR detector (most commonly, the ball entering the basket).

The task of the generator, given a range of dates, is to generate for each day within the range fake measurements.

The measurements of a certain type, in a specific day, are drawn from a probability distribution that is day dependant.

The generator distinguish three types of days in a year:
- **Busy day**: a day for example of school or of work.
- **Unplayable day**: a day that is considered to be unplayable for example because of bad weather conditions (rain or cold).
- **Playable day**: any other day.

For every day type and for every measurement type, it's built a probability distribution from which the generator will sample pseudo-realistic timestamps for the measurements.



