# Jeff's Office Light

This contains a python script (which you can run via systemd) that polls the
status of the monitor and USB camera on a Linux machine. It posts to Home
Assistant when the status of either change.

There's also an example Home Assistant automation which I use to drive a light
bulb in my office. If my camera is on (e.g. I'm in a meeting), the light bulb
turns red. Otherwise, if my screen is on, the light bulb turns green. If
neither of those are true, the light bulb turns off.
