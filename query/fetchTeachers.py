def fetchTeachers_query(schoolId):  
# add open quote to schoolId and end quote to schoolId
    schoolId = '"' + schoolId + '"'
    print(schoolId)
    return """
        query{
            school(id: """ + schoolId + """){
                teachers{
                    user{
                        name
                    }
                }
                classes{
                    id
                    grade
                }
            }

        } 
     """   
          
