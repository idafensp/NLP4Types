import time

import logging
logger = logging.getLogger(__name__)

class Steps:
    fstep = 0
    lstep = -1

    times = []
    tags = []

    def __init__(self, fs = 0, ls=1000):
        self.fstep = fs
        self.lstep = ls

    def isstep(self, step, tag=""):
        if self.lstep >= step >= self.fstep:

            new_time = time.time()
            self.times.append(new_time)
            self.tags.append(tag)

            logger.debug("Starting step %s (%s)"  % (step,tag))

            if len(self.times) > 1:
                step_time = new_time - self.times[-2]
                logger.debug("Previous step (%s) took %s seconds"  % (self.tags[-2],step_time))
            
            return True
        else:
            logger.debug("Skipping step %s (%s)"  % (step,tag))
            return False

    def endsteps(self):
        self.times.append(time.time())

    def __get_total_time_string(self, init, end):
        total_secs = end - init
        total_hours = total_secs / 60.0 / 60.0
        total_days = total_hours / 24.0
        tts = "Total time=%s secs. - %s hours. - %s days" % (total_secs, total_hours, total_days)

        return tts


    def get_print_times(self):
        time_string = "--- TIMES ----\n"
        time_string = time_string + str(self.times) + "\n-----------\n"
        for (i,t) in enumerate(self.times[1:]):
            time_lapse = t - self.times[i]
            ts = "%s) Step %s (%s) took=%s secs." % (i, (self.fstep+i), self.tags[i],time_lapse)
            time_string  = time_string + ts + "\n"


        tts = self.__get_total_time_string(self.times[0],self.times[-1])

        time_string = time_string + tts + "\n"

        time_string  = time_string + "-----------\n"
        return time_string