from SearchTree import SearchTree


def main():
    t = int(input("Number of tests."))
    for __ in range(t):
        h, w, c = [int(x) for x in input("Height Width NumberOfColors").split()]
        board = []
        for i in range(h):
            board.append([int(x) for x in input(f"{i+1}-row").split()])
        st = SearchTree(starter=board)
        st.stepreduction(2, 2)
        st.stepreduction(2, 3)
        st.randomWalk()
        st.descendants(1)


if __name__ == "__main__":
    main()
