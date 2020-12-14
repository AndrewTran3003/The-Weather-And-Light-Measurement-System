# The Weather And Light Measurement System
This system is a part of assignment 2 for the subject IoT Programming at Swinburne University of technology.

It consists of an LED indicator which represents the fan (I cannot use the mini fan as it causes problems with the USB port of my computer), a temperature sensor, and an ambient light sensor.

The system collects the data from the temperature sensor and compares it against the weather data gathered from a 3rd party API. If the temperature inside is higher than that of the API, it will say "The current value is higher than that of the API" and vice versa.

The ambient light sensor is used to trigger the dark mode/light mode theme of the website backed by the Flask server. If it is dark, the website will have a dark theme and vice versa.

The data collected by the sensors is stored in a MySQL database, and queried by the website to generate the visualization (in the form of a bar chart and a table) of the data.

Link to the video presentation: https://drive.google.com/file/d/1O694GsXb47DXfF-dX1IpNKdWlPKpZfHI/view?usp=sharing
