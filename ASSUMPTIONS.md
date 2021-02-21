# Assumptions
This document contains assumptions that were made during the completion of this assignment.

* API responses will be in JSON format, each response format will vary on method

* The `student` API response has the following skeleton:
    ```json
    {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "hashed",
        "textbooks": 
            [
                1,
                2,
                3
            ]
    }
    ```
    * Assume `student` API response has prehashed password

* Incoming student credentials are in JSON, exact parameters in documentation for each endpoint

* Unfortunately, since base64 cannot encode `:`, the QR Code does not work on `localhost` (the link breaks otherwise)

* Assume that a link to the page with each student's textbooks is only needed once the QR Code has been generated