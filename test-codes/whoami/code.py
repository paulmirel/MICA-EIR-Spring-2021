import sys, board, microcontroller, gc, analogio

print("I'm built on the chip: {:} running at {:}MHz".format( sys.platform, microcontroller.cpu.frequency/1000000) )
print("It's possible that this is a unique id for the chip (hex bytes): {:}".format( "".join("{:02x}".format(x) for x in microcontroller.cpu.uid) ) )
print("I have {:}kb of ram, {:}kb used for this program so far".format((gc.mem_alloc()+gc.mem_free())/1000.0, gc.mem_alloc()/1000.0))
print("  that might be lying about some available ram on things like the samd51")
print("I have some non-Volatile (microcontroller.nvm) {:} bytes".format(len(microcontroller.nvm) if microcontroller.nvm else 0))
voltage = microcontroller.voltage if "voltage" in dir(microcontroller) else None
if voltage:
    print("I think I'm plugged into something giving {:}V of power".format(voltage))
else:
    if "VOLTAGE_MONITOR" in dir(board):
        vbat_voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)
        voltage = vbat_voltage.value
        print("My raw board.VOLTAGE_MONITOR is {:}".format(voltage))
        print("So, I think my voltage is {:}".format( (voltage * 3.3 ) /65535 * 2))
    else:
        print("I don't know what voltage I'm plugged into (microcontroller.voltage)")


print("My circuitpython version is: {:}".format( sys.version ) )
print("My uf2 is: {:} {:}".format( sys.implementation.name, ".".join((str(s) for s in sys.implementation.version) )))

bits = 0
v = sys.maxsize
while v:
    bits += 1
    v >>= 1
print("Max integer is {:} ({:} bits)".format( sys.maxsize, bits+1 ) ) # +1 for sign

print("I look for import files in:")
for p in sys.path:
    print("  " + p)

print("Do I have builtin neopixel? {:}".format( "yes: board.NEOPIXEL" if ("NEOPIXEL" in dir(board)) else "no") )
print("Do I have a red LED? {:}".format( "maybe: board.D13" if ("D13" in dir(board)) else "not sure, I don't have board.D13") )

print("Pins")
board_pins = []
for pin in dir(microcontroller.pin):
    if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
        pins = []
        for alias in dir(board):
            if getattr(board, alias) is getattr(microcontroller.pin, pin):
                pins.append("board.{}".format(alias))
        if len(pins) > 0:
            board_pins.append(" ".join(pins))
for pins in sorted(board_pins):
    print("  {:}".format(pins))

try:
    import rtc
    t = rtc.RTC().datetime
    print("I have a built-in RTC which says: {:}.{:}.{:} {:}:{:}:{:}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
    print("  (usually not battery backup, so it restarts at power-up)")
except ImportError:
    print("I don't have a built-in RTC (or, at least, no rtc module)")
except Exception(e):
    print("I don't seem to have a built-in rtc: {:}".format(e))

