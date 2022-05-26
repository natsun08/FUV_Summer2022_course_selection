import PySimpleGUI as sg
import pandas as pd
from course_select_alogrithm import main

sg.theme('Dark Amber')

choose_major = ["Choose one","CS", "IS", "MATH", "ENG"]
past_courses_checkbox = []
past_courses = []
prof_list = []
prof_list_display = []
display = []
window_major = None
window_error = None

class NoMajorError(Exception):
    """Exception class to raise when the user do not choose a major"""
    pass

def show_courses(major, minor, prof, courses_taken):
    """
    This function calculate and take out the 
    suggested courses and show them in a pop up with tables
    """
    should_take_courses_major,should_take_courses_minor,Text_1, Text_2 = main(major, 
                                                                            minor, 
                                                                            prof, 
                                                                            courses_taken)
    data_1 = pd.DataFrame(should_take_courses_major)
    headings_major = list(data_1)
    values_major = data_1.values.tolist()
    layout_major = [
        [sg.Text(Text_1)],
        ]
    if len(values_major) == 0:
        layout_major.append([sg.Text("There're currently no course that "
                                    + "serves your major this semester " +
                                    "that you're able to learn", 
                                    text_color = "white")])
    else:
        layout_major.append([sg.Table(values = values_major, headings = headings_major,
                                    key = "Table_major",vertical_scroll_only = False, 
                                    col_widths = 30, def_col_width=10, 
                                    auto_size_columns = True)])
    if Text_2 != "":
        data_2 = pd.DataFrame(should_take_courses_minor)
        headings_major = list(data_2)
        values_major = data_2.values.tolist()
        layout_major.append([sg.Text(Text_2)])
        if len(values_major) == 0:
            layout_major.append([sg.Text("There're currently no course that serves " + 
                                        "your minor this semester that you're " +
                                        "able to learn"
                                        , text_color = "white")])
        else:
            layout_major.append([sg.Table(values = values_major, 
                                        headings = headings_major, 
                                        key = "Table_minor", 
                                        vertical_scroll_only = False, 
                                        size = (1000, 10))])
    window_major = sg.Window(title = 'These courses is available this semester', 
                            layout = layout_major, 
                            resizable=True, finalize=True)
    return window_major

def please_choose_your_major():
    """Pop up when the user do not choose a major"""
    layout = [
        [sg.Text("Please choose your major")],
        [sg.Button("OK")]
    ]
    window_error =  sg.Window("Error", layout = layout, 
                            force_toplevel = True,keep_on_top = True, 
                            disable_close=True, finalize=True, 
                            element_justification= "center")
    return window_error

def run_course_selection():
    """
    Take out the data the user choose to calculate the suggested courses
    """
    courses_taken = []
    prof = []
    major = values["major"]
    if major == "Choose one":
        #If the user do not choose a major
        raise NoMajorError
    for i in past_courses:
        try:
            if values[i]  == True:
                courses_taken.append(i)
        except KeyError:
            pass
        finally:
            continue
    minor = values["minor"]
    for i in prof_list:
        try:
            if values[i]  == True:
                prof.append(i)
        except KeyError:
            pass
        finally:
            continue
    return show_courses(major, minor, prof, courses_taken)

def reset_visual(window_major):
    """Reset all the elements including closing other tabs (except the error pop up)"""
    window['major'].Update('Choose one')
    window['minor'].Update('Choose one')
    for i in past_courses:
        try:
            window[i].Update( False)
        except KeyError:
            pass
        finally:
            continue
    for i in prof_list:
        try:
            window[i].Update( False)
        except KeyError:
            pass
        finally:
            continue
    if window_major != None:
        window_major.close()
        window_major = None


#Get all the data for the check box
with open("Past_course.csv", encoding = 'utf-8') as readfile:
    file = pd.read_csv(readfile)
    for i in range(0,len(file)-1 , 2):
        past_courses.append(file.course[i])
        past_courses.append(file.course[i+1])
        past_courses_checkbox.append([sg.Checkbox(file.course[i], key = file.course[i]),sg.Checkbox(file.course[i+1], key = file.course[i+1])])

with open("available_courses.csv") as readfile:
    file = pd.read_csv(readfile)
    set_prof = set(file.intrucstor)
    i = 0
    for inst in set_prof:
        prof_list.append(inst)
        display.append(sg.Checkbox(inst, key = inst))
        if (i%2 == 1 and i < len(set_prof)) or(i%2 == 0 and i == len(set_prof)-1) :
            prof_list_display.append(display)
            display = []
        i = i + 1

#The main layout
layout = [
        [sg.Text("Choose your major", size = (20, 1)) , sg.Text("Choose your minor", size =(20, 1) )],
        [sg.OptionMenu(values = choose_major, default_value= "Choose one", key = "major", size = (20, 1)), sg.OptionMenu(values = choose_major, default_value= "Choose one", key = "minor", size = (20, 1))],
        [sg.Text("Choose your past courses",  size = (70,1)), sg.Text("Choose prefered instructor (optional)",  size = (50,1))],
        [sg.Column(past_courses_checkbox, scrollable = True, size = (600,300), key = "courses"), sg.Column(prof_list_display, scrollable = True, size = (500,300), key = "prof")],
        [sg.Button("Run", size = (30, 1)), sg.Button("Reset", size = (10, 1))]
        
]


#The main window
window_1 = sg.Window("Course Selection Program",
                layout,
                default_element_size=(12, 14),
                resizable=True, finalize=True)

#Main loop
while True:
    window, event, values = sg.read_all_windows()
    if event in ( sg.WINDOW_CLOSED, 'Exit' ):
        window.close()
        if window == window_major:
            window_major = None
        if window == window_error:
            window_error = None
        if window == window_1:
            break
    if event == "OK":
        window.close()
        window_error = None
    if window_error != None:
        continue
    if event == "Run":
        try:
            window_major = run_course_selection()
        except NoMajorError:
            window_error = please_choose_your_major()
        
    if event == "Reset":
        reset_visual(window_major)
        print(window)

window.close()


