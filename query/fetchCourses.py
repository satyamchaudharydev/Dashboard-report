def fetchCourses_query():
    return """
    query{
         coursePackages{
            title
        }
        }
    """