import time, SearchTree,random


def test(what, additional=3, wtime=50,stesttime=25):
    t = time.time()
    checker = lambda x: x - t <= wtime
    while checker(time.time()):
        h = random.randint(1,15)
        w = random.randint(1,15)
        st = SearchTree.SearchTree(object=False, hei=h, wid=w, maxtime=stesttime)
        if what == "stredpg":
            st.stepreduction(additional, predicted_gain=True)
        elif what == "stred":
            st.stepreduction(additional,predicted_gain=False)
        elif what == "randomwalk":
            st.randomWalk()
        else:
            st.descendants(additional)


