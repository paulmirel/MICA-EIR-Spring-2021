#pushbutton test

import time
import board

def verbose(msg):
    print(msg)

# our special button handler
from record_button import RecordButton

record_button = RecordButton(board.D12)
broken_button = RecordButton(board.D12) # should cause a readable message!
loop_time = 0

print( "Button Check" )
while True: 
    start_loop_time = time.monotonic()

    # this is the pattern of "check often if long chunk of code"
    # If you can click the button slower than once per 100ms,
    # you'll see  "Button Closed 3" or some other count
    # for the collected button-presses during this "long chunk"
    for x in range(1,80):
        record_button.check()
        time.sleep(0.01) # have to check each < 100ms
    
    # now we want to know if a button
    # happened during that "long" chunk of code
    if record_button.was_pressed():
        print( "Button Closed {:}".format(record_button.count) )
        record_button.reset()

    if broken_button.was_pressed():
        print("This should never happen! It's broken!")

    # print out how slow we are
    this_loop_time = time.monotonic() - start_loop_time
    if loop_time < this_loop_time:
        loop_time = this_loop_time
        print("Loop time {:}".format(loop_time))
    time.sleep(0.001)
