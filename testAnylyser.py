import matplotlib.pyplot as plt
import driver_multiple_tests
import time
import os

# types : randomwalk stredpg stred desc


def time_size_util(what, ax, args=None, newtests=False, readTime=20, testTime=30):
    """
    util function for its wrapper testAnylyser.time_size
    :param what: [string] type of search (string), check *types*
    :param ax: [AxesSubplot] pyplot Figure on which to add data
    :param args: [int] additional arguments if necessery (branches/descednats)
    :param newtests: [bool] should we performe new tests for this search
    :param readTime: [int] maximum time of creating plot (reading logs)
    :param testTime: [int] time for additonal tests (if :param newtests == True)
    :return: [AxesSubplot] ax updated with new data
    """
    args_type = ["stredpg", "stred", "desc"]
    additional = False
    if what in args_type:
        additional = True
        assert args is not None
    if newtests:
        driver_multiple_tests.test(what, additional=args, wtime=testTime)

    def util():
        sizes = []
        times = []
        checker = lambda x: x - time.time() < readTime
        path = what + "log.txt"
        with open(path, "r") as f:
            for line in f.readlines():
                if checker(time.time()):
                    command = line[:-1].split(";")
                    if (additional and command[1] == str(args)) or not additional:
                        sizes.append(int(command[0]))
                        times.append(float(command[-1]))
                else:
                    break
        if additional:
            l = f"{what} {args}"
        else:
            l = f"{what}"
        ax.scatter(sizes, times, marker="o", label=l)
        ax.set(xlabel="Size of jawbreaker board", ylabel="Time of execution")
        ax.legend()
        return ax

    return util()


def time_size(which, name, t=20, new=None):
    """
    :param which: (list) of tuples  eg. [ ("stredpg",2),("desc",2),("randomwalk",None)]
    :param t: (integer) denoting time of the test
    :param new: (list) of tuples (type_of_search,args,time[s]) [("stredpg",2,20),
    ("randomwalk, None,10)] or None
    :param name: (string) name of a file to save
    :return: n/a
    """
    if new is None:
        new = []
    fig, ax = plt.subplots()
    for el in which:
        assert 0 < len(el) <= 2
        if len(el) == 1:
            a = None
        else:
            a = el[1]
        if len(new):
            found = False
            for x in new:
                if el[0] == x[0] and a == x[1]:
                    ax = time_size_util(el[0], ax, args=a, newtests=True, readTime=t // len(which), testTime=x[2])
                    found = True
                    break
            if not found:
                ax = time_size_util(el[0], ax, args=a, readTime=t // len(which))

        else:
            ax = time_size_util(el[0], ax, args=a, readTime=t // len(which))
    os.chdir("analytics")
    fig.savefig(f"{name}.png")
    os.chdir("..")


which = [("stredpg", 3), ("randomwalk", None), ("stred", 3), ("desc", 2)]
time_size(which, "final", 30, new=[("desc", 2, 60), ("stred", 3, 20)])
