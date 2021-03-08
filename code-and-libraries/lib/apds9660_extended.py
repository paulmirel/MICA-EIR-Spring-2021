from adafruit_apds9960.apds9960 import APDS9960

from collections import namedtuple

class APDS9960_Extended (APDS9960):
    """ Just APDS9960 plus the independent gesture values """
    def gesture_date(self):
        """(named) Tuple (up, down, left, right).
        Can return None if no data available.
        Discards all but the latest data set.
        Setup:
            i2c = busio.I2C(SCL, SDA)
            apds = APDS9960(i2c)
            apds.enable_gesture = True
            ... set thresholds etc
        """

        # FIXME: this is copypasta directly from gesture()
        #   really should factor it and this (as generator). do a pull-request

        # buffer to read of contents of device FIFO buffer
        if not self.buf129:
            self.buf129 = bytearray(129)

        buffer = self.buf129
        buffer[0] = APDS9960_GFIFO_U
        any_read = False

        n_recs = self._read8(APDS9960_GFLVL)

        while n_recs > 0:
            # we want to exhaust the fifo, i.e. get the last one

            with self.i2c_device as i2c:
                i2c.write_then_readinto(
                    buffer,
                    buffer,
                    out_end=1,
                    in_start=1,
                    in_end=min(129, 1 + n_recs * 4),
                )
            any_read = True

            # FIXME? why?
            #time.sleep(0.030)  # 30 ms

            n_recs = self._read8(APDS9960_GFLVL)

        if any_read:
            upp, down, left, right = buffer[1:5]
            data = namedtuple("gesture", ("up", "down", "left", "right"))
            data.up = upp
            data.down = down
            data.left = left
            data.right = right
            return data

        else:
            return None

