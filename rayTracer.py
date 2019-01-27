from tkinter import *
from math import *
from vectors import *

# define screen size
WIDTH, HEIGHT = 640, 480

# define sphere class
class Sphere:

    def __init__(self, loc, radius, diff, spec, color):
        self.location = loc
        self.radius = radius
        self.diffuse = diff
        self.specular = spec
        self.color = color

# function for calculate ray intersection and deffuse
def raycast(currx, curry):
    result = 0
    # calculate intersection
    k = camPos.x - currx
    l = camPos.y - curry
    m = camPos.z - scrPos.z

    alpha = (currx * l) / k - curry + sp1.location.y
    beta = (currx * m) / k - scrPos.z + sp1.location.z

    a = 1 + (l / k) * (l / k) + (m / k) * (m / k)
    b = (-2) * (sp1.location.x + (l * alpha / k) + (m * beta / k))
    c = (sp1.location.x * sp1.location.x) + (alpha * alpha) + (beta * beta) - (sp1.radius * sp1.radius)

    delta = b * b - 4 * a * c
    # if there are intersections then calculate calcualte surface points
    if 0 <= delta:
        result = 0
        tempRoot1 = (-b + pow(delta, 0.5)) / (2 * a)
        tempRoot2 = (-b - pow(delta, 0.5)) / (2 * a)

        tempZ1 = ((tempRoot1 - currx) * m / k) + scrPos.z
        tempZ2 = ((tempRoot2 - currx) * m / k) + scrPos.z

        tempY1 = ((tempRoot1 - currx) * l / k) + curry
        tempY2 = ((tempRoot2 - currx) * l / k) + curry

        if tempZ1 <= tempZ2:
            surPoint = Vector(tempRoot1, tempY1, tempZ1)

        else:
            surPoint = Vector(tempRoot2, tempY2, tempZ2)

        # calculate the diffuse value for the given surface point
        # light directional vector
        lightDirVec = lightPos.substract(surPoint)
        lightDirMag = sqrt(lightDirVec.x ** 2 + lightDirVec.y ** 2 + lightDirVec.y ** 2)
        lightDirUnitVec = lightDirVec.multiply(1 / lightDirMag)

        # surface normal directional vector
        surfaceNormVec = surPoint.substract(sp1.location)
        surfaceNorMag = sqrt(surfaceNormVec.x ** 2 + surfaceNormVec.y ** 2 + surfaceNormVec.z ** 2)
        surfaceNorUnitVec = surfaceNormVec.multiply(1 / surfaceNorMag)

        # dor product between normal and light direction
        diffdot = (lightDirUnitVec.x * surfaceNorUnitVec.x + lightDirUnitVec.y * surfaceNorUnitVec.y + lightDirUnitVec.z * surfaceNorUnitVec.z)

        # calculate the diffuse and clap it to 0-255
        result = min(max(lightI * sp1.diffuse * diffdot, 0), 255)

    return result


# create the window and canvas
window = Tk()
window.title("Lakshika Udakandage - Simple Ray Tracer")


# create the canvas
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#555555")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH / 2, HEIGHT / 2), image=img, state="normal")

# create cam and screen and light
camPos = Vector(0, 0, -1000)
scrPos = Vector(0, 0, 0)
lightPos = Vector(200, 300, 600)
lightI = 0.9

# create the sphere
spLoc = Vector(700, 500, 1100)
spColor = Vector(10, 200, 10)
sp1 = Sphere(spLoc, 300, 0.8, 0.5, spColor)

# add the loop to paint the canvas
for y in range(1, HEIGHT):
    for x in range(1, WIDTH):
        castResult = raycast(x, y)
        if castResult > 0:
            # convert RGB to hex color
            hexcolor = "#{:02x}{:02x}{:02x}".format(int(castResult * sp1.color.x), int(castResult * sp1.color.y),
                                                    int(castResult * sp1.color.z))
            # pain the given pixel with the color
            img.put(hexcolor, (x, y))

# call the main function to crete the window and run the program
mainloop()