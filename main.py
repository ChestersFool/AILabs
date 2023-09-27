from tkinter import *


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), fill='black', width=5)
    lasx, lasy = event.x, event.y


def start_btn():
    pixels_color_matrix = get_matrix_pixels()
    vector = []
    for i in range(int(canvas_height / segment_height)):
        for j in range(int(canvas_width / segment_width)):
            vector.append(get_segment(pixels_color_matrix, i, j))
    print(vector)

    vector_normalized = []
    max_vec = max(vector)

    for elem in vector:
        vector_normalized.append(elem / max_vec)

    print(vector_normalized)

    digit = text.get("1.0", "end-1c")

    # write to the file
    f = open("models.txt", "a")
    f.write(' '.join(map(str, vector_normalized)))
    f.write(' ' + digit)
    f.close()


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


def get_segment(pixels_color_matrix, row, col):
    black_pixels = 0
    for i in range(segment_height):
        for j in range(segment_width):
            color = pixels_color_matrix[i + row * segment_height][j + col * segment_width]
            if color == 1:
                black_pixels += 1

    return black_pixels


def clear_canvas():
    canvas.delete('all')

def search_digit():
    pass

lasx, lasy = 0, 0
canvas_width, canvas_height = 300, 300
segment_width, segment_height = 60, 60

app = Tk()
app.geometry("400x400")

canvas = Canvas(app, bg='white', height=canvas_height, width=canvas_width)
canvas.place(x=50, y=10)
canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)

btn = Button(text="start", command=start_btn)
btn.place(x=10, y=330)

search_digit_btn = Button(text="search", command=search_digit)
search_digit_btn.place(x=150, y=330)

clear_btn = Button(text="clear", command=clear_canvas)
clear_btn.place(x=60, y=330)

text = Text(height=1, width=5)
text.place(x=100, y=330)

app.mainloop()
