from timeDiff import diffTime
from datetime import datetime
def getFilteredFeedbackData(data):
    
    filteredData = []
    for i in data:
        name = i['user']['name']
        school = i['batch']['school']['name']
        grade = i['batch']['classes'][0]['grade']
        section = i['batch']['classes'][0]['section']
        teacher = i['batch']['allottedMentor']['mentorProfile']['user']['name']
        feedbackType = i['feedbackType']
        rating = i['rating'] if i['rating'] else "Not Given"
        updatedAt = i['updatedAt']
        createdAt = i['createdAt']
        timeTaken = diffTime(createdAt, updatedAt)
        
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
