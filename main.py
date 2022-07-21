from bin import problem_instantiator

print("Hello World")

problemInstance = problem_instance.ProblemInstance([1, 2, 3], [[1,2,3],[1,2,4],[1,2,5]])

print("getNodes(): ", problemInstance.getNodes())
print("getNode(1): ", problemInstance.getNode(1))
print("getDistanceMatrix(): ", problemInstance.getDistanceMatrix())
print("getDistance(1, 2): ", problemInstance.getDistance(1, 2))
