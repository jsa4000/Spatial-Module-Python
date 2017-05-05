import time

class ProgressBar:
    """
        Progress bar to show the progress in the terminal.

        Following as example of how to use:

            with ProgressBar(filesize) as pbar:
                for i in range(10):
                    pbar.update(1)
                    time.sleep(1)
    """
    def __init__(self, total, start=0, units="%", size=30):
        self.total = total
        self.units = units
        self.current = start
        self.size = size
    def __enter__(self):
        # This must return itslf for With statemets
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        percent =  100
        print(self.get_progress_bar(1) + " 100.0"+ self.units + " DONE!         ")
    def get_progress_bar(self, percent):
        return "[" + ("#" * int(percent * self.size)) + (" " * (self.size -  int(percent * self.size))) + "]"
    def update(self, amount):
        self.current += amount
        percent =  self.current / self.total
        print(self.get_progress_bar(percent) + " " +"{0:.1f}".format(round(percent * 100,2)) + self.units, end="\r")
     
def timeit(method, showparams = False):
    """
        Define an inner function that invoke the method and measure the
        time that takes to run it.
    """
    def timed(*args, **kw):
        """
            This function will compute the time that takes to invoke
            the function passed by parameters.
            This function will return the same result as the function.
        """
        tstart = time.time()
        result = method(*args, **kw)
        tend = time.time()
        #Print the total amount of time consuming for the curent call
        if (showparams):
            print(('Time: %r (%r, %r) %2.2f sec') % (method.__name__, args, kw, tend-tstart))
        else:
            print(('Time: %r %2.2f sec') % (method.__name__, tend-tstart))
        return result
    # Compute the timing and return the same values of the function
    return timed
