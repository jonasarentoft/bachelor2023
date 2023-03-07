from common.utility import GetPath

def GetDataForBidirectional(forwardDistances, backwardDistances, forwardPrevious, backwardPrevious):
    intersection = (backwardDistances.keys() & forwardDistances.keys())
    intersection = int(list(intersection)[0])
    path = GetPath(intersection, backwardPrevious)[::-1] + [intersection] + GetPath(intersection, forwardPrevious)
    
    return (forwardDistances | backwardDistances), path