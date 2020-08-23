import time,SearchTree

def main():
    T = int(input("Time of the test"))
    t = time.time()
    while time.time() - t <= T:
        st = SearchTree.SearchTree(random=True)
        st.randomWalk()
        for i in range(1,4):
            if time.time() - t > T:
                break
            for j in range(1,4):
                if time.time() - t > T:
                    break
                st.stepreduction(i,j)
        st.descendants(1)
        st.descendants(2)










if __name__ == "__main__":
    main()
