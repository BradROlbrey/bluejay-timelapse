I quickly cobbled together these two Python scripts and Raspberry Pi Zero Ws to take timelapse pictures of baby bluejays, spanning a week and a half from just after they hatch until they leave the nest.
A Pi 0 is used for each camera.
The daytime camera uses a Pi Camera module v2.1, and the nighttime camera uses a Pi Camera module without an IR filter. The NoIR version allowed me to add infrared LEDs to provide light - bluejays can't see infrared, so this did not disturb them.
Still, not wanting to bathe them in IR perpetually, I turn the LEDs on and off through the Pi's GPIO pins only when a picture is taken. After all, who knows what else sees infrared?


Full week-and-a-half day timelapse, showing the little monsters grow into adorable fluffy birdos! (Apparently Github markdown doesn't support iframes, so this player-looking image is actually just a link to youtube, which might play an ad unless you have an adblocker)

<iframe width="100%" height="100%" src="https://www.youtube.com/embed/kPjclxg8t8g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Single night timelapse, showing restless chicks keeping mom up at night :)

<a href="https://www.youtube.com/watch?v=3oLIl-vjsxg" target="_blank" rel="noopener noreferrer"><img src="https://user-images.githubusercontent.com/17125101/204960245-653d34a1-eb0f-416c-9eea-50532602a2ab.png" width="800" /></a>


Picture of daytime camera mounted towards nest:
![bj-timelapse_daycam_pointing_at_nest](https://user-images.githubusercontent.com/17125101/204882842-5f5077b8-d8ae-40df-b7cf-c9b0411a0464.jpg)

Picture of day camera and night camera with IR LEDs jerryrigged to aluminum mounting pole:
![bj-timelapse_day_and_night_cams_on_stick](https://user-images.githubusercontent.com/17125101/204882860-31376c9a-5015-4eff-addf-3ffa03e012e3.jpg)
