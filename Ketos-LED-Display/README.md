Instructions for setting up and impleneting RGB LED displays
============================================================

Starting points to note:
- This folder contains a C++ library, and bindings to use separate C# and python libraries. For the functionality required and simplicity's sake, we will be using the [python library](rpi-rgb-led-matrix/bindings/python).
- The setup assumes that the pi and boards are wired correctly, and that the power supply is set up correctly. For wiring instructions, see [here](rpi-rgb-led-matrix/wiring.md).

Testing the LED displays:
1. In the terminal, go to the [python samples directory](rpi-rgb-led-matrix/bindings/python/samples).
2. Run "sudo python _filename_.py -c _chainlength_". For example, if there are 4 displays in a chain, to run simple-square.py, run "sudo python simple-square.py -c4"
   - note that you must run command as root and hence sudo is required

Doing the API calls to get display data:
1. In the terminal, go to the directory with the API call script found [here](rpi-rgb-led-matrix/bindings/python/samples/data-files).
2. Run "sudo python getData.py"
   - The API call is done in a while true loop with 5 min intervals after each successful call. To edit this value, edit time.sleep() in the loop
   - To prevent the API calls from looping, uncomment "break" in the while loop
   - Each successful API call logs the data into 2 different txt files. [data-keys.txt](rpi-rgb-led-matrix/bindings/python/samples/data-files/data-keys.txt) logs the keys of the dictionary obtained. [data-values.txt](rpi-rgb-led-matrix/bindings/python/samples/data-files/data-values.txt) logs the corresponding values of those keys.

Turning on the LED displays to display the data:
1. In the terminal, go back to the [python samples directory](rpi-rgb-led-matrix/bindings/python/samples).
2. Run "sudo python runtext.py -c _chainlength_", where _chainlength_ is the number of displays in a chain.