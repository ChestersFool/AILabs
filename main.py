from tkinter import *

lasx, lasy = 0, 0
canvas_width, canvas_height = 300, 300
segment_width, segment_height = 100, 100
app = Tk()
app.geometry("400x400")


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), fill='black', width=10)
    lasx, lasy = event.x, event.y


canvas = Canvas(app, bg='white', height=canvas_height, width=canvas_width)

# canvas.pack(anchor='nw', fill='both', expand=1)
canvas.place(x=50, y=10)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)


def get_segment(pixels_color_matrix, row, col):
    black_pixels = 0
    for i in range(segment_height):
        for j in range(segment_width):
            color = pixels_color_matrix[i + row * segment_height][j + col * segment_width]
            if color == 1:
                black_pixels += 1

    if black_pixels >= (segment_width * segment_width) / 2:
        return 1
    return 0


def to_do_some_shit():
    pixels_color_matrix = get_matrix_pixels()
    vector = []
    for i in range(int(canvas_height / segment_height)):
        for j in range(int(canvas_width / segment_width)):
            vector.append(get_segment(pixels_color_matrix, i, j))
    print(vector)


def get_matrix_pixels():
    pixels_color_matrix = []
    for i in range(canvas_height):
        pixels_color_array = []
        for j in range(canvas_width):
            color = get_pixel_color(j, i)
            if color == 'white':
                color = 0
            else:
                color = 1
            pixels_color_array.append(color)
            print(color, end="")
        print()
        pixels_color_matrix.append(pixels_color_array)

    return pixels_color_matrix


def get_pixel_color(x, y):
    # canvas use different coordinates than turtle
    # y = -y
    # find IDs of all objects in rectangle (x, y, x, y)
    ids = canvas.find_overlapping(x, y, x, y)
    # if found objects
    if ids:
        # get ID of last object (top most)
        index = ids[-1]
        # get its color
        color = canvas.itemcget(index, "fill")
        # if it has color then return it
        if color:
            return color
    # if there was no object then return "white" - background color in turtle
    return "white"  # default color


btn = Button(text="start", command=to_do_some_shit)
btn.place(x=10, y=330)

app.mainloop()
