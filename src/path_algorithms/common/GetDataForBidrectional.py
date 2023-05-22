from common.GetPath import GetPath

def GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious, intersection):

    if intersection:
    
        path = GetPath(intersection, backwardPrevious)[::-1] + GetPath(intersection, forwardPrevious)[1:]
        distance = forwardDistances.get(intersection) + backwardDistances.get(intersection)
        return (forwardDistances | backwardDistances), path, distance
    
    else:
        return (forwardDistances | backwardDistances), [], None 