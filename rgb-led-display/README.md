# Instructions for setting up and implementing RGB LED Display


## Starting points to note:
-   This folder contains a C++ library, and bindings to use separate C# and python libraries. For simplicity, we will be using the [python library](rgb-led-display-library/bindings/python).
-   These instructions assume that the RPis and LED panels are wired correctly, and that the power supply is set up correctly. For wiring instructions and troubleshooting, see [here](rgb-led-display-library/wiring.md).


## Big idea:
A RPi3 only has 40 pins, and so the max number of parallel rows it can accomodate is 3. Since we have 20 LED panels and are planning to make 5 rows of 4, we will need 2 RPis for the full display.

Since the API call we are doing fetches a JSON containing 4 different items, the display with 5 rows will be header followed by the 4 items, as shown:

|Header|
| ------------- |
|Data key & value 1|
|Data key & value 2|
|Data key & value 3|
|Data key & value 4|

The API call is done in this [script](rgb-led-display-library/bindings/python/samples/data-files/get_data.py) in a while true loop. Each successful API call logs the data into 2 different txt files. [data_keys.txt](rgb-led-display-library/bindings/python/samples/data-files/data_keys.txt) logs the keys of the dictionary obtained (eg. water tested). [data_values.txt](rgb-led-display-library/bindings/python/samples/data-files/data_values.txt) logs the corresponding values of those keys (eg. 120 gal).

Both the RPis will have the exact same library. Both will run the same script to do the API call to fetch the data to display. However, the script to display the data will be different for each RPi since they have different responsibilities - the 1st RPi will be in charge of the 1st 3 rows (out of 5) and the 2nd RPi will be in charge of the remaining 2.

The display script for the 1st RPi is [runtext_1.py](rgb-led-display-library/bindings/python/samples/runtext_1.py), which displays a header onto Row 1, then fetches the 1st 2 key-value pairs from the .txt files to display onto Rows 2 and 3. The display script for the 2nd RPi is [runtext_2.py](rgb-led-display-library/bindings/python/samples/runtext_2.py), which simply fetches the remaining 2 key-value pairs from the .txt files to display onto Rows 4 and 5.


## Steps to implement the full 5 row display:
1.  Run the script to fetch data on the 1st RPi
    -   Go to the [directory](rgb-led-display-library/bindings/python/samples/data-files) with the script
    -   Run:
    ```
    python3 get_data.py
    ```
    This will repeatedly fetch the data at regular intervals.
2.  Run the script to display the data on the 1st RPi
    -   Open a separate terminal
    -   Go to the [directory](rgb-led-display-library/bindings/python/samples) with the script
    -   Run:
    ```
    sudo python3 runtext_1.py -P3
    ```
    _sudo_ is required because some dependencies included require root permissions. _-P3_ indicates that there are 3 parallel rows for the 1st RPi. There is no need to specify how many panels are chained in a row since a default of 4 is already set [here](rgb-led-display-library/bindings/python/samples/samplebase.py).
3.  Repeat Step 1, but for the 2nd RPi this time.
4.  Repeat Step 2 for the 2nd RPi also. However, run this instead:
    ```
    sudo python3 runtext_2.py -P2
    ```
    As mentioned earlier, the 2nd RPi has a different display script from the 1st. It is also only in charge of 2 rows and thus -_P2_ is used.


## Final notes:
-   Default settings for the displays (eg. brightness, no. of panels in a chain, etc) can be changed [here](rgb-led-display-library/bindings/python/samples/samplebase.py).
-   If the displays flicker a lot, check that --led-slowdown-gpio is set to a default of 4 (the highest allowed value). This will slow down the RPi such that its speed matches the panels better and reduce a lot of the flickering.
-   For some reason, a --led-brightness setting of 100% leads to the least amount of flickering.
