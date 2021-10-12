from PIL import Image
from PIL import ImageDraw
import random

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result

def draw_bezier_v_checkmark(draw: ImageDraw, box, color=(0,0,0), num_points=100, checkmark_width=6):
    '''
    Draw the V checkmark using bezier curve.
    '''
    ts = [t/num_points for t in range(num_points+1)]
    x1, y1, x2, y2 = box

    img_width, img_height = draw.im.size
    box_width, box_height = x2-x1, y2-y1

    # p1 = (0, 0.5*box_height)
    # p12 = (0.3*box_width, 0.6*box_height)
    # p2 = (0.4*box_width, box_height)
    # p23 = (0.5*box_width, 0.5*box_height)
    # p3 = (0.9*box_width+50, -50)

    p1 = (0-random.randint(0, int(box_width/10)), random.uniform(0.4, 0.6)*box_height)
    p2 = (random.uniform(0.4, 0.6)*box_width, box_height)
    p3 = (random.uniform(0.9, 1.5)*box_width, random.uniform(0., -box_height))
    p12 = (random.uniform(0.5, 0.75)*(p1[0]+p2[0]), random.uniform(0.3, 0.4)*(p1[1]+p2[1]))
    p23 = (random.uniform(0.3, 0.4)*(p2[0]+p3[0]), random.uniform(0.3, 0.4)*(p2[1]+p3[1]))

    xys = [p1, p12, p2]
    bezier = make_bezier(xys)
    points = bezier(ts)

    xys = [p2, p23, p3]
    bezier = make_bezier(xys)
    points.extend(bezier(ts))

    offset_x = random.randint(-int(box_width/4), int(box_width/4))
    offset_y = random.randint(-int(box_height/3), 0)

    points = [(point[0]+x1+offset_x, point[1]+y1+offset_y) for point in points]
    [map((int,int), point) for point in points]
    for idx in range(len(points)-1):
        draw.line([points[idx], points[idx+1]], fill=color, width=checkmark_width)

    return draw


def draw_bezier_x_checkmark(draw: ImageDraw, box, color=(0,0,0), num_points=100, checkmark_width=12):
    '''
    Draw the V checkmark using bezier curve.
    '''
    ts = [t/num_points for t in range(num_points+1)]
    x1, y1, x2, y2 = box

    img_width, img_height = draw.im.size
    box_width, box_height = x2-x1, y2-y1

    offset_x = random.randint(-int(box_width/5), int(box_width/5))
    offset_y = random.randint(-int(box_height/4), 0)

    ### x checkmark
    p1 = (box_width*random.uniform(0, 0.3), box_height*random.uniform(0, 0.3))
    p12 = (box_width*random.uniform(0.4, 0.6), box_height*random.uniform(0.4, 0.6))
    p2 = (box_width*random.uniform(0.7, 1), box_height*random.uniform(0.7, 1))

    p3 = (box_width*random.uniform(0.7, 1), box_height*random.uniform(0, 0.3))    
    p34 = (box_width*random.uniform(0.4, 0.6), box_height*random.uniform(0.4, 0.6))
    p4 = (box_width*random.uniform(0, 0.3), box_height*random.uniform(0.7, 1))   

    points1 = []
    xys = [p1, p12, p2]
    bezier1 = make_bezier(xys)
    points1 = bezier1(ts)
    points1 = [(point[0]+x1+offset_x, point[1]+y1+offset_y) for point in points1]
    [map((int,int), point) for point in points1]

    points2 = []
    xys = [p3, p34, p4]
    bezier2 = make_bezier(xys)
    points2 = bezier2(ts)
    points2 = [(point[0]+x1+offset_x, point[1]+y1+offset_y) for point in points2]
    [map((int,int), point) for point in points2]

    for idx in range(len(points1)-1):
        draw.line([points1[idx], points1[idx+1]], fill=(0,0,0), width=checkmark_width)

    for idx in range(len(points2)-1):
        draw.line([points2[idx], points2[idx+1]], fill=(0,0,0), width=checkmark_width)

    return draw


if __name__ == '__main__':
    im = Image.new('RGBA', (1000, 1000), (0, 0, 0, 0)) 
    draw = ImageDraw.Draw(im)
    ts = [t/100.0 for t in range(101)]

    # xys = [(0, 500), (300, 600), (400, 1000)]
    # bezier = make_bezier(xys)
    # points = bezier(ts)

    # xys = [(400, 1000), (500, 500), (900, 0)]
    # bezier = make_bezier(xys)
    # points.extend(bezier(ts))

    # xys = [(100, 50), (100, 0), (50, 0), (50, 35)]
    # bezier = make_bezier(xys)
    # points.extend(bezier(ts))

    # xys = [(50, 35), (50, 0), (0, 0), (0, 50)]
    # bezier = make_bezier(xys)
    # points.extend(bezier(ts))

    # xys = [(0, 50), (20, 80), (50, 100)]
    # bezier = make_bezier(xys)
    # points.extend(bezier(ts))

    # for idx in range(len(points)-1):
    #     draw.line([points[idx], points[idx+1]], fill=(0,0,0), width=3)
    # im.show()