import sys
EPSILON = sys.float_info.epsilon  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

#if __name__ == '__main__':
def get_colors(min,max):
    cols={0:(0,0,0)}
    minval, maxval =min, max
    steps = 31
    delta = float(maxval-minval) / steps
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # [BLUE, GREEN, RED]
    #print('  Val       R    B    G')
    for i in range(steps+1):
        val = minval + i*delta
        r, g, b = convert_to_rgb(minval, maxval, val, colors)
        c=r,g,b
        key=int(val)
        cols.update({key:c})
    #print(cols)
    return cols

       # print('{:.3f} -> ({:3d}, {:3d}, {:3d})'.format(val, r, g, b))
    #print(colors)