# KrtPomodoro

This is a small Pomodoro application which I wrote to use with my tiling window managers. Indeed, it is an extremelly simple HttpServer which has a timer.

In order to make it run, I install a Python Virtual Environment:

    virtualenv ~/.venv/krtpomodoro/bin/activate
    source ~/.venv/krtpomodoro/bin/activate/bin/activate
    pip install -r requirements.txt
    
And that's it. This server can be started using the **server_start.sh** script, and the pomodoro server will start running on port 4884  in localhost. --- Yes, it only runs in localhost, I don't need anything but a localhost to run my naive pomodoro timer.

There's a file to configure all of this: **config.ini**, please, check it to understand it.
 
## Using the Pomodoro:

**Start the timer**

    curl -X POST http://localhost:4884/pomodoro/start
 
**Stop the timer**

    curl -X POST http://localhost:4884/pomodoro/stop
    
 **Toggle start/stop the timer**
 
    curl -X POST http://localhost:4884/pomodoro/toggle
    
  **Reset the timer**
  Sets the timer to the initial value and stops the timer. A start POST is needed to restart.
 
    curl -X POST http://localhost:4884/pomodoro/reset
    
  **Full Query the timer pomodoro**
  
       curl http://localhost:4884/pomodoro
       25:00 stopped POMODORO
   
   The return value is a simple string with 3 fields:
   
   * Time left of the timer (in minutes:seconds)
   * Status: stopped/started
   * What is it going on: BREAK/POMODORO -- Break time or working(pomodoro) time
   
   ** Query the timer **
   This is only intended for the Polybar configuration. Nothing else.
   
    curl http://localhost:4884/pomodoro/timer
    %{F#FF0000} 25:00

  ## Other tools running together with the Pomodoro
  Some oher tools are working with the Pomodoro... This will eventually become a set of tools which will provide me interesting information for my Window Manager or I will split the other naive out of the Pomodoro timer.
  
     curl localhost:4884/battery
     100 Full
  
    Provides the information retreived from **sys/class/power_supply/BAT0/** -- the capacity and the status files.
  