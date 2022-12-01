def fetchSchool_query():
    return """
    query{
        schools{
            name
            id
            teachers{
				id
                user{
                    name
                }
          }
        }
    }
    """

