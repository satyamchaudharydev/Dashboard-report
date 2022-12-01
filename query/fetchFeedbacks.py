def fetchFeedback_query(
    schoolId: str = None,
    grade: str = None,
    teacherId: str = None,

):
     
    # filterString = ''
    
    # print(filteredString)
    
    def getSchoolFilteredString(schoolId):
        if(schoolId): 
            return """
            {
                batch_some:{
                    school_some:{
                    id: "%s" 
                    }
                }
            }
        """ % (schoolId)
        else:
            return ''
    def getSchoolGradeString(gradeId):
        if(gradeId): 
            return """
            {
                batch_some:{
                    classes_some: {
                    grade: %s
                    }
                }
                }

        """ % (grade)
        else:
            return ''
    def getTeacherFilteredString(teacherId):
        if(teacherId): 
            return """
            {
                teacher:{
                    id: "%s" 
                }
            }
        """ % (teacherId)
        else:
            return ''        
    return  """
        query {
           sessionFeedbacks(
            filter: {
                AND: [
                    {
                    feedbackType: postClasswork,
                    },
                    """ +  getSchoolGradeString(schoolId)  + """
                    """ +  getSchoolFilteredString(grade)  + """
                    """ +  getTeacherFilteredString(teacherId)  + """
                ]
            }
        
        ){
        id
        createdAt
        updatedAt
        feedbackType
        rating
        selectedFields{
        tags{
            label
        }
        liked
        }
        user{
        name
        }
        course{
        title
        }
        batch{
        id
        classes{
            section
            grade
        }
        
        school{
            name
            id
        }
        allottedMentor{
        mentorProfile{
            user{
            name
            }
        } 
        }
        
        
        
        
        }
    }
        
        
        
        }
        
       

    
    
    """
    