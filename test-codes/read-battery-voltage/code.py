import board
from analogio import AnalogIn

vbat_voltage_pin = AnalogIn(board.VOLTAGE_MONITOR)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2


battery_voltage = get_voltage(vbat_voltage_pin)
print("VBat voltage: {:.2f}".format(battery_voltage))