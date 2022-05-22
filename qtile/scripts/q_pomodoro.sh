#!/bin/bash

a=$(curl localhost:4884/pomodoro 2>/dev/null | awk '{print $1}')
echo -n $a
