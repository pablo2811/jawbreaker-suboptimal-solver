from SearchTree import SearchTree


def main():
    t = int(input("Number of tests."))
    for __ in range(t):
        h, w, c = [int(x) for x in input("Height Width NumberOfColors").split()]
        st = SearchTree(object=False, hei=h, wid=w, maxtime=80)
        st.stepreduction(3, predicted_gain=True)
        print(st.bestScore)
        st.solutionGif("10x10 PG")
        st.stepreduction(3,False)
        print(st.bestScore)
        st.solutionGif("10x10 noPG")




if __name__ == "__main__":
    main()
