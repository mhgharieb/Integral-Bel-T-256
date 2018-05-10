# Integral Attack on Bel-T-256
<!--- This project contains the supporting material of the paper entitled "Integral Attacks on Round-Reduced Bel-T-256", which has been submitted to SAC 2018.--->
## File description
1. `Bel-T.py`: The python script used to generate a MILP model for *n* rounds of the Bel-T block cipher, then search for an integral distinguisher based on the bit-based division property using the [Gurobi](http://www.gurobi.com/) optimizer.
2. `helpFunction.py`: The python module that contains the MILP models describing the division trail through COPY, XOR, AND, modular addition, modular addition with a constant, and modular subtraction. 
## Dependencies
The only dependency is the Gurobi optimizer which can be found [here](http://www.gurobi.com/).

## Usage
`python Bel-T.py <number of rounds> <Input division property>`

### Example 1
Create a MILP model for 2-round Bel-T and then search for an integral distinguisher based on the following input division property `00000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000011111111000000000000000000000000`. Note: This is "*IC1*" integral distinguisher in the paper.
* Command: 
```python
python Bel-T.py 2 "00000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000011111111000000000000000000000000"
```
* Output: 
```python
Integral Distinguisher Found!

# of rounds: 2 , activebits:9 , Input DP: 00000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000011111111000000000000000000000000
balanced bits: 5 [91, 92, 93, 94, 95]
Time used = 43.373281002 Seconds
```
This output means that the integral distinguisher for 2-round Bel-T and the above-mentioned input division property exists, and the bits 91, 92, 93, 94, and  95 (counted from the most significant bits) are balanced. This distinguisher needs 2<sup>9</sup> chosen plaintexts.

### Example 2
Create a MILP model for 2-round Bel-T and then search for an integral distinguisher based on the following input division property `01111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000`
* Command: 
```python
python Bel-T.py 2 "01111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000"
```
* Output: 
```python
Integral Distinguisher do NOT exist

Time used = 82.1842508316 Seconds
```
This output means that there is no integral distinguisher for 2-round Bel-T and the above-mentioned input division property.
