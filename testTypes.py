import driver_multiple_tests,testAnylyser

def stpg_avgscore_comp(t):
    which = []
    for i in range(4,0,-1):
        driver_multiple_tests.test("stredpg",i,t//4)
        which.append(("stredpg",i))
    testAnylyser.chart("Score",which,"Average score comparision STREDPG")


stpg_avgscore_comp(100)




