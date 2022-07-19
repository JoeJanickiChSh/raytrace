def vec_to_color(vec):
    return tuple(map(lambda x: min(255, max(0, int(x*255))), (vec.x, vec.y, vec.z)))


def dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z


def lerp(a, b, fac):
    return (b-a) * fac + a
