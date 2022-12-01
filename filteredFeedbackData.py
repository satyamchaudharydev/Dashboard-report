from timeDiff import diffTime
from datetime import datetime
def getFilteredFeedbackData(data):
    
    filteredData = []
    index = 0
    for i in data:
        index += 3
        name = i['user']['name']
        school = i['batch']['school']['name']
        grade = i['batch']['classes'][0]['grade']
        section = i['batch']['classes'][0]['section']
        teacher = i['batch']['allottedMentor']['mentorProfile']['user']['name']
        feedbackType = i['feedbackType']
        rating = i['rating'] if i['rating'] else "Not Given"
        updatedAt = i['updatedAt']
        createdAt = i['createdAt']
        # add index to the 20 in timetaken
        timeTaken = 20 + index
        
        selectedFields = []
        if(len(i['selectedFields']) > 0):
            for selected_field in i['selectedFields']:  
                selectedFields.append(selected_field['tags']['label'])
        else:
            selectedFields.append("Not selected")
            
            
            
        selectedFields = ','.join(selectedFields)
        filteredData.append({
            'name': name,
            'school': school,
            'grade': grade,
            'section': section,
            'teacher': teacher,
            'feedbackType': feedbackType,
            'rating': rating,
            'timeTaken': timeTaken,
            'selectedFields': selectedFields,
            # 'time': only data
            'time': createdAt.split('T')[0]
        })
    return filteredData
