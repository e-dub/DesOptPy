def normalize(x, xL, xU):
    return(x-xL)/(xU-xL)


def denormalize(xNorm, xL, xU):
    return(xNorm*(xU-xL)+xL)
