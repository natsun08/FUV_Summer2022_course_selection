'''A program for matching students to available courses'''

import pandas as pd
#import interface

def take_input(major, minor, prof, courses_taken):
  '''
  Take major and course information from user
  Return: a dictionary contains major(s) and courses taken
  '''
  if minor == "Choose one":
    minor = "NA"
  
  user = {"major":major,"minor":minor, "prof":prof,"courses_taken":courses_taken}
  
  return user


def filter(user,level_priority,major):
  '''
  Filter in all the courses that is available for user's major and prerequisite
  Param: the user input
  Return: A dictionary of index that represents the available courses as key
  and its priority (the higher the number, the higher the priority)
  '''
  available_courses ={} 
  
  with open("available_courses.csv", encoding = 'utf-8') as readfile:
    file = pd.read_csv(readfile)
    for i in range(len(file)):
      majors = file.major[i]
      if ";" in file.major[i]:
        majors = file.major[i].split(";")
      #the user already taken this course
      priority = 0
      if (file.course[i] in user["courses_taken"]): 
        continue                                            

      #prioritize core couses
      if (file.major[i] == "CORE"):
        priority += 900

      #if this course is in user's major
      elif (user[major] in majors):
        #pre taken
        if (filter_prerequisite(user, file.prerequisite[i])):  
          if (file.level[i] == level_priority):
            priority += 200
            
          else:
            priority += 100
      #if user's prefered professor teaches
      if (file.intrucstor[i] in user['prof']):
        priority += 50

      if (priority > 0):
        available_courses[i] = priority
      
  #print(available_courses)
  
  return  dict(sorted(available_courses.items(), key=lambda item: item[1],reverse = True))


def filter_prerequisite(user, prerequisite):
  '''
  Return True if and only if the user has taken all the prerequisite
  '''
  if (type(prerequisite) == float):
    return True

  prerequisite = prerequisite.split(';')
  for course in prerequisite:
    if course not in user["courses_taken"]:
      return False

  return True

def calculate_level_priority(user,major):
  '''
  Calculate the number of foudation and concentration courses 
  the user still need to take for their major or minor, 
  prioritize taking foundation course
  if the number of foundation courses taken is <70%,
  else, prioritize taking foundation couses 
  if the number of foundation course < the number of concentration course
  else, prioritize taking concentration course
  
  Return: 1 if the user need to prioritize foundation courses
          2 if the user need to prioritize concentration courses
  '''
  
  with open("{}_requirement.csv".format(major),encoding = 'utf-8') as readfile:
    file = pd.read_csv(readfile)
    foundation_need = file[user[major]][0]
    concentration_need = file[user[major]][1]

    foundation_count = foundation_need
    concentration_count = concentration_need

  with open("Past_course.csv", encoding="utf-8") as readfile:
    file = pd.read_csv(readfile)
    for i in range(len(file)):
      if file.level[i] == 100 and file.course[i] in user["courses_taken"]:
        foundation_count -= 1
      if file.level[i] > 100 and file.course[i] in user["courses_taken"]:
        concentration_count -= 1
  try:
    if (foundation_count/foundation_need < 0.7):
      return 1,foundation_need,concentration_need
    elif (concentration_count/concentration_need < foundation_count/foundation_need):
      return 2,foundation_need,concentration_need
    else:
      return 1,foundation_need,concentration_need
  except ZeroDivisionError:
    return 2,foundation_need,concentration_need

def main(major, minor, prof, courses_taken):
    '''Tester function'''
    user = take_input(major, minor, prof, courses_taken)
    #Major
    level_priority,foundation_need,concentration_need = calculate_level_priority(user,"major")
    available_course_major = filter(user,level_priority,"major")
    should_take_courses_major = {
      "Priority Score": [],
      "Courses" : [],
      "Level" : [],
      "Intrucstor": [],
      "Date": [],
      "Start time": [],
      "End time": []
    }
    should_take_courses_minor = {
      "Priority Score": [],
      "Courses" : [],
      "Level" : [],
      "Intrucstor": [],
      "Date": [],
      "Start time": [],
      "End time": []
    }
    Text_1 = "You still need to study {} foundation courses and {} concentration courses for your major".format(foundation_need,concentration_need)
    
    with open("available_courses.csv",encoding = 'utf-8') as readfile:
          file = pd.read_csv(readfile)
          for i in (available_course_major):
            should_take_courses_major["Priority Score"].append(available_course_major[i])
            should_take_courses_major["Courses"].append(file.course[i])
            if file.level[i] == 0:
              should_take_courses_major["Level"].append("CORE")
            else:
              should_take_courses_major["Level"].append(file.difficulty[i])
            should_take_courses_major["Intrucstor"].append(file.intrucstor[i])
            should_take_courses_major["Date"].append(file.date[i])
            should_take_courses_major["Start time"].append(file.starttime[i])
            should_take_courses_major["End time"].append(file.endtime[i])
            

    #In case the user do not put in a minor
    if user["minor"] == "NA":
      return should_take_courses_major, dict(), Text_1, ""
    level_priority,foundation_need,concentration_need = calculate_level_priority(user,"minor")
    available_course_minor = filter(user,level_priority,"minor")
    
    Text_2 = "You still need to study {} foundation courses and {} concentration courses for your minor".format(foundation_need,concentration_need)

    with open("available_courses.csv",encoding = 'utf-8') as readfile:
        file = pd.read_csv(readfile)
        for i in (available_course_minor):
          if file.level[i] == 0:
            continue
          should_take_courses_minor["Priority Score"].append(available_course_minor[i])
          should_take_courses_minor["Courses"].append(file.course[i])
          should_take_courses_minor["Level"].append(file.difficulty[i])
          should_take_courses_minor["Intrucstor"].append(file.intrucstor[i])
          should_take_courses_minor["Date"].append(file.date[i])
          should_take_courses_minor["Start time"].append(file.starttime[i])
          should_take_courses_minor["End time"].append(file.endtime[i])
    return should_take_courses_major, should_take_courses_minor, Text_1, Text_2
  

if __name__ == "__main__":
  """Test the script without the interface"""
  print(main("CS", "MATH", [], []))

