    def angleClock(self, hour, minutes):
        angle1 = (hour % 12 * 60.0 + minutes) / 720.0
        angle2 = minutes / 60.0
        diff = abs(angle1-angle2)
