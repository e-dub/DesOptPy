def normalize(x, xL, xU):
    return (x - xL) / (xU - xL)


def denormalize(xNorm, xL, xU):
    return xNorm * (xU - xL) + xL


if __name__ == '__main__':
    print('testing')
    import numpy as np

    x0 = np.array([9, 900])
    xL = np.array([10, 10])
    xU = np.array([1000, 1000])
    xNorm = normalize(x0, xL, xU)
    print(xNorm)
    x = denormalize(xNorm, xL, xU)
    print(x)
