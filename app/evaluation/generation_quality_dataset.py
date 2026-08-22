GENERATION_QUALITY_DATASET = [

    {
        "id": "g01",
        "question": "What is Big Data?",
        "expected_slides": [9],
        "reference_answer": (
            "Big Data is the capability to manage a huge volume of "
            "disparate data at the right speed and within the right "
            "time frame to allow real-time analysis and reaction."
        ),
        "required_concepts": [
            "huge volume",
            "disparate data",
            "speed",
            "real-time analysis",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g02",
        "question": "What is Volume in Big Data?",
        "expected_slides": [13],
        "reference_answer": (
            "Volume in Big Data refers to the amount of data that exists "
            "and the size or amount of data that is collected."
        ),
        "required_concepts": [
            "amount of data",
            "size",
            "data collected",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g03",
        "question": "What is Velocity in Big Data?",
        "expected_slides": [14],
        "reference_answer": (
            "Velocity in Big Data refers to the speed with which data "
            "is generated and the continuous flow of data from various sources."
        ),
        "required_concepts": [
            "speed",
            "data generated",
            "continuous flow",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g04",
        "question": "What is structured data?",
        "expected_slides": [19, 20],
        "reference_answer": (
            "Structured data is data that has a defined length and format. "
            "It is usually stored in a database, can be queried using SQL, "
            "and is organized in rows and columns."
        ),
        "required_concepts": [
            "defined length",
            "defined format",
            "database",
            "rows and columns",
            "SQL",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g05",
        "question": "What is unstructured data?",
        "expected_slides": [23],
        "reference_answer": (
            "Unstructured data is data that does not follow a specified "
            "format or predefined schema."
        ),
        "required_concepts": [
            "does not follow",
            "specified format",
            "predefined schema",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g06",
        "question": "What is semi-structured data?",
        "expected_slides": [26],
        "reference_answer": (
            "Semi-structured data falls between structured and unstructured "
            "data. It does not necessarily conform to a fixed schema but "
            "may have organizational properties, be self-describing, and "
            "contain simple label/value pairs."
        ),
        "required_concepts": [
            "between structured and unstructured",
            "organizational properties",
            "fixed schema",
            "self-describing",
            "label/value pairs",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g07",
        "question": "What is data virtualization?",
        "expected_slides": [57],
        "reference_answer": (
            "Data virtualization is the creation of virtual servers, "
            "infrastructures, devices, and computing resources."
        ),
        "required_concepts": [
            "virtual servers",
            "infrastructures",
            "devices",
            "computing resources",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g08",
        "question": "What is a relational database?",
        "expected_slides": [67],
        "reference_answer": (
            "A relational database stores and manages data using tables "
            "consisting of rows and columns. Relational databases are built "
            "on one or more relations and use a database schema."
        ),
        "required_concepts": [
            "tables",
            "rows",
            "columns",
            "relations",
            "database schema",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g09",
        "question": "What are key-value pair databases?",
        "expected_slides": [71, 73],
        "reference_answer": (
            "Key-value pair databases store data as key-value pairs. "
            "They are a type of non-relational database."
        ),
        "required_concepts": [
            "key-value pairs",
            "non-relational",
        ],
        "expected_abstention": False,
    },

    {
        "id": "g10",
        "question": "What is the CAP theorem in distributed databases?",
        "expected_slides": [],
        "reference_answer": "",
        "required_concepts": [],
        "expected_abstention": True,
    },

]