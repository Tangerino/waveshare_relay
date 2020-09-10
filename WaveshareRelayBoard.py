
"""
Relay hat support
RPi Relay Board
https://www.waveshare.com/product/raspberry-pi/hats/rpi-relay-board.htm
(c) 2020 - Carlos Tangerino
This is a free software
"""


def _set_relay_state(channel, state):
    file_name_template = "/sys/class/gpio/gpio{}/value"
    file_name = file_name_template.format(channel)
    try:
        with open(file_name, "w") as fp:
            fp.write(state)
    except Exception as e:
        error_message = "state - {}".format(e)
        return True, error_message
    return False, ""


class WaveshareRelayBoard:
    def __init__(self):
        self.ports = {
            0: "26",
            1: "20",
            2: "21"
        }
        self.state_on = "0"
        self.state_off = "1"
        self.count = len(self.ports)
        self.error = False          # if error on init (not target hardware)
        self.error_message = ""
        for relay, channel in self.ports.items():
            try:
                with open("/sys/class/gpio/export", "w") as fp:
                    fp.write(channel)
            except Exception as e:
                # ignore this error if done before. Should we unexport?
                # but we can't be sure will work all the time
                pass
            try:
                file_name = "/sys/class/gpio/gpio{}/direction".format(channel)
                with open(file_name, "w") as fp:
                    fp.write("out")
            except Exception as e:
                self.error_message = "direction - {}".format(e)
                self.error = True
                break

    def on(self, channel):
        if not self.error:
            self.error, self.error_message = _set_relay_state(self.ports[channel], self.state_on)
        return self.error

    def off(self, channel):
        if not self.error:
            self.error, self.error_message = _set_relay_state(self.ports[channel], self.state_off)
        return self.error


if __name__ == '__main__':
    from time import sleep
    relay_board = WaveshareRelayBoard()
    if relay_board.error:
        print("Error - {}".format(relay_board.error_message))
    else:
        delay = 0.1
        while True:
            for r in range(relay_board.count):
                relay_board.on(r)
                sleep(delay)
            for r in range(relay_board.count):
                relay_board.off(r)
                sleep(delay)
