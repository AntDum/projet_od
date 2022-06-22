from project_od.utils import bezier_cub, bezier_lin, bezier_quad


class AnimateValue:
    def __init__(self, origin, destination, keys=[0, 1], fps=30, time=1) -> None:
        """
            Interpolate the value from origin to destination

            - Origin is the starting point
            - Destination is the end point

            The keys represent key pos (0-1) if ouside it goes ouside of the pos
            - keys length is 
                - 2 (linear)
                - 3 (quadratic)
                - 4 (cubic) 
            
            - fps is the fps 
            - time is the time to reach to destination (in seconds)

        """
        if not isinstance(origin, tuple | list):
            if isinstance(destination, tuple | list) and len(destination) > 1:
                raise ValueError("Origin and destination need to have the same form")
            origin = [origin]
            if not isinstance(destination, tuple | list):
                destination = [destination]
        if len(origin) != len(destination):
            raise ValueError("Origin and Destion need to have the same length")

        self.fps = fps
        self.time = time
        self.keys = keys
        self.destination = destination
        self.origin = origin
        self.delta =  tuple(d-o for o, d in zip(self.origin, self.destination))
        self._time = 0
    
    def set_origin(self, origin):
        self.origin = origin
        self.delta = tuple(d-o for o, d in zip(self.origin, self.destination))
    
    def set_destination(self, dest):
        self.destination = dest
        self.delta = tuple(d-o for o, d in zip(self.origin, self.destination))

    def reset(self):
        self._time = -1
    
    def next(self):
        self._time += 1
        if self._time == 0:
            return self.origin
        if self._time + 1 > self.time * self.fps:
                return self.destination

        frac_time = (self._time)/(self.time * self.fps)
        step = frac_time

        if len(self.keys) == 2:
            step = bezier_lin(frac_time, *self.keys)
        
        elif len(self.keys) == 3:
            step = bezier_quad(frac_time, *self.keys)
        
        elif len(self.keys) == 4:
            step = bezier_cub(frac_time, *self.keys)

        return tuple(o + d * step for d, o in zip(self.delta, self.origin))


    def has_finish(self):
        return self._time >= self.time * self.fps